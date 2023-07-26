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
from plugin.common.script_runner import ScriptRunner

@operation
def execute(ctx, **kwargs):
    # getting ssh config from node properties
    host_config = ctx.node.properties.get('ssh_config', {})
    
    _hostname = host_config.get('hostname', '')
    _username = host_config.get('username', '')
    _privatekey = host_config.get('privatekey', '')
    _commands = host_config.get('commands', [])
    
    ctx.logger.info(f'executing commands: {_commands}')
    # log the ssh config
    ctx.logger.info('SSH config: {0}, {1}, {2}'.format( _hostname, _username, _privatekey))
    
    _client = ScriptRunner(_hostname, _username, _privatekey, ctx.logger)
    _cmd_outputs = _client.execute(_commands)
    
    ctx.logger.info(f'commands output: {_cmd_outputs}')
    ctx.logger.info('SSH commands executed successfully')