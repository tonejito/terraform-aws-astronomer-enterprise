# Required in path

- Terraform 0.12
- Helm 2.14.0
- Kubectl 1.12.0
- aws-iam-authenticator

- check that at least two subnets, in same region as aws_region and in different AZs
- turn off public endpoint after deployment, or deploy from a host in one of the subnets and you can set it to private in the first place
