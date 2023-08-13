resource "null_resource" "my_hello_worl1" {
  provisioner "local-exec" {
    command = <<-EOT
      # Your local shell command here
      echo "Hello from local command" > local_output.txt
      ls
    EOT
  }
}

