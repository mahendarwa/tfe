resource "null_resource" "my_hello_worl13232" {
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

data "local_file" "file_content" {
  depends_on = [null_resource.my_hello_worl13232]

  filename = "inventory.txt"
}

output "captured_value" {
  value = data.local_file.file_content.content
}
