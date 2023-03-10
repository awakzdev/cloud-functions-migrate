//////////////////////////////

# Providers
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.49.0"
    }
  }
  required_version = ">= 0.14"
}

provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}

//////////////////////////////

# Variables 
variable "gcp_project" {
  description = "project id"
}

variable "gcp_region" {
  description = "region"
}

variable "name_prefix" {
  description = "naming prefix for resources"
}

//////////////////////////////

# Locals
locals {
  functions = jsondecode(file("${path.module}/function_info.json"))
  pubsub_topics = jsondecode(file("${path.module}/pubsub_topics.json"))
}

//////////////////////////////

# Pub/Sub topic resource
resource "google_pubsub_topic" "pub_sub" {
  for_each = toset(local.pubsub_topics)

  name = "${var.name_prefix}-${each.key}"

  labels = {
    topic = each.key
  }

  message_retention_duration = "86600s"
}

//////////////////////////////

# Storage bucket resource
resource "google_storage_bucket" "function_bucket" {
  name     = "${var.name_prefix}-sync-cloud-functions"
  location = var.function_storage_location
}

resource "google_storage_bucket_object" "archive" {
  name   = "bootstrap_nodejs_function.zip"
  bucket = google_storage_bucket.function_bucket.name
  source = "./bootstrap_nodejs_function.zip"
}

//////////////////////////////

# Cloud Function resource 
resource "google_cloudfunctions_function" "secret_test_func" {
  for_each = local.functions

  name        = each.key
  description = "Test - ${each.key}"
  runtime     = "nodejs16"
  region      = var.gcp_functions_region
  entry_point = "catalog_sync" # Entrypoint should be a function in the code

  # vpc_connector = google_vpc_access_connector.serverless_vpc.id
  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.archive.name

  available_memory_mb   = each.value.available_memory_mb
  timeout               = each.value.timeout
  trigger_http = lookup(each.value, "httpTrigger", null) == null ? null : true
  
  dynamic "event_trigger" {
    for_each   = lookup(each.value, "eventTrigger", {})
    content {
      event_type = event_trigger.value.eventType
      resource   = event_trigger.value.resource
    }
  }

  # Environment Variables
  environment_variables = lookup(each.value, "environment_variables", null) != null ? {
    for key, value in each.value.environmentVariables :
    key => value
  } : null

  # Build Environment Variables
  build_environment_variables = lookup(each.value, "build_environment_variables", null) != null ?{
    for key, value in each.value.buildEnvironmentVariables :
    key => value
  } : null

  # Secrets Exposed as an environment variable
  dynamic "secret_environment_variables" {
    for_each = lookup(each.value.secrets, "secretEnvironmentVariables", [])
    content {
      key = secret_environment_variables.value.key
      project_id = secret_environment_variables.value.projectId
      secret = secret_environment_variables.value.secret
      version = secret_environment_variables.value.secret
    }
  }

  # Secrets Mounted as a volume
  dynamic "secret_volumes" {
    for_each = lookup(each.value.secrets, "secretVolumes", [])
    content {
      mount_path = secret_volumes.value.mountPath
      secret     = secret_volumes.value.secret
      project_id = secret_volumes.value.projectId

      dynamic "versions" {
        for_each = secret_volumes.value.versions
        content {
          path    = versions.value.path
          version = versions.value.version
        }
      }
    }
  }

  lifecycle {
    ignore_changes = [
      source_archive_bucket,source_archive_object,labels["deployment-tool"]
    ]
  }
}
