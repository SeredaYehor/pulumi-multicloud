import pulumi
import modules.local_gateways.gateway

class LocalGatewaysArgs:
    def __init__(self, virtual_network_gateway_id: pulumi.Input[str],
                       resource_group_name: pulumi.Input[str],
                       config: pulumi.Input[pulumi.config.Config]):
        self.gateway_id = virtual_network_gateway_id
        self.resource_group_name = resource_group_name
        self.config = config

class LocalGateways(pulumi.ComponentResource): #module for creation of azure network
    def __init__(self, name: str, args: LocalGatewaysArgs, opts: pulumi.ResourceOptions = None):
        super().__init__('azure:module:LocalGateways', name, None, opts) #used for creation of Pulumis component resource

        keys = args.config.require_object("vpn-tunnels-shared-keys") #retrieving value from configs
        connect_clouds = args.config.require_object("connect-clouds")
        connections = {}

        if connect_clouds:
            for key in keys:
                connections[key["name"]] = GatewayConnection(key, args.gateway_id, args.resource_group_name)
