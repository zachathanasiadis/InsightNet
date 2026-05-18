variable "location" {
  type    = string
  default = "Germany West Central"
}

variable "github_sp_object_id" {
  type        = string
  description = "Microsoft Entra ID service principal object ID for the GitHub Actions OIDC identity, used for RBAC role assignments"
}