import pulumi

from modules.aws.vnet           import VirtualNetwork
from modules.aws.gateway        import AWSGateways, AWSGatewaysArgs
from modules.aws.vpn_connection import VPNConnection, VPNConnectionArgs
from modules.aws.route_tables   import RouteTables, RouteTablesArgs
from modules.aws.ec2            import EC2, EC2Args

class AWSModuleArgs:
    def __init__(self, gateway_ip: pulumi.Input[str],
                       config: pulumi.Input[pulumi.config.Config]):
        self.gateway_ip = gateway_ip
        self.config = config

class AWSModule(pulumi.ComponentResource): #module for creation of azure network
    def __init__(self, name: str, args: AWSModuleArgs, opts: pulumi.ResourceOptions = None):
        super().__init__('aws:module:AWSModule', name, None, opts) #used for creation of Pulumis component resource

        vpc_component = VirtualNetwork('vpc_component',
            opts=pulumi.ResourceOptions(parent=self))

        gateways_component = AWSGateways('gateways_component',
            AWSGatewaysArgs(gateway_ip=args.gateway_ip,
                            vpc_id=vpc_component.out_vpc_id),
            opts=pulumi.ResourceOptions(parent=self))

        route_tables_component = RouteTables('route_tables_component',
            RouteTablesArgs(vpn_gateway_id=gateways_component.out_vpn_gateway_id,
                            internet_gateway_id=gateways_component.out_internet_gateway_id,
                            vpc_id=vpc_component.out_vpc_id,
                            public_subnet_id=vpc_component.out_public_subnet_id),
            opts=pulumi.ResourceOptions(parent=self))

        vpn_connection_component = VPNConnection('vpn_connection_component',
            VPNConnectionArgs(vpn_gateway_id=gateways_component.out_vpn_gateway_id,
                              customer_gateway_id=gateways_component.out_customer_gateway_id),
            opts=pulumi.ResourceOptions(parent=self))

        ssh_key=args.config.get("aws-ssh-key-name")

        ec2_component = EC2('ec2_component',
            EC2Args(vpc_id=vpc_component.out_vpc_id,
                    public_subnet_id=vpc_component.out_public_subnet_id,
                    ssh_key_name=ssh_key),
            opts=pulumi.ResourceOptions(parent=self))
