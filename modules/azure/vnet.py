import pulumi
import pulumi_azure_native as azure_native

class VirtualNetworkArgs: #class for passing inputs to module
    def __init__(self, resource_group_name: pulumi.Input[str]):
        self.resource_group_name = resource_group_name

class VirtualNetwork(pulumi.ComponentResource): #module for creation of azure network
    def __init__(self, name: str, args: VirtualNetworkArgs, opts: pulumi.ResourceOptions = None):
        super().__init__('azure:network:VirtualNetwork', name, None, opts) #used for creation of Pulumis component resource

        az_virtual_network = azure_native.network.VirtualNetwork("vpn-net",
            address_space={
                "address_prefixes": ["15.27.0.0/16"],
            },
            virtual_network_name="vpn-net",
            resource_group_name=args.resource_group_name,
            opts=pulumi.ResourceOptions(parent=self))

        az_public_subnet = azure_native.network.Subnet("public-subnet",
            opts=pulumi.ResourceOptions(depends_on=[az_virtual_network], parent=self),
            address_prefix="15.27.1.0/24",
            subnet_name="public-subnet",
            virtual_network_name="vpn-net",
            resource_group_name=args.resource_group_name)

        az_gateway_subnet = azure_native.network.Subnet("GatewaySubnet",
            opts=pulumi.ResourceOptions(depends_on=[az_virtual_network], parent=self),
            address_prefix="15.27.2.0/24",
            subnet_name="GatewaySubnet",
            virtual_network_name="vpn-net",
            resource_group_name=args.resource_group_name)

        self.out_gateway_subnet_id = az_gateway_subnet.id
