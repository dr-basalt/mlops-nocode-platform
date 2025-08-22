# Sorties pour le module Terraform K3s
# Auteur: dr-basalt
# Date: 2025-08-22

output "master_ips" {
  description = "Adresses IP des nœuds master"
  value       = libvirt_domain.k3s_master[*].network_interface.0.addresses.0
}

output "worker_ips" {
  description = "Adresses IP des nœuds worker"
  value       = libvirt_domain.k3s_worker[*].network_interface.0.addresses.0
}

output "kubeconfig_path" {
  description = "Chemin vers le fichier kubeconfig généré"
  value       = var.kubeconfig_output_path
}

output "cluster_name" {
  description = "Nom du cluster K3s"
  value       = var.cluster_name
}

output "master_count" {
  description = "Nombre de nœuds master"
  value       = var.master_count
}

output "worker_count" {
  description = "Nombre de nœuds worker"
  value       = var.worker_count
}