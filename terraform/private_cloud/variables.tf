variable "customer_id" {
  description = "A short, letters-only string to identify your deployment, and to prefix some AWS resources. We recommend 'astro'."
  type = string
}

variable "ten_dot_what" {
  description = "10.X.0.0/16 - choose X to not collide with the customer's VPC CIDR. Choose a number (input as a string) between 0-254. Usually a customer will have a VPC cidr like this: 10.Y.0.0/16 . In that case, you just need to choose X != Y. In the case that netmask (/16 part) is a number larger than 16, the same applies. However, in the case that the netmask is a number less than 16, you should use this website http://jodies.de/ipcalc, input the customer's VPC CIDR and make sure that 'HostMin' up to 'HostMax' does not overlap with your chosen CIDR. In the case that their subnet starts with 172 or 192, any number will be fine. This CIDR logic in combination with some other features like peering re-try, automated network connection troubleshooting help, and an onboarding form could enable user self-service for private cloud in the future."
  type = string
}

variable "aws_region" {
  type = string
}

variable "acme_server" {
  description = "Endpoint to use for generating the let's encrypt TLS certificate. Defaults to the production endpoint"
  default = "https://acme-v02.api.letsencrypt.org/directory"
  type = string
}

variable "peer_vpc_id" {
  default = ""
  type = string
}

variable "peer_account_id" {
  default = ""
  type = string
}

variable "route53_domain" {
  default = "steven-development.com"
  type = string
}
