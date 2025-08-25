# Outputs pour le module Terraform v0.diy deployment
# Auteur: Qwen3 Coder
# Date: 2025-08-25

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