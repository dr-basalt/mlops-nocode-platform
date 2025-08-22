# Variables pour le module Terraform K3s
# Auteur: dr-basalt
# Date: 2025-08-22

variable "cluster_name" {
  description = "Nom du cluster K3s"
  type        = string
  default     = "k3s-cluster"
}

variable "master_count" {
  description = "Nombre de nœuds master"
  type        = number
  default     = 1
}

variable "worker_count" {
  description = "Nombre de nœuds worker"
  type        = number
  default     = 2
}

variable "master_memory" {
  description = "Quantité de mémoire pour les nœuds master (en Mo)"
  type        = number
  default     = 2048
}

variable "master_vcpu" {
  description = "Nombre de vCPU pour les nœuds master"
  type        = number
  default     = 2
}

variable "worker_memory" {
  description = "Quantité de mémoire pour les nœuds worker (en Mo)"
  type        = number
  default     = 4096
}

variable "worker_vcpu" {
  description = "Nombre de vCPU pour les nœuds worker"
  type        = number
  default     = 2
}

variable "master_disk_size" {
  description = "Taille du disque pour les nœuds master (en octets)"
  type        = number
  default     = 21474836480 # 20 Go
}

variable "worker_disk_size" {
  description = "Taille du disque pour les nœuds worker (en octets)"
  type        = number
  default     = 42949672960 # 40 Go
}

variable "storage_pool" {
  description = "Nom du pool de stockage libvirt"
  type        = string
  default     = "default"
}

variable "network_name" {
  description = "Nom du réseau libvirt"
  type        = string
  default     = "default"
}

variable "ssh_user" {
  description = "Utilisateur SSH pour se connecter aux machines"
  type        = string
  default     = "ubuntu"
}

variable "ssh_private_key_path" {
  description = "Chemin vers la clé privée SSH"
  type        = string
  default     = "~/.ssh/id_rsa"
}

variable "ssh_authorized_key" {
  description = "Clé publique SSH à ajouter aux machines"
  type        = string
}

variable "k3s_version" {
  description = "Version de K3s à installer"
  type        = string
  default     = "v1.27.1+k3s1"
}

variable "k3s_token" {
  description = "Jeton pour l'authentification du cluster K3s"
  type        = string
  default     = "my-k3s-secret-token"
}

variable "kubeconfig_output_path" {
  description = "Chemin où sauvegarder le fichier kubeconfig"
  type        = string
  default     = "./kubeconfig.yaml"
}