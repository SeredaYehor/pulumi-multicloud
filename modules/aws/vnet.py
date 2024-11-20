import pulumi
from pulumi_aws import ec2

class VirtualNetwork(pulumi.ComponentResource):
    def __init__(self, name: str, opts=None):
        super().__init__('aws:network:VirtualNetwork', name, None, opts)

        vpc = ec2.Vpc("vpn_vpc",
            opts=pulumi.ResourceOptions(parent=self),
            cidr_block="15.26.0.0/16",
            instance_tenancy="default",
            tags={
                "Name": "vpn_vpc",
                "CreatedBy": "pulumi",
            })

        public_subnet = ec2.Subnet("vpn_public_subnet",
            opts=pulumi.ResourceOptions(parent=self),
            vpc_id=vpc.id,
            cidr_block="15.26.1.0/24",
            map_public_ip_on_launch=True,
            tags={
                "Name": "vpn_public_subnet",
                "CreatedBy": "pulumi",
            })

        self.out_vpc_id = vpc.id
        self.out_public_subnet_id = public_subnet.id
