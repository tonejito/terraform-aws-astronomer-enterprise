# Required in path

- [Terraform 0.12](https://www.terraform.io/upgrade-guides/0-12.html)
- [Helm 2.14.0](https://helm.sh/docs/using_helm/)
- [Kubectl 1.12.0](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [aws-iam-authenticator](https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html)

- check that at least two subnets, in same region as aws_region and in different AZs
- turn off public endpoint after deployment, or deploy from a host in one of the subnets and you can set it to private in the first place
