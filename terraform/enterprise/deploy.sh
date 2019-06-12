#!/bin/bash

set -xe

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Some dependent AWS modules (EKS, RDS) do not yet support Terraform 0.12,
# So we need to clone the repo, which has patched versions of the dependent
# modules locally installed.
if [ ! -d $DIR/terraform-aws-astronomer-aws ]; then
  git clone https://github.com/astronomer/terraform-aws-astronomer-aws.git
fi

terraform init
terraform apply -var-file=$DIR/terraform.tfvars.sample --target=module.aws
