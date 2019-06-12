output "file_content" {
  value = "${data.local_file.test_file.content}"
}
