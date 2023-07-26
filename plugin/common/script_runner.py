import paramiko
import io

class ScriptRunner: 
    
    def __init__(self, hostname, username, private_key_str, logger) -> None:
        self.hostname = hostname
        self.username = username
        self.private_key_str = private_key_str
        self.logger = logger
        
    
    def execute(self, commands ):
        # Create an SSH client
        ssh_client = paramiko.SSHClient()

        # Automatically add the server's host key (this is insecure, do not use in production)
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Load the private key from the string for authentication
            private_key = paramiko.RSAKey(file_obj=io.StringIO(self.private_key_str))

            # Connect to the remote server using the private key
            ssh_client.connect(self.hostname, username=self.username, pkey=private_key)

            outputs = {}  # Dictionary to store the output of each command

            for command in commands:
                # Execute the command on the remote server
                stdin, stdout, stderr = ssh_client.exec_command(command)

                # Read the output of the command
                output = stdout.read().decode('utf-8')

                # Store the output in the dictionary
                outputs[command] = output.strip()

            return outputs

        except paramiko.AuthenticationException:
            self.logger.error("Authentication failed. Please check your private key or credentials.")
        except paramiko.SSHException as ssh_ex:
            self.logger.error(f"SSH error: {ssh_ex}")
        except Exception as ex:
            self.logger.error(f"Error: {ex}")
        finally:
            # Close the SSH connection
            ssh_client.close()

