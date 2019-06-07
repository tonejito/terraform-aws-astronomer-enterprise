resource "local_file" "test_file" {
  content = "${var.content}"
  filename = "${path.module}/test_file.txt"
}

data "local_file" "test_file" {
    filename = "${local_file.test_file.filename}"
}
