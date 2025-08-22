# Exemple d'utilisation du module Terraform RunPod
# Auteur: dr-basalt
# Date: 2025-08-22

terraform {
  required_providers {
    runpod = {
      source  = "runpod/runpod"
      version = "1.0.0"
    }
  }
}

# Variables
variable "runpod_api_key" {
  description = "Clé API RunPod"
  type        = string
  sensitive   = true
}

module "runpod_pods" {
  source = "../../modules/runpod"

  runpod_api_key       = var.runpod_api_key
  pod_count            = 1
  pod_name             = "my-ml-pod"
  image_name           = "runpod/pytorch:2.0.1-py3.10-cuda11.8.0-devel-ubuntu22.04"
  gpu_type_id          = "NVIDIA GeForce RTX 4090"
  gpu_count            = 1
  container_disk_in_gb = 40
  volume_in_gb         = 0
  volume_mount_path    = "/runpod-volume"
  cloud_type           = "ALL"
  min_vcpu_count       = 2
  min_memory_in_gb     = 15
  docker_args          = ""
  ports                = ""
  env                  = {}
  template_id          = ""
  container_name       = "runpod-container"
  start_ssh            = true
  is_public            = false
  shutdown_timeout     = 5
}

output "runpod_pod_ids" {
  description = "IDs des pods RunPod"
  value       = module.runpod_pods.pod_ids
}

output "runpod_pod_names" {
  description = "Noms des pods RunPod"
  value       = module.runpod_pods.pod_names
}

output "runpod_pod_urls" {
  description = "URLs des pods RunPod"
  value       = module.runpod_pods.pod_urls
}