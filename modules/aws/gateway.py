import pulumi
from pulumi_aws import ec2

class AWSGatewaysArgs:
    def __init__(self, gateway_ip: pulumi.Input[str], vpc_id: pulumi.Input[str]):
        self.gateway_ip = gateway_ip
        self.vpc_id = vpc_id

class AWSGateways(pulumi.ComponentResource):
    def __init__(self, name: str, args: AWSGatewaysArgs, opts=None):
        super().__init__('aws:network:AWSGateways', name, None, opts)

        customer_gateway = ec2.CustomerGateway("azure_customer_gateway",
            opts=pulumi.ResourceOptions(parent=self),
            bgp_asn="65000",
            ip_address=args.gateway_ip,
            type="ipsec.1",
            tags={
                "Name": "azure_customer_gateway",
                "CreatedBy": "pulumi",
            })

        vpn_gateway = ec2.VpnGateway("vpn_gateway",
            opts=pulumi.ResourceOptions(parent=self),
            vpc_id=args.vpc_id,
            tags={
                "Name": "vpn_gateway",
                "CreatedBy": "pulumi",
            })

        internet_gateway = ec2.InternetGateway("azure_igw",
            opts=pulumi.ResourceOptions(parent=self),
            vpc_id=args.vpc_id,
            tags={
                "Name": "azure_igw",
                "CreatedBy": "pulumi",
            })

        self.out_customer_gateway_id = customer_gateway.id
        self.out_vpn_gateway_id = vpn_gateway.id
        self.out_internet_gateway_id = internet_gateway.id
