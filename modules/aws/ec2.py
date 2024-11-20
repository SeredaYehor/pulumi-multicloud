import pulumi
from pulumi_aws import ec2

class EC2Args:
    def __init__(self, vpc_id: pulumi.Input[str],
                       public_subnet_id: pulumi.Input[str],
                       ssh_key_name: pulumi.Input[str]):
        self.vpc_id = vpc_id
        self.public_subnet_id = public_subnet_id
        self.ssh_key_name = ssh_key_name

class EC2(pulumi.ComponentResource):
    def __init__(self, name: str, args: EC2Args, opts=None):
        super().__init__('aws:network:EC2', name, None, opts)

        network_interface = ec2.NetworkInterface("vpn-interface",
            opts=pulumi.ResourceOptions(parent=self),
            subnet_id=args.public_subnet_id,
            private_ips=["15.26.1.4"],
            tags={
                "Name": "vpn-interface",
                "CreatedBy": "pulumi",
            })

        security_group = ec2.SecurityGroup("vpn-security-group",
            opts=pulumi.ResourceOptions(parent=self),
            name="vpn-security-group",
            vpc_id=args.vpc_id,
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

        instance = ec2.Instance("vpn-instance",
            opts=pulumi.ResourceOptions(parent=self),
            ami="ami-0866a3c8686eaeeba",
            instance_type=ec2.InstanceType.T2_MICRO,
            subnet_id=args.public_subnet_id,
            network_interfaces=[{
                "network_interface_id": network_interface.id,
                "device_index": 0,
            }],
            key_name=args.ssh_key_name,
            vpc_security_group_ids=[security_group.id],
            tags={
                "Name": "vpn-instance",
                "CreatedBy": "pulumi",
            })
