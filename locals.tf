locals {
  astronomer_helm_values = var.astronomer_helm_values != "" ? var.astronomer_helm_values : <<EOF
global:
  baseDomain: ${var.deployment_id}.${var.route53_domain}
  tlsSecret: astronomer-tls
nginx:
  privateLoadBalancer: true
EOF
}
