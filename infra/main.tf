terraform {
  required_version = ">= 1.4.0"
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}

variable "environment" {
  type        = string
  description = "Deployment environment (dev/staging/prod)."
}

resource "null_resource" "placeholder" {
  triggers = {
    environment = var.environment
  }
}
