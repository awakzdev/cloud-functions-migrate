resource "google_cloudfunctions_function" "secret_test_func" {
  for_each = local.functions
  
  region      = var.gcp_functions_region
  name        = each.key
  description = "${each.key}-Cloud-Function"
  runtime     = "nodejs16"
  entry_point = "catalog_sync" # Entrypoint should be a function in the code

  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.archive.name
  available_memory_mb   = each.value.available_memory_mb
  timeout               = each.value.timeout

  // PRODUCTION ONLY
  # runtime     = each.value.runtime
  # entry_point = each.value.entrypoint

  // Cloud Functions with secret must contains IAM permissions 'roles/secretmanager.secretAccessor' otherwise your function will fail.
  // Cloud Functions of 'event_trigger = Bucket' type are required additional permissions.
  // To view the full list / Troubleshoot visit - https://cloud.google.com/functions/docs/troubleshooting#cloud-console_5
  # service_account_email = google_service_account.cloud_functions_service_account.email

  trigger_http = lookup(each.value, "httpsTrigger", {}) == {} ? null : true
  
  dynamic "event_trigger" {
    for_each = contains(keys(each.value), "eventTrigger") ? [1] : []
    content {
      event_type = each.value.eventTrigger.eventType
      resource   = each.value.eventTrigger.resource

      dynamic "failure_policy" {
        for_each = contains(keys(each.value.eventTrigger.failurePolicy), "retry") ? [1] : []
        content {
          retry = true
        }
      }
    }
  }

  # Environment Variables
  environment_variables = lookup(each.value, "environment_variables", null) != null ? {
    for key, value in each.value.environmentVariables :
    key => value
  } : null

  # Build Environment Variables
  build_environment_variables = lookup(each.value, "build_environment_variables", null) != null ? {
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

  # Setting timeouts for resources
  # Default is 5 but terraform might time out before creation / update is complete.
  timeouts {
    create = "10m"
    update = "10m"
  }
}
