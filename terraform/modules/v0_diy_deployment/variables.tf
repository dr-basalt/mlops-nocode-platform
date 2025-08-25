# Variables pour le module Terraform v0.diy deployment
# Auteur: Qwen3 Coder
# Date: 2025-08-25

variable "namespace" {
  description = "Namespace Kubernetes pour le déploiement"
  type        = string
  default     = "v0-diy"
}

variable "image_repository" {
  description = "Repository de l'image Docker pour v0.diy"
  type        = string
  default     = "sujalxplores/v0.diy"
}

variable "image_tag" {
  description = "Tag de l'image Docker pour v0.diy"
  type        = string
  default     = "latest"
}

variable "replicas" {
  description = "Nombre de réplicas pour le déploiement"
  type        = number
  default     = 1
}

variable "service_port" {
  description = "Port du service"
  type        = number
  default     = 3000
}

variable "postgres_host" {
  description = "Hôte PostgreSQL"
  type        = string
  default     = "postgresql"
}

variable "postgres_port" {
  description = "Port PostgreSQL"
  type        = number
  default     = 5432
}

variable "postgres_database" {
  description = "Nom de la base de données PostgreSQL"
  type        = string
  default     = "v0_diy"
}

variable "postgres_user" {
  description = "Utilisateur PostgreSQL"
  type        = string
  default     = "v0_diy"
}

variable "postgres_password" {
  description = "Mot de passe PostgreSQL"
  type        = string
  sensitive   = true
}

variable "redis_host" {
  description = "Hôte Redis"
  type        = string
  default     = "redis"
}

variable "redis_port" {
  description = "Port Redis"
  type        = number
  default     = 6379
}