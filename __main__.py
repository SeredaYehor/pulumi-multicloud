import pulumi
import pulumi_azure_native as azure_native
from modules.aws_structure import AWSComponent, AWSComponentArgs #module which creates AWS network resources
from modules.azure_structure import AzureComponent, AzureComponentArgs
from modules.local_network_gateway import GatewayConnection


config = pulumi.Config()
keys = config.require_object("vpn-tunnels-shared-keys") #retrieving value from configs
aws_ssh_key=config.get("aws-ssh-key-name")
azure_public_ssh_key=config.get("azure-vm-public-key")
azure_resource_group = config.get("resource-group-name")
connect_clouds = config.require_object("connect-clouds")
connections = {}

azure = AzureComponent('azure-infrastructure',
        AzureComponentArgs(resource_group_name=azure_resource_group, ssh_public_key=azure_public_ssh_key)) #passing inputs to module as Args object
aws = AWSComponent('aws-infrastructure',
      AWSComponentArgs(gateway_ip=azure.vpn_gateway_ip, ssh_key_name=aws_ssh_key))

if connect_clouds:
    for key in keys:
        connections[key["name"]] = GatewayConnection(key, azure.virtual_network_gateway_id, azure_resource_group)
