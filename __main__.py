import pulumi
from modules.aws.module_main import AWSModule, AWSModuleArgs #module which creates AWS network resources
from modules.azure.module_main import AzureModule
from modules.local_gateways.module_main import LocalGateways, LocalGatewaysArgs

config = pulumi.Config()

azure = AzureModule('azure_module') #passing inputs to module as Args object
aws = AWSModule('aws_module',
    AWSModuleArgs(gateway_ip=azure.out_vpn_gateway_ip,
                  config=config))

local_gateways = LocalGateways('local_gateways',
    LocalGatewaysArgs(virtual_network_gateway_id=azure.out_virtual_network_gateway_id,
                       resource_group_name=azure.out_resource_group_name,
                       config=config))
