# Pulumi Multicloup AWS/Azure

This project designed as IaC solution for deploying virtual network in aws and azure cloud which are linked using VPN.

## Preparing environment

In order to use this scripts you will need to install python version>=3.8 and pulumi. Described installation you may find in official [documentation](https://www.pulumi.com/docs/iac/download-install/)
After pulumi installation you will also need to install azure cli, because they are critical for project workability. Then you will need to provide AWS environment variables with access and secret keys and execute `az login` to give pulumi the ability to work with clouds.

Example environment variables:

```sh
export AWS_ACCESS_KEY_ID="<YOUR_ACCESS_KEY_ID>"
export AWS_SECRET_ACCESS_KEY="<YOUR_SECRET_ACCESS_KEY>"
export AWS_PROFILE="<YOUR_PROFILE_NAME>"
```

For azure you also need to specify `subscriptionId` in Pulumi.dev.yaml.

## Initializing and deploying project

For this step you just need to create new directory, where pulumi will store downloaded scripts from this github repo.
Deployment of this project takes two deploys:

1. Deployment of init virtual networks with VPN gateways
2. Deployment of local VPN gateways in azure for connecting two clouds

For the first step you will need to provide name of your already created azure resource group(resource-group-name) in Pulumi.dev.yaml and ensure that variable `connect-clouds` is set to false.
Here is commands that you need to execute:

1. Initialize new project:
   ```sh
   pulumi new https://github.com/SeredaYehor/pulumi-multicloud.git
   ```
2. Preview changes
   ```sh
   pulumi preview
   ```
3. Deploy infrastructure
   ```sh
   pulumi up
   ```

After deploying first part of infrastructure you will need to pass args into Pulumi.dev.yaml file which will be used in linking azure gateways to AWS VPN.
This args you can retrieve from AWS vpn configuration file. This file can be downloaded from AWS VPN resource which can be located: VPC->Site-to-Site VPN connections->VPN ID link of aws-azure-vpn-connection. Then click on `Download configuration` and provide these options:

> Vendor = Generic
>
> Platform = Generic
>
> Software = Vendor Agnostic
>
> IKE version = ikev2

From downloaded file locate `Pre-Shared Key` under Internet Key Exchange Configuration and `Outside IP Address of Virtual Private Gateway` for each IPSec Tunnels.
Provide these values to Pulumi.dev.yaml file as in this example:

```
vpn-tunnels-shared-keys:
    - name: aws-vpn-tunnel-first
      outside_ip: your-ipsec-tunnel-1-virtual-private-gateway-ip
      shared_key: your-ipsec-tunnel-1-pre-shared-key
    - name: aws-vpn-tunnel-second
      outside_ip: your-ipsec-tunnel-2-virtual-private-gateway-ip
      shared_key: your-ipsec-tunnel-2-pre-shared-key
```

Also do not forget to enable `connect-clouds` option in Pulumi.dev.yaml and after that you may execute:

```sh
pulumi up
```

That`s it. In order to check if vpn connection has been established successfully go to AWS VPN resource and check status of tunnels. There should be green status `Up`.

Delete infrastructure:
```sh
pulumi destroy
```

This project based on this [work](https://kallakruparaju.medium.com/seamless-integration-establishing-private-connectivity-between-aws-and-azure-cloud-environments-39ba5992913f)
More information about pulumi you may find in the [official documentation](https://www.pulumi.com/docs/iac/download-install/)
