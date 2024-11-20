import pulumi
from pulumi_aws import ec2

class VPNConnectionArgs:
    def __init__(self, vpn_gateway_id: pulumi.Input[str],
                       customer_gateway_id: pulumi.Input[str]):
        self.vpn_gateway_id = vpn_gateway_id
        self.customer_gateway_id = customer_gateway_id

class VPNConnection(pulumi.ComponentResource):
    def __init__(self, name: str, args: VPNConnectionArgs, opts=None):
        super().__init__('aws:network:VPNConnection', name, None, opts)

        vpn_connection = ec2.VpnConnection("azure_vpn_connection",
            opts=pulumi.ResourceOptions(parent=self),
            vpn_gateway_id=args.vpn_gateway_id,
            customer_gateway_id=args.customer_gateway_id,
            static_routes_only=True,
            type="ipsec.1",
            tags={
                "Name": "azure_vpn_connection",
                "CreatedBy": "pulumi",
            })

        vpn_connection_route = ec2.VpnConnectionRoute("vpn_connection_route",
            opts=pulumi.ResourceOptions(parent=self),
            destination_cidr_block="15.27.1.0/24",
            vpn_connection_id=vpn_connection.id)

