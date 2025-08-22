# Variables pour le module Terraform Vast.ai
# Auteur: dr-basalt
# Date: 2025-08-22

variable "vastai_api_key" {
  description = "Clé API Vast.ai"
  type        = string
  sensitive   = true
}

variable "instance_count" {
  description = "Nombre d'instances à créer"
  type        = number
  default     = 1
}

variable "instance_config" {
  description = "Configuration de l'instance Vast.ai"
  type = object({
    image      = string
    disk_space = number
    gpu_type   = string
    gpu_count  = number
    cpu_count  = number
    ram        = number
    ssh_port   = number
    label      = string
  })
  default = {
    image      = "nvidia/cuda:11.0-devel-ubuntu20.04"
    disk_space = 50
    gpu_type   = "any"
    gpu_count  = 1
    cpu_count  = 4
    ram        = 16
    ssh_port   = 22
    label      = "terraform-instance"
  }
}