# you can use the decorators that gives the ability
# to mark the task as resumable or not
from cloudify.decorators import operation
# you can use the exeption logic to mark the operation final status
# [ as it will affect the workflow execution] you can raise according
# to your logic could be `RecoverableError` if you want you code to do retries
# and wait for a certian period of time or `NonRecoverableError`
# which means mark this operation as failure and stop the flow right there
# unless you set ignore_failure flag as true on the workflow trigger
from cloudify.exceptions import NonRecoverableError

# 'ctx' is always passed as a keyword argument to operations, so
# your operation implementation must either specify it in the arguments
# list, or accept '**kwargs'. Both are shown here.
from plugin.equinix.metal import Metal

@operation
def create_metal_server(ctx, **kwargs):
    # getting some values from passed properties
    host_config = ctx.node.properties.get('metal_config', {})
    
    _project_id = host_config.get('project_id', '')
    _api_key = host_config.get('api_key', '')
    _hostname = host_config.get('hostname', '')
    _plan = host_config.get('plan', '')
    _metro = host_config.get('metro', '')
    _os = host_config.get('operating_system', '')
    _userdata = host_config.get('userdata', '')
    
    ctx.logger.info('Project ID: {0}, hostname: {1}, plan: {2}, metro: {3}, os: {4}'.format(
        _project_id, _hostname, _plan, _metro, _os))
    
    _client = Metal(_api_key, _project_id, ctx.logger)
     
    # check request is already processed
    _metal_server_id = ctx.instance.runtime_properties.get('metal_server_id', '')
    
    if not _metal_server_id:
        try: 
            on_demand = _client.on_demand(metro=_metro, plan=_plan, hostname=_hostname, operating_system=_os, userdata=_userdata)
            ctx.instance.runtime_properties['metal_server_id'] = on_demand["id"]
            _metal_server_id = on_demand["id"]
        except Exception as e:
            ctx.logger.error(f"Unable to provision Equinix Metal: {e}")
            raise NonRecoverableError(e)
    
    # try catch with non recoverable error
    try:
        if not _client.is_device_active(_metal_server_id):
            return ctx.operation.retry(message='Equinix Metal server is not ready yet.', retry_after=60)
    except Exception as e:
        ctx.logger.error(f"Unable to provision Equinix Metal: {e}")
        raise NonRecoverableError(e)
    
    _device_details = _client.get_device(_metal_server_id)
    
    ctx.instance.runtime_properties['metal_server'] = _device_details
    # extract the ip address and log it
    ctx.logger.info(f"IP address: {_device_details['ip_addresses'][0]['address']}")
    ctx.instance.runtime_properties['ip'] = _device_details["ip_addresses"][0]["address"]
    ctx.logger.info('Equinix Metal server & is ready for deployment')


@operation
def start_metal_server(ctx, **kwargs):    
    ctx.logger.info('Waiting for Equinix Metal Server to be ready')


@operation
def stop_metal_server(ctx, **kwargs):
    ctx.logger.info('Stopping Equinix Metal server')
    
    metal_server_id = ctx.instance.runtime_properties.get('metal_server_id', {})
    host_config = ctx.node.properties.get('metal_config', {})
    _project_id = host_config.get('project_id', '')
    _api_key = host_config.get('api_key', '')
    _client = Metal(_api_key, _project_id, ctx.logger)
    _client.stop(metal_server_id)
    
    ctx.logger.info('Stopped Equinix Metal server')


@operation
def restart_metal_server(ctx, **kwargs):
    
    ctx.logger.info('Restarting Equinix Metal server')
    
    metal_server_id = ctx.instance.runtime_properties.get('metal_server_id', {})
    host_config = ctx.node.properties.get('metal_config', {})
    _project_id = host_config.get('project_id', '')
    _api_key = host_config.get('api_key', '')
    _client = Metal(_api_key, _project_id,ctx.logger)
    
    _client.restart(metal_server_id)
    ctx.logger.info('Restarted Equinix Metal server')


@operation
def delete_metal_server(ctx, **kwargs):
    ctx.logger.info('Deleting Equinix Metal server')
    
    metal_server_id = ctx.instance.runtime_properties.get('metal_server_id', {})
    host_config = ctx.node.properties.get('metal_config', {})
    _project_id = host_config.get('project_id', '')
    _api_key = host_config.get('api_key', '')
    _client = Metal(_api_key, _project_id, ctx.logger)
    _client.delete(metal_server_id)
    # reset the runtime properties
    ctx.instance.runtime_properties['metal_server_id'] = None
    ctx.instance.runtime_properties['metal_server'] = None
    
    ctx.logger.info('Deleted Equinix Metal server')
