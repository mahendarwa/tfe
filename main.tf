resource "null_resource" "my_hello_worl1" {
  provisioner "local-exec" {
    command = <<-EOT
      # Your local shell command here
      echo "Hello from local command" > local_output.txt
      ls
    EOT
  }
}

data "local_file" "example" {
 # depends_on = [null_resource.generate_file]  # If needed, specify dependencies
  filename = "local_output.txt"  # Update the path accordingly
}

output "file_content" {
  value = data.local_file.example.content
}
