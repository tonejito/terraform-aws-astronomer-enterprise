variable deployment_id {}

module "astronomer_aws_from_scratch" {
  source  = "../.."
  deployment_id = var.deployment_id
  email = "steven@astronomer.io"
  route53_domain = "astronomer-development.com"
  management_api = "public"
  tags = {
    "CI" = "true"
  }
}
