# Sorties pour le module Terraform Vast.ai
# Auteur: dr-basalt
# Date: 2025-08-22

output "instance_count" {
  description = "Nombre d'instances créées"
  value       = var.instance_count
}

output "instance_config" {
  description = "Configuration utilisée pour les instances"
  value       = var.instance_config
}