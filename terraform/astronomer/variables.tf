variable "db_connection_string" {
  type = "string"
  sensitive = true
}
variable output "tls_key" {
  type = "string"
}
variable "tls_cert" {
  type = "string"
}
variable "kubeconfig_path" {
  type = "string"
}
