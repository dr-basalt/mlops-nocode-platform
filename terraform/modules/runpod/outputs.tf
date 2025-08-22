# Sorties pour le module Terraform RunPod
# Auteur: dr-basalt
# Date: 2025-08-22

output "pod_ids" {
  description = "IDs des pods"
  value       = runpod_pod.pod[*].id
}

output "pod_names" {
  description = "Noms des pods"
  value       = runpod_pod.pod[*].name
}

output "pod_urls" {
  description = "URLs des pods"
  value       = runpod_pod.pod[*].url
}

output "pod_ssh_commands" {
  description = "Commandes SSH pour accéder aux pods"
  value       = runpod_pod.pod[*].ssh_command
}