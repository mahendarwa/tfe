resource "null_resource" "my_hello_worl132" {
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

variable "file_path" {
  description = "Path to the input text file"
  type        = string
  default     = "inventory.txt"
}

output "file_contents" {
  value = file(var.file_path)
}
