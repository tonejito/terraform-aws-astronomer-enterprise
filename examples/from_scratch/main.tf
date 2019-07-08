variable deployment_id {}

module "astronomer_aws_from_scratch" {
  # To use this module, source like this:
  # source          = "astronomer/astronomer-enterprise/aws"
  # and provide a version:
  # version         = "< supply version >"
  source = "../.."

  # a collision avoidance variable used to separate
  # deployments in the same account
  deployment_id = var.deployment_id

  # provide your email
  email = "steven@astronomer.io"

  # supply your public DNS hosted zone name
  route53_domain = "astronomer-development.com"

  # EKS kubernetes management endpoint
  management_api = "public"

  enable_bastion = true

  # Choose tags for the AWS resources
  tags = {
    "CI" = "true"
  }
}
