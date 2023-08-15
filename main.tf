resource "null_resource" "my_hello_worl12" {
  provisioner "local-exec" {
    command = <<-EOT
      # Your local shell command here
      echo "Hello from local command" > local_output.txt
      ls
      hostname > inventory.txt
      cat inventory.txt
    EOT
  }
}

