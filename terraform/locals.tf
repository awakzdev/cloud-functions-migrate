locals {
  # A list of all available functions
  functions = jsondecode(file("${path.module}/function_info.json"))
  
  # A list of all available pub\sub topics
  pubsub_topics = jsondecode(file("${path.module}/pubsub_topics.json"))
}