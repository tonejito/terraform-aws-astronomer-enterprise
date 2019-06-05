provider "kubernetes" {
  config_path = "${var.kubeconfig_path}"
  load_config_file = true
}

provider "helm" {
  service_account = "tiller"
  debug           = true
  kubernetes {
    config_path = "${var.kubeconfig_path}"
    load_config_file = true
  }
}

module "astronomer" {
  depends_on = ["module.astronomer-gcp"]
  source  = "astronomer/astronomer/kubernetes"
  version = "0.0.1"
  admin_email = "${var.admin_email}"
  base_domain = "${var.base_domain}"
  db_connection_string = "${var.db_connection_string}"
  tls_cert = "${var.tls_cert}"
  tls_key = "${var.tls_key}"
}
