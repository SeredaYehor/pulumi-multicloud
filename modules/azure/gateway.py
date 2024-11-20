import pulumi
import pulumi_azure_native as azure_native

class VirtualNetworkGatewayArgs: #class for passing inputs to module
    def __init__(self, resource_group_name: pulumi.Input[str],
        subnet_id: pulumi.Input[str]):
        self.resource_group_name = resource_group_name
        self.subnet_id = subnet_id

class VirtualNetworkGateway(pulumi.ComponentResource): #module for creation of azure network
    def __init__(self, name: str, args: VirtualNetworkGatewayArgs, opts: pulumi.ResourceOptions = None):
        super().__init__('azure:network:VirtualNetworkGateway', name, None, opts) #used for creation of Pulumis component resource

        az_public_ip_address = azure_native.network.PublicIPAddress("gateway-ip",
            public_ip_address_name="gateway-ip",
            resource_group_name=args.resource_group_name,
            opts=pulumi.ResourceOptions(parent=self))

        az_virtual_network_gateway = azure_native.network.VirtualNetworkGateway("vpn-gateway",
            active_active=False,
            gateway_type=azure_native.network.VirtualNetworkGatewayType.VPN,
            enable_bgp=False,
            virtual_network_gateway_name="vpn-gateway",
            vpn_type=azure_native.network.VpnType.ROUTE_BASED,
            sku={
                "name": azure_native.network.VirtualNetworkGatewaySkuName.VPN_GW1,
                "tier": azure_native.network.VirtualNetworkGatewaySkuTier.VPN_GW1,
            },
            ip_configurations=[{
                "name": "gwipconfig1",
                "private_ip_allocation_method": azure_native.network.IPAllocationMethod.DYNAMIC,
                "public_ip_address": {
                    "id": az_public_ip_address.id,
                },
                "subnet": {
                    "id": args.subnet_id,
                },
            }],
            resource_group_name=args.resource_group_name,
            opts=pulumi.ResourceOptions(parent=self))

        self.out_vpn_gateway_ip = az_virtual_network_gateway.bgp_settings.bgp_peering_addresses[0].tunnel_ip_addresses[0]
        self.out_virtual_network_gateway_id = az_virtual_network_gateway.id
