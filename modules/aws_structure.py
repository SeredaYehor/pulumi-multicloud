import pulumi
from pulumi_aws import ec2

class AWSComponentArgs:
    def __init__(self, gateway_ip: pulumi.Input[str], ssh_key_name: pulumi.Input[str]):
        self.gateway_ip = gateway_ip
        self.ssh_key_name = ssh_key_name

class AWSComponent(pulumi.ComponentResource):
    def __init__(self, name: str, args: AWSComponentArgs, opts=None):
        super().__init__('aws:network:AWSComponent', name, None, opts)

        aws_vpc = ec2.Vpc("vpn-vpc",
            opts=pulumi.ResourceOptions(parent=self),
            cidr_block="15.26.0.0/16",
            instance_tenancy="default",
            tags={
                "Name": "vpn-vpc",
                "CreatedBy": "pulumi",
            })

        aws_public_subnet = ec2.Subnet("vpn-public-subnet",
            opts=pulumi.ResourceOptions(parent=self),
            vpc_id=aws_vpc.id,
            cidr_block="15.26.1.0/24",
            map_public_ip_on_launch=True,
            tags={
                "Name": "vpn-public-subnet",
                "CreatedBy": "pulumi",
            })

        aws_customer_gateway = ec2.CustomerGateway("aws-azure-customer-gateway",
            opts=pulumi.ResourceOptions(parent=self),
            bgp_asn="65000",
            ip_address=args.gateway_ip,
            type="ipsec.1",
            tags={
                "Name": "aws-azure-customer-gateway",
                "CreatedBy": "pulumi",
            })

        aws_vpn_gateway = ec2.VpnGateway("aws_vpn_gateway",
            opts=pulumi.ResourceOptions(parent=self),
            vpc_id=aws_vpc.id,
            tags={
                "Name": "aws_vpn_gateway",
                "CreatedBy": "pulumi",
            })

        aws_internet_gateway = ec2.InternetGateway("aws-azure-igw",
            opts=pulumi.ResourceOptions(parent=self),
            vpc_id=aws_vpc.id,
            tags={
                "Name": "aws-azure-igw",
                "CreatedBy": "pulumi",
            })

        aws_public_route_table = ec2.RouteTable("aws-azure-public-rt",
            opts=pulumi.ResourceOptions(parent=self),
            vpc_id=aws_vpc.id,
            routes=[{
                "cidr_block": "0.0.0.0/0",
                "gateway_id": aws_internet_gateway.id,
            },
            {
                "cidr_block": "15.27.1.0/24",
                "gateway_id": aws_vpn_gateway.id,
            },
            ],
            tags={
                "Name": "aws-azure-public-rt",
                "CreatedBy": "pulumi",
            })

        aws_public_rt_association = ec2.RouteTableAssociation("aws-azure-public-rta",
            opts=pulumi.ResourceOptions(parent=self),
            subnet_id=aws_public_subnet.id,
            route_table_id=aws_public_route_table.id)

        aws_vpn_connection = ec2.VpnConnection("aws-azure-vpn-connection",
            opts=pulumi.ResourceOptions(parent=self),
            vpn_gateway_id=aws_vpn_gateway.id,
            customer_gateway_id=aws_customer_gateway.id,
            static_routes_only=True,
            type="ipsec.1",
            tags={
                "Name": "aws-azure-vpn-connection",
                "CreatedBy": "pulumi",
            })

        aws_vpn_connection_route = ec2.VpnConnectionRoute("aws-vpn-connection-route",
            opts=pulumi.ResourceOptions(parent=self),
            destination_cidr_block="15.27.1.0/24",
            vpn_connection_id=aws_vpn_connection.id)

        aws_security_group = ec2.SecurityGroup("aws-vpn-security-group",
            opts=pulumi.ResourceOptions(parent=self),
            name="aws-vpn-security-group",
            vpc_id=aws_vpc.id,
            ingress=[{
                "from_port": 22,
                "to_port": 22,
                "protocol": "tcp",
                "cidr_blocks": ["0.0.0.0/0"],
            },
            {
                "from_port": 0,
                "to_port": 0,
                "protocol": "-1",
                "cidr_blocks": ["15.27.1.0/24"],
            }])

        aws_instance = ec2.Instance("aws-vpn-instance",
            opts=pulumi.ResourceOptions(parent=self),
            ami="ami-0866a3c8686eaeeba",
            instance_type=ec2.InstanceType.T2_MICRO,
            associate_public_ip_address=True,
            private_ip="15.26.1.5",
            key_name=args.ssh_key_name,
            subnet_id=aws_public_subnet.id,
            vpc_security_group_ids=[aws_security_group.id],
            tags={
                "Name": "aws-vpn-instance",
                "CreatedBy": "pulumi",
            })
