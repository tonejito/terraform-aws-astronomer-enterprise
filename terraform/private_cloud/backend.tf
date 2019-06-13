terraform {
  required_version = ">= 0.12"
  backend "s3" {
    bucket         = "private-cloud-state"
    key            = "staging/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "private-cloud-state-locking"
  }
}
