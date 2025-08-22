# Exemple d'utilisation du module Terraform Vast.ai
# Auteur: dr-basalt
# Date: 2025-08-22

terraform {
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "3.2.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "2.4.0"
    }
    template = {
      source  = "hashicorp/template"
      version = "2.2.0"
    }
  }
}

# Variables
variable "vastai_api_key" {
  description = "Clé API Vast.ai"
  type        = string
  sensitive   = true
}

module "vastai_instances" {
  source = "../../modules/vastai"

  vastai_api_key = var.vastai_api_key
  instance_count = 1
  instance_config = {
    image      = "nvidia/cuda:11.0-devel-ubuntu20.04"
    disk_space = 50
    gpu_type   = "RTX_4090"
    gpu_count  = 1
    cpu_count  = 4
    ram        = 16
    ssh_port   = 22
    label      = "my-ml-instance"
  }
}

output "vastai_instance_count" {
  description = "Nombre d'instances Vast.ai créées"
  value       = module.vastai_instances.instance_count
}

output "vastai_instance_config" {
  description = "Configuration utilisée pour les instances Vast.ai"
  value       = module.vastai_instances.instance_config
}