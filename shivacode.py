Please create an Internal Azure Load Balancer for VM EAC2WIZADW10V in East US 2.

VM details

Subscription: SUB-CORP-EISDEV

Subscription ID: 6462b347-4d8a-43b4-a457-48d34dc93bf0

Resource Group: rg-sub-corp-eisdev-nonprod-use2-app

VNet/Subnet: vnet-corp-eis-dev-use2 / snet-corp-eis-dev-use2-pe

Private IP: 10.83.124.189

Environment: NonProd

Purpose
This VM is being used as an intermediary ADF/SHIR connectivity VM. As discussed, an Internal Load Balancer is needed in front of this VM to support the private connectivity path.

Request
Please configure:

Internal Load Balancer

Frontend private IP

Backend pool with VM EAC2WIZADW10V

Required health probe and LB rule(s)
