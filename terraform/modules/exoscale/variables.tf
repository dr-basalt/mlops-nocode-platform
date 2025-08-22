# Variables pour le module Terraform Exoscale
# Auteur: dr-basalt
# Date: 2025-08-22

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

variable "zone" {
  description = "Zone Exoscale"
  type        = string
  default     = "ch-gva-2"
}

variable "instance_count" {
  description = "Nombre d'instances à créer"
  type        = number
  default     = 1
}

variable "instance_name" {
  description = "Nom des instances"
  type        = string
  default     = "exoscale-instance"
}

variable "template" {
  description = "Template d'instance (image)"
  type        = string
  default     = "Linux Ubuntu 22.04 LTS 64-bit"
}

variable "size" {
  description = "Taille de l'instance"
  type        = string
  default     = "Medium"
}

variable "disk_size" {
  description = "Taille du disque (en Go)"
  type        = number
  default     = 50
}

variable "key_pair" {
  description = "Nom de la paire de clés SSH"
  type        = string
}

variable "security_groups" {
  description = "Liste des groupes de sécurité existants"
  type        = list(string)
  default     = []
}

variable "ssh_user" {
  description = "Utilisateur SSH pour se connecter aux instances"
  type        = string
  default     = "ubuntu"
}

variable "ssh_private_key_path" {
  description = "Chemin vers la clé privée SSH"
  type        = string
  default     = "~/.ssh/id_rsa"
}

variable "ssh_authorized_key" {
  description = "Clé publique SSH à ajouter aux instances"
  type        = string
}