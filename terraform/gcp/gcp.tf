provider "google" {
  version = "~> 2.7"
  region  = "${var.region}"
  project = "${var.project}"
  zone    = "${var.zone}"
}

provider "google-beta" {
  version = "~> 2.7"
  region  = "${var.region}"
  project = "${var.project}"
  zone    = "${var.zone}"
}

provider "acme" {
  version = "~> 1.3"
  server_url = "${var.acme_server}"
}

provider "random" {
  version = "~> 2.1"
}

provider "tls" {
  version = "~> 2.0"
}

module "astronomer-gcp" {
  source  = "astronomer/astronomer-gcp/google"
  version = "0.1.1"
  bastion_admin_emails = ["${var.bastion_admin_emails}"]
  bastion_user_emails = ["${var.bastion_user_emails}"]
  deployment_id = "${var.deployment_id}"
  dns_managed_zone = "${var.dns_managed_zone}"
  project = "${var.project}"
}

resource "local_file" "kubeconfig" {
  sensitive_content = "${module.astronomer-gcp.kubeconfig}"
  filename = "${var.write_kubeconfig_to}"
}
