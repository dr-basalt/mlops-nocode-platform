# Exemple d'utilisation du module Terraform Exoscale
# Auteur: dr-basalt
# Date: 2025-08-22

terraform {
  required_providers {
    exoscale = {
      source  = "exoscale/exoscale"
      version = "0.50.0"
    }
  }
}

# Fournisseur Exoscale
provider "exoscale" {
  key    = var.exoscale_key
  secret = var.exoscale_secret
}

# Variables
variable "exoscale_key" {
  description = "Clé API Exoscale"
  type        = string
  sensitive   = true
}

variable "exoscale_secret" {
  description = "Secret API Exoscale"
  type        = string
  sensitive   = true
}

module "exoscale_instances" {
  source = "../../modules/exoscale"

  exoscale_key        = var.exoscale_key
  exoscale_secret     = var.exoscale_secret
  zone                = "ch-gva-2"
  instance_count      = 2
  instance_name       = "my-ml-instance"
  template            = "Linux Ubuntu 22.04 LTS 64-bit"
  size                = "Medium"
  disk_size           = 50
  key_pair            = "my-keypair" # Remplacer par votre paire de clés
  ssh_user            = "ubuntu"
  ssh_private_key_path = "~/.ssh/id_rsa"
  ssh_authorized_key   = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ..." # Remplacer par votre clé publique
}

output "exoscale_instance_ips" {
  description = "Adresses IP des instances Exoscale"
  value       = module.exoscale_instances.instance_ips
}

output "exoscale_instance_ids" {
  description = "IDs des instances Exoscale"
  value       = module.exoscale_instances.instance_ids
}