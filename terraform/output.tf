output "bastion_socks5_proxy_command" {
  value = "${module.astronomer_gcp.bastion_socks5_proxy_command}"
}

output "proxy_port" {
  value = "${var.proxy_port}"
}
