module "aws" {
  # source          = "astronomer/astronomer-aws/aws"
  # version         = "1.0.2"
  source          = "./terraform-aws-astronomer-aws"
  deployment_id   = var.deployment_id
  admin_email     = var.email
  route53_domain  = var.route53_domain
  vpc_id          = var.vpc_id
  private_subnets = var.private_subnets
  # It makes the installation easier to leave
  # this public, then just flip it off after
  # everything is deployed.
  # Otherwise, you have to deal with a bastion
  # and proxy settings.
  management_api  = "public"
}

resource "local_file" "kubeconfig" {
  sensitive_content = module.aws.kubeconfig
  filename          = "${path.module}/kubeconfig"
}

# install tiller, which is the server-side component
# of Helm, the Kubernetes package manager
module "system_components" {
  source       = "astronomer/astronomer-system-components/kubernetes"
  version      = "0.0.2"
  enable_istio = "false"
}

module "astronomer" {
  # you can do it like this for development
  # just comment out version, source
  source = "../terraform-kubernetes-astronomer"
  # source  = "astronomer/astronomer/kubernetes"
  # version = "0.1.1"
  cluster_type         = "private"
  base_domain          = module.aws.base_domain
  db_connection_string = module.aws.db_connection_string
  tls_cert             = module.aws.tls_cert
  tls_key              = module.aws.tls_key
  private_load_balancer= false
  local_umbrella_chart = var.local_umbrella_chart
}

