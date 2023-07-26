
import requests
from plugin.equinix.utils import NotFoundExcpetion, ServerNotAvailable

EQIX_METAL_API = "https://api.equinix.com/metal/v1"

class Metal:
    
    def __init__(self, api_key, project_id, logger):
        self.base_url = EQIX_METAL_API
        self.api_url = self.base_url + "/projects/{0}".format(project_id)
        self.logger = logger
        self.headers = {
            "X-Auth-Token": api_key,
            "Content-Type": "application/json",
        }
        
    def on_demand(self, metro, plan, hostname, operating_system, userdata=''):
        """Request on demand Equinix Metal device

        Args:
            metro (string): Equinix metal metro
            plan (string): Equinix metal plan
            hostname (string): hostname for the device
            operating_system (string): OS for the device
            userdata (str, optional): Userdata for the device. Defaults to ''.

        Returns:
            device: Equinix Metal device details
        """
        
        device_payload = {
            "metro": metro,
            "plan": plan,
            "hostname": hostname,
            "operating_system": operating_system,
            "userdata": userdata
        }
        
        self.logger.info("Provisioning bare metal server")
        self.logger.debug(f"Payload: {device_payload}")
        
        url = self.api_url + "/devices"
        try:
            response = requests.post(
                url, json=device_payload, headers=self.headers)
            
            if response.status_code == 201:
                self.logger.info("Successfully initiated Equinix Metal server provisioning!")
                return response.json()
            else:
                self.logger.error(f"Unable to provision Equinix Metal: {response.status_code} - {response.text}")
                raise Exception(f"Unable to provision Equinix Metal: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Unable to initiate Equinix Metal server: {e}")
            raise e
        
    def get_device(self, device_id):
        """Get Equinix Metal details

        Args:
            device_id (UUID): unique identifier for the device

        Raises:
            NotFoundExcpetion: Equinix Metal device with given UUID is not found

        Returns:
            device_details: Equinix Metal details
        """
        url = self.base_url + "/devices/{0}".format(device_id)
        
        # return device details
        self.logger.info(f"Fetching device details for device id: {device_id}")
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            self.logger.info("Server provisioning completed successfully!")
            return response.json()
        elif response.status_code == 404:
            self.logger.error(f"Device with id {device_id} not found")
            raise NotFoundExcpetion(f"Device with id {device_id} not found")
        elif response.status_code >= 500:
            self.logger.error(f"Server not available: {response.status_code} - {response.text}")
            raise ServerNotAvailable(f"Server not available: {response.status_code} - {response.text}")
        else:
            self.logger.info("Server is still provisioning. Please try again later...")
            return None
    
    def is_device_active(self, device_id):
        """ Check if the device is active

        Args:
            device_id (UUID): unique identifier for the device

        Returns:
            boolean: return True if device is active else False
        """
        
        self.logger.info(f"Fetching device details for device id: {device_id}")
      
        device_details = self.get_device(device_id)
        if device_details and device_details["state"]:
            server_status = device_details["state"]
            if server_status == "active":
                self.logger.info("Server provisioning completed successfully!")
                return True
        self.logger.info("Server is still provisioning. Waiting...")
        return False
        
    
    def stop(self, device_id):
        self.logger.info(f"Stopping device with id: {device_id}")
        pass
    
    def restart(self, device_id):
        """Restart Equinix Metal device with given UUID

        Args:
            device_id (UUID): Restart Equinix Metal device with given UUID

        Raises:
            Exception: Generic exception if the restart fails
            
        Returns:
            json: response from Equinix Metal API
        """
        
        self.logger.info(f"Restarting device with id: {device_id}")
        url = self.base_url + "/devices/{0}/actions".format(device_id)
        action_payload = {
            "type": "reboot"
        }
        
        try:
            response = requests.post(url, json=action_payload, headers=self.headers)
            
            if response.status_code == 202:
                self.logger.info("Bare metal server reboot initiated successfully!")
                return response.json()
            else:
                self.logger.error(f"Error: {response.status_code} - {response.text}")
                raise Exception(f"Unable to reboot Equinix Metal: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"An error occurred while rebooting: {e}")
            raise e

    def delete(self, device_id):
        """Delete Equinix Metal device with given UUID

        Args:
            device_id (UUID): Delete Equinix Metal device with given UUID

        Raises:
            Exception: Exception if the delete fails
    
        """
       
        self.logger.info(f"Deleting device with id: {device_id}")
        
        url = self.base_url + "/devices/{0}".format(device_id)
        
        try:
            response = requests.delete(url, headers=self.headers)
            
            if response.status_code == 204:
                self.logger.info("Bare metal server deprovisioned successfully!")
            else:
                self.logger.error(f"Error: {response.status_code} - {response.text}")
                raise Exception(f"Unable to deprovision Equinix Metal: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"An error occurred while deprovisioning: {e}")
            raise e
        
        
        
