# Variables pour le module Terraform RunPod
# Auteur: dr-basalt
# Date: 2025-08-22

variable "runpod_api_key" {
  description = "Clé API RunPod"
  type        = string
  sensitive   = true
}

variable "pod_count" {
  description = "Nombre de pods à créer"
  type        = number
  default     = 1
}

variable "pod_name" {
  description = "Nom des pods"
  type        = string
  default     = "runpod-pod"
}

variable "image_name" {
  description = "Nom de l'image Docker"
  type        = string
  default     = "runpod/pytorch:2.0.1-py3.10-cuda11.8.0-devel-ubuntu22.04"
}

variable "gpu_type_id" {
  description = "ID du type de GPU"
  type        = string
  default     = "NVIDIA GeForce RTX 4090"
}

variable "gpu_count" {
  description = "Nombre de GPU"
  type        = number
  default     = 1
}

variable "container_disk_in_gb" {
  description = "Taille du disque du conteneur (en Go)"
  type        = number
  default     = 40
}

variable "volume_in_gb" {
  description = "Taille du volume (en Go)"
  type        = number
  default     = 0
}

variable "volume_mount_path" {
  description = "Chemin de montage du volume"
  type        = string
  default     = "/runpod-volume"
}

variable "cloud_type" {
  description = "Type de cloud"
  type        = string
  default     = "ALL"
}

variable "min_vcpu_count" {
  description = "Nombre minimum de vCPU"
  type        = number
  default     = 2
}

variable "min_memory_in_gb" {
  description = "Mémoire RAM minimum (en Go)"
  type        = number
  default     = 15
}

variable "docker_args" {
  description = "Arguments Docker"
  type        = string
  default     = ""
}

variable "ports" {
  description = "Ports à exposer"
  type        = string
  default     = ""
}

variable "env" {
  description = "Variables d'environnement"
  type        = map(string)
  default     = {}
}

variable "template_id" {
  description = "ID du template"
  type        = string
  default     = ""
}

variable "container_name" {
  description = "Nom du conteneur"
  type        = string
  default     = "runpod-container"
}

variable "start_ssh" {
  description = "Démarrer SSH"
  type        = bool
  default     = true
}

variable "is_public" {
  description = "Le pod est-il public ?"
  type        = bool
  default     = false
}

variable "shutdown_timeout" {
  description = "Délai d'arrêt automatique (en secondes)"
  type        = number
  default     = 5
}