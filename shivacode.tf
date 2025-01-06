variable "github_token" {
  description = "GitHub token for authentication"
  type        = string
  sensitive   = true
}

module "optum_ips" {
  source = "git::https://${var.github_token}@github.com/dojo360/optum-ips.git"
}

 - name: Terraform Plan
        run: terraform plan -var="TF_VAR_namespace=${{ github.event.inputs.TF_VAR_namespace }}"
        env:
          TF_VAR_github_token: ${{ secrets.ICP_GH_TOKEN }}
