# Module Terraform pour déployer des pods RunPod
# Auteur: dr-basalt
# Date: 2025-08-22

# Fournisseur RunPod
provider "runpod" {
  api_key = var.runpod_api_key
}

# Ressource pour créer un pod RunPod
resource "runpod_pod" "pod" {
  count = var.pod_count

  name            = "${var.pod_name}-${count.index}"
  image_name      = var.image_name
  gpu_type_id     = var.gpu_type_id
  gpu_count       = var.gpu_count
  container_disk_in_gb = var.container_disk_in_gb
  volume_in_gb    = var.volume_in_gb
  volume_mount_path = var.volume_mount_path
  cloud_type      = var.cloud_type
  min_vcpu_count  = var.min_vcpu_count
  min_memory_in_gb = var.min_memory_in_gb
  docker_args     = var.docker_args
  ports           = var.ports
  env = var.env
  template_id     = var.template_id

  # Configuration du conteneur
  container_name  = var.container_name
  start_ssh       = var.start_ssh

  # Configuration du réseau
  is_public       = var.is_public

  # Configuration de l'arrêt automatique
  shutdown_timeout = var.shutdown_timeout
}