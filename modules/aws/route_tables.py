import pulumi
from pulumi_aws import ec2

class RouteTablesArgs:
    def __init__(self, vpn_gateway_id: pulumi.Input[str],
                       internet_gateway_id: pulumi.Input[str],
                       vpc_id: pulumi.Input[str],
                       public_subnet_id: pulumi.Input[str]):
        self.vpn_gateway_id = vpn_gateway_id
        self.internet_gateway_id = internet_gateway_id
        self.vpc_id = vpc_id
        self.public_subnet_id = public_subnet_id

class RouteTables(pulumi.ComponentResource):
    def __init__(self, name: str, args: RouteTablesArgs, opts=None):
        super().__init__('aws:network:RouteTables', name, None, opts)

        public_route_table = ec2.RouteTable("azure-public-rt",
            opts=pulumi.ResourceOptions(parent=self),
            vpc_id=args.vpc_id,
            routes=[{
                "cidr_block": "0.0.0.0/0",
                "gateway_id": args.internet_gateway_id,
            },
            {
                "cidr_block": "15.27.1.0/24",
                "gateway_id": args.vpn_gateway_id,
            },
            ],
            tags={
                "Name": "azure_public_rt",
                "CreatedBy": "pulumi",
            })

        public_rt_association = ec2.RouteTableAssociation("azure_public_rta",
            opts=pulumi.ResourceOptions(parent=self),
            subnet_id=args.public_subnet_id,
            route_table_id=public_route_table.id)

