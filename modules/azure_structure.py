import pulumi
import pulumi_azure_native as azure_native

class AzureComponentArgs: #class for passing inputs to module
    def __init__(self, resource_group_name: pulumi.Input[str], ssh_public_key: pulumi.Input[str]):
        self.resource_group_name = resource_group_name
        self.ssh_public_key = ssh_public_key

class AzureComponent(pulumi.ComponentResource): #module for creation of azure network
    def __init__(self, name: str, args: AzureComponentArgs, opts: pulumi.ResourceOptions = None):
        super().__init__('azure:network:AzureComponent', name, None, opts) #used for creation of Pulumis component resource

        az_virtual_network = azure_native.network.VirtualNetwork("vpn-net",
            address_space={
                "address_prefixes": ["15.27.0.0/16"],
            },
            virtual_network_name="vpn-net",
            resource_group_name=args.resource_group_name,
            opts=pulumi.ResourceOptions(parent=self))

        az_public_subnet = azure_native.network.Subnet("public-subnet",
            opts=pulumi.ResourceOptions(depends_on=[az_virtual_network], parent=self),
            address_prefix="15.27.1.0/24",
            subnet_name="public-subnet",
            virtual_network_name="vpn-net",
            resource_group_name=args.resource_group_name)

        az_gateway_subnet = azure_native.network.Subnet("GatewaySubnet",
            opts=pulumi.ResourceOptions(depends_on=[az_virtual_network], parent=self),
            address_prefix="15.27.2.0/24",
            subnet_name="GatewaySubnet",
            virtual_network_name="vpn-net",
            resource_group_name=args.resource_group_name)

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
                    "id": az_gateway_subnet.id,
                },
            }],
            resource_group_name=args.resource_group_name,
            opts=pulumi.ResourceOptions(parent=self))

        az_vm_public_ip_address = azure_native.network.PublicIPAddress("vm-ip",
            public_ip_address_name="vm-ip",
            resource_group_name=args.resource_group_name,
            opts=pulumi.ResourceOptions(parent=self))

        az_network_interface = azure_native.network.NetworkInterface("vpn-network-interface",
            network_interface_name="vpn-network-interface",
            resource_group_name=args.resource_group_name,
            ip_configurations=[{
                "name": "ipconfig1",
                "public_ip_address": {
                     "id": az_vm_public_ip_address.id,
                },
                "subnet": {
                     "id": az_public_subnet.id,
                },
            }],
            opts=pulumi.ResourceOptions(parent=self))

        az_network_security_group = azure_native.network.NetworkSecurityGroup("vpn-nsg",
            network_security_group_name="vpn-nsg",
            resource_group_name=args.resource_group_name,
            security_rules=[{
                "access": azure_native.network.SecurityRuleAccess.ALLOW,
                "destination_address_prefix": "15.27.1.0/24",
                "destination_port_range": "*",
                "direction": azure_native.network.SecurityRuleDirection.INBOUND,
                "name": "rule1",
                "priority": 130,
                "protocol": azure_native.network.SecurityRuleProtocol.ASTERISK,
                "source_address_prefix": "15.26.1.0/24",
                "source_port_range": "*",
            }],
            opts=pulumi.ResourceOptions(parent=self))

        az_virtual_machine = azure_native.compute.VirtualMachine("vpn-virtual-machine",
            hardware_profile={
                "vm_size": azure_native.compute.VirtualMachineSizeTypes.STANDARD_D1_V2,
            },
            network_profile={
                "network_interfaces": [{
                     "id": az_network_interface.id,
                      "primary": True,
                }],
            },
            os_profile={
                "admin_username": "azure",
                "computer_name": "azure-vm",
                "linux_configuration": {
                     "disable_password_authentication": True,
                     "ssh": {
                         "public_keys": [{
                             "key_data": args.ssh_public_key,
                             "path": "/home/azure/.ssh/authorized_keys",
                         }],
                     },
                },
            },
            storage_profile={
                "image_reference": {
                     "offer": "UbuntuServer",
                     "publisher": "Canonical",
                     "sku": "16.04-LTS",
                     "version": "latest",
                },
                "os_disk": {
                    "caching": azure_native.compute.CachingTypes.READ_WRITE,
                    "create_option": azure_native.compute.DiskCreateOptionTypes.FROM_IMAGE,
                    "managed_disk": {
                        "storage_account_type": azure_native.compute.StorageAccountTypes.STANDARD_LRS,
                    },
                    "name": "myVMosdisk",
                },
            },
            resource_group_name=args.resource_group_name,
            vm_name="vpn-vm",
            opts=pulumi.ResourceOptions(parent=self))

        self.vpn_gateway_ip = az_virtual_network_gateway.bgp_settings.bgp_peering_addresses[0].tunnel_ip_addresses[0]
        self.virtual_network_gateway_id = az_virtual_network_gateway.id
