import pulumi
import pulumi_azure_native as azure_native
import pulumi_azure as azure_old

class GatewayConnection:
    def __init__(self, key, az_virtual_network_gateway, input_resource_group_name):
        self.az_local_network_gateway = azure_native.network.LocalNetworkGateway(key["name"],
            gateway_ip_address=key["outside_ip"],
            local_network_address_space={
                "address_prefixes": ["15.26.0.0/16"],
            },
            local_network_gateway_name=key["name"],
            resource_group_name=input_resource_group_name)

        self.az_virtual_gateway_connection = azure_old.network.VirtualNetworkGatewayConnection(key["name"] + "-connection",
            resource_group_name=input_resource_group_name,
            virtual_network_gateway_id=az_virtual_network_gateway,
            local_network_gateway_id=self.az_local_network_gateway.id,
            connection_protocol="IKEv2",
            connection_mode="Default",
            use_policy_based_traffic_selectors=False,
            enable_bgp=False,
            type="IPsec",
            shared_key=key["shared_key"],
            name=key["name"] + "-connection")
