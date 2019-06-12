provider "acme" {
  version    = "~> 1.3"
  server_url = var.acme_server
}

provider "aws" {
  version = "~> 2.13"
  region  = var.aws_region
}

provider "local" {
  version = "~> 1.2"
}

provider "null" {
  version = "~> 2.1"
}

provider "random" {
  version = "~> 2.1"
}

provider "template" {
  version = "~> 2.1"
}

provider "tls" {
  version = "~> 2.0"
}

provider "http" {
  version = "1.1"
}

provider "kubernetes" {
  config_path      = local_file.kubeconfig.filename
  load_config_file = true
}

provider "helm" {
  service_account = "tiller"
  namespace       = "kube-system"
  install_tiller  = true
  tiller_image    = "gcr.io/kubernetes-helm/tiller:v2.14.1"
  kubernetes {
    config_path = local_file.kubeconfig.filename

    # config_path = "${local_file.kubeconfig.filename}"
    load_config_file = true
  }
}

