variable "content" {
  type = "string"
}
module "fake_module" {
  source  = "./fake_module"
  content = "${var.content}"
}
