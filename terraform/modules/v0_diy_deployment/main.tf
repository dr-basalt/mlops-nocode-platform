# Module Terraform pour le déploiement de v0.diy
# Auteur: Qwen3 Coder
# Date: 2025-08-25

terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.20.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.9.0"
    }
  }
}

# Variables d'entrée
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

# Création du namespace
resource "kubernetes_namespace" "v0_diy" {
  metadata {
    name = var.namespace
  }
}

# Déploiement de v0.diy
resource "kubernetes_deployment" "v0_diy" {
  metadata {
    name      = "v0-diy"
    namespace = kubernetes_namespace.v0_diy.metadata[0].name
    labels = {
      app = "v0-diy"
    }
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        app = "v0-diy"
      }
    }

    template {
      metadata {
        labels = {
          app = "v0-diy"
        }
      }

      spec {
        container {
          image = "${var.image_repository}:${var.image_tag}"
          name  = "v0-diy"

          port {
            container_port = var.service_port
          }

          env {
            name  = "DATABASE_URL"
            value = "postgresql://${var.postgres_user}:${var.postgres_password}@${var.postgres_host}:${var.postgres_port}/${var.postgres_database}"
          }

          env {
            name  = "REDIS_URL"
            value = "redis://${var.redis_host}:${var.redis_port}"
          }

          env {
            name  = "NEXT_PUBLIC_SITE_URL"
            value = "http://localhost:3000"
          }

          resources {
            limits = {
              cpu    = "1"
              memory = "2Gi"
            }
            requests = {
              cpu    = "500m"
              memory = "1Gi"
            }
          }
        }
      }
    }
  }
}

# Service pour v0.diy
resource "kubernetes_service" "v0_diy" {
  metadata {
    name      = "v0-diy"
    namespace = kubernetes_namespace.v0_diy.metadata[0].name
  }

  spec {
    selector = {
      app = "v0-diy"
    }

    port {
      port        = var.service_port
      target_port = var.service_port
    }

    type = "ClusterIP"
  }
}

# Ingress pour v0.diy (optionnel)
resource "kubernetes_ingress_v1" "v0_diy" {
  metadata {
    name      = "v0-diy"
    namespace = kubernetes_namespace.v0_diy.metadata[0].name
    annotations = {
      "nginx.ingress.kubernetes.io/rewrite-target" = "/"
    }
  }

  spec {
    rule {
      http {
        path {
          path      = "/"
          path_type = "Prefix"

          backend {
            service {
              name = kubernetes_service.v0_diy.metadata[0].name
              port {
                number = var.service_port
              }
            }
          }
        }
      }
    }
  }
}

# Outputs
output "namespace" {
  value = kubernetes_namespace.v0_diy.metadata[0].name
}

output "service_name" {
  value = kubernetes_service.v0_diy.metadata[0].name
}

output "service_port" {
  value = kubernetes_service.v0_diy.spec[0].port[0].port
}

output "ingress_url" {
  value = "http://${kubernetes_ingress_v1.v0_diy.spec[0].rule[0].host}"
}