variable "gcp_project" {
  description = "project id"
}

variable "gcp_region" {
  description = "region"
}

variable "name_prefix" {
  description = "naming prefix for resources"
}

variable "gcp_functions_region" {
  description = "Region to deploy the GCP functions. Some newer regions such as me-west1 don't support functions yet so it might be required to use a different region for the functions"
}
