module "aws" {
  source          = "astronomer/astronomer-aws/aws"
  version         = "1.1.2"
  deployment_id   = var.deployment_id
  admin_email     = var.email
  route53_domain  = var.route53_domain
  vpc_id          = var.vpc_id
  private_subnets = var.private_subnets
  enable_bastion  = var.enable_bastion
  cluster_type    = "private"
  # It makes the installation easier to leave
  # this public, then just flip it off after
  # everything is deployed.
  # Otherwise, you have to have some way to
  # access the kube api from terraform:
  # - bastion with proxy
  # - execute terraform from VPC
  management_api = var.management_api
}

# install tiller, which is the server-side component
# of Helm, the Kubernetes package manager
module "system_components" {
  dependencies = [module.aws.depended_on]
  source       = "astronomer/astronomer-system-components/kubernetes"
  version      = "0.0.6"
  # source       = "../terraform-kubernetes-astronomer-system-components"
  enable_istio = "false"
}

module "astronomer" {
  dependencies = [module.system_components.depended_on]
  source       = "astronomer/astronomer/kubernetes"
  version      = "1.0.6"
  # source                = "../terraform-kubernetes-astronomer"
  cluster_type          = "private"
  private_load_balancer = true
  astronomer_version    = "0.9.2"
  base_domain           = module.aws.base_domain
  db_connection_string  = module.aws.db_connection_string
  tls_cert              = module.aws.tls_cert
  tls_key               = module.aws.tls_key
}

