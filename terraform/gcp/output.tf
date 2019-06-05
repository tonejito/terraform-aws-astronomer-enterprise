output "bastion_socks5_proxy_command" {
  value = "${module.astronomer-gcp.bastion_socks5_proxy_command}"
}

output "db_connection_string" {
  value = "${module.astronomer-gcp.db_connection_string}"
  sensitive = true
}

output "tls_key" {
  value = "${module.astronomer-gcp.tls_key}"
  sensitive = true
}

output "tls_cert" {
  value = "${module.astronomer-gcp.tls_cert}"
  sensitive = true
}

output "kubeconfig_path" {
  value = "${local_file.kubeconfig.filename}"
}
