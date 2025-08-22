# Sorties pour le module Terraform Exoscale
# Auteur: dr-basalt
# Date: 2025-08-22

output "instance_ips" {
  description = "Adresses IP des instances"
  value       = exoscale_compute.instance[*].ip_address
}

output "instance_ids" {
  description = "IDs des instances"
  value       = exoscale_compute.instance[*].id
}

output "instance_names" {
  description = "Noms des instances"
  value       = exoscale_compute.instance[*].name
}

output "security_group_id" {
  description = "ID du groupe de sécurité"
  value       = length(var.security_groups) > 0 ? var.security_groups[0] : (length(exoscale_security_group.sg) > 0 ? exoscale_security_group.sg[0].id : null)
}