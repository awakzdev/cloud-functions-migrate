resource "google_pubsub_topic" "pub_sub" {
  for_each = toset(local.pubsub_topics)

  name = "${each.key}"

  labels = {
    topic = each.key
  }

  message_retention_duration = "86600s"
}
