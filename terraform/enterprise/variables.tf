variable "route53_domain" {
  type = string
}

variable "email" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "deployment_id" {
  type = string
}

variable "private_subnets" {
  type = list(string)
}

variable "aws_region" {
  default = "us-east-1"
  type = string
}

variable "acme_server" {
  default = "https://acme-v02.api.letsencrypt.org/directory"
  type = string
}
