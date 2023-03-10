locals {
  functions = jsondecode(file("${path.module}/function_info.json"))
}
