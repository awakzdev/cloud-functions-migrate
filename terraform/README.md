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

## Configuration
To migrate Google Cloud Functions, you will need to update the configuration file `function_info.json` to match your Project ID. some fields contain the Project it was fetched from and since our goal is migration we'd like to set this up on a different project.

## Here an example using VSCode

1. Press Ctrl + H using VSCode, A window will popup on the top right corner.
2. Top section should contain the Project name which was used to fetch the JSON, Bottom section should contain the Project ID you'd like to migrate to.
3. Once Step 1 and 2 were done click anywhere in the JSON then hold Ctrl+Alt+Enter to replace all highlighted text to your desired Project ID.

## Deployment Guide
This guide provides step-by-step instructions on how to deploy and destroy infrastructure using Terraform.

## Prerequisites
- Terraform installed on your local machine
- A Google Cloud account
- A Google Cloud SDK installed on your local machine

Steps

1. Authenticate using the following command:
```
gcloud auth login
```

2. Initialize Terraform and download the required plugins
```
terraform init
```
3. Preview the Terraform changes
```
terraform plan
```
4. Applying the changes 
```
terraform apply
```
Once the infrastructure has been created, check the output for the URLs of your Cloud Functions.

To destroy the infrastructure, run the following command:
```
terraform destroy
```
