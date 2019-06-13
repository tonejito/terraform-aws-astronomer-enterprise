module "aws" {
  # source             = "astronomer/astronomer-aws/aws"
  # version            = "1.0.2"
  source             = "./modules/terraform-aws-astronomer-aws"
  deployment_id      = var.customer_id
  admin_email        = "steven@astronomer.io"
  # route53_domain     = "airflow.run"
  route53_domain     = var.route53_domain
  cluster_type       = "private"
  enable_bastion     = true
  ten_dot_what_cidr  = var.ten_dot_what
  # It makes the installation easier to leave
  # this public, then just flip it off after
  # everything is deployed.
  # Otherwise, you have to deal with a bastion
  # and proxy settings.
  management_api     = "public"

  # peering settings
  peer_account_id = var.peer_account_id
  peer_vpc_id     = var.peer_vpc_id
}

# install tiller, which is the server-side component
# of Helm, the Kubernetes package manager
module "system_components" {
  source       = "astronomer/astronomer-system-components/kubernetes"
  version      = "0.0.3"
  enable_istio = "false"
}

module "astronomer" {
  source                = "astronomer/astronomer/kubernetes"
  version               = "1.0.1"
  cluster_type          = "private"
  private_load_balancer = true
  base_domain           = module.aws.base_domain
  db_connection_string  = module.aws.db_connection_string
  tls_cert              = module.aws.tls_cert
  tls_key               = module.aws.tls_key
}

# write the cname record
data "aws_lambda_invocation" "elb_name" {
  function_name = "${module.aws.elb_lookup_function_name}"
  input = "{}"
}

data "aws_elb" "nginx_elb" {
  name = "${data.aws_lambda_invocation.elb_name.result_map["Name"]}"
}

data "aws_route53_zone" "selected" {
  name = "${var.route53_domain}."
}

resource "aws_route53_record" "astronomer" {
  zone_id = "${data.aws_route53_zone.selected.zone_id}"
  name    = "*.${var.customer_id}.${data.aws_route53_zone.selected.name}"
  type    = "CNAME"
  ttl     = "30"
  records = ["${data.aws_elb.nginx_elb.dns_name}"]
}
