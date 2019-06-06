module "astronomer" {
  # you can do it like this for development
  # just comment out version, source
  # source  = "./terraform-kubernetes-astronomer"
  source  = "astronomer/astronomer/kubernetes"
  version = "0.0.2"
  admin_email = "${var.email}"
  base_domain = "${module.astronomer_gcp.base_domain}"
  db_connection_string = "${module.astronomer_gcp.db_connection_string}"
  tls_cert = "${module.astronomer_gcp.tls_cert}"
  tls_key = "${module.astronomer_gcp.tls_key}"
  cluster_type = "public"
  enable_istio = "true"
}

module "astronomer_gcp" {
  source  = "astronomer/astronomer-gcp/google"
  version = "0.2.2"
  bastion_admin_emails = ["${var.email}"]
  bastion_user_emails = ["${var.email}"]
  deployment_id = "${var.deployment_id}"
  dns_managed_zone = "${var.dns_managed_zone}"
  project = "${var.project}"
}

resource "local_file" "kubeconfig" {
  sensitive_content = "${module.astronomer_gcp.kubeconfig}"
  filename = "${path.module}/kubeconfig"
}
