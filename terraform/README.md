## Terraform 
This is a sample code that will allow iteration using the JSON provided from the python files.

You may create a `terraform.tfvars` file using the following command :
```
cat > terraform.tfvars << EOF
gcp_project = "cc-s2s-vpn-test"
gcp_region = "me-west1"
gcp_functions_region = "europe-west2"
name_prefix = "cloud-function-test"
EOF
```

## Deployment Guide
This guide provides step-by-step instructions on how to deploy and destroy infrastructure using Terraform.

## Prerequisites
- Terraform installed on your local machine
- A Google Cloud account
- A Google Cloud SDK installed on your local machine

Steps

1. Initialize Terraform and download the required plugins
```
terraform init
```
2. Preview the Terraform changes
```
terraform plan
```

3. Applying the changes 
```
terraform apply
```
Once the infrastructure has been created, check the output for the URLs of your Cloud Functions.

To destroy the infrastructure, run the following command:
```
terraform destroy
```