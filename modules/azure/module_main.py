import pulumi
import pulumi_azure_native as azure_native

from modules.azure.vnet    import VirtualNetwork, VirtualNetworkArgs
from modules.azure.gateway import VirtualNetworkGateway, VirtualNetworkGatewayArgs

class AzureModule(pulumi.ComponentResource): #module for creation of azure network
    def __init__(self, name: str, opts: pulumi.ResourceOptions = None):
        super().__init__('azure:module:Azure', name, None, opts) #used for creation of Pulumis component resource

        resource_group = azure_native.resources.ResourceGroup("vpn-aws",
            opts=pulumi.ResourceOptions(parent=self),
            resource_group_name="vpn-aws")

        vnet = VirtualNetwork("az-vnet",
            VirtualNetworkArgs(resource_group_name=resource_group.name),
            opts=pulumi.ResourceOptions(parent=self, depends_on=[resource_group]))

        gateway = VirtualNetworkGateway("az-gateway",
            VirtualNetworkGatewayArgs(resource_group_name=resource_group.name,
                                      subnet_id=vnet.out_gateway_subnet_id),
            opts=pulumi.ResourceOptions(parent=self, depends_on=[resource_group]))

        self.out_vpn_gateway_ip = gateway.out_vpn_gateway_ip
        self.out_virtual_network_gateway_id = gateway.out_virtual_network_gateway_id
        self.out_resource_group_name = resource_group.name
