variable "project" {
  type = "string"
}
variable "region" {
  type = "string"
}
variable "zone" {
  type = "string"
}
variable "dns_managed_zone" {
  type = "string"
}
variable "acme_server" {
  type = "string"
}
variable "bastion_admin_emails" {
  type = "list"
}
variable "bastion_user_emails" {
  type = "list"
}
variable "deployment_id" {
  type = "string"
}
variable "write_kubeconfig_to" {
  type = "string"
}
