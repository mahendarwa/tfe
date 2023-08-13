resource "null_resource" "my_hello_world1" {
  provisioner "local-exec" {
    command = "hostname"
  }
}
