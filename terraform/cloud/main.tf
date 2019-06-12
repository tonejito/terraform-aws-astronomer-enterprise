/*
module "system_components" {
  # you can do it like this for development
  # just comment out version, source
  source = "./terraform-kubernetes-astronomer-system-components"
  # source  = "astronomer/astronomer/kubernetes"
  # version = "0.1.1"
  enable_istio         = var.enable_istio
}

module "astronomer" {
  # you can do it like this for development
  # just comment out version, source
  source = "./terraform-kubernetes-astronomer"
  # source  = "astronomer/astronomer/kubernetes"
  # version = "0.1.1"
  base_domain          = module.astronomer_gcp.base_domain
  db_connection_string = module.astronomer_gcp.db_connection_string
  tls_cert             = module.astronomer_gcp.tls_cert
  tls_key              = module.astronomer_gcp.tls_key
  private_load_balancer= false
  local_umbrella_chart = var.local_umbrella_chart
}
*/

module "gcp" {
  # source               = "astronomer/astronomer-gcp/google"
  # version              = "0.2.2"
  source = "./terraform-google-astronomer-gcp"
  admin_emails = [var.email]
  deployment_id        = var.deployment_id
  dns_managed_zone     = var.dns_managed_zone
  project              = var.project
}

resource "local_file" "kubeconfig" {
  sensitive_content = module.astronomer_gcp.kubeconfig
  filename          = "${path.module}/kubeconfig"
}

