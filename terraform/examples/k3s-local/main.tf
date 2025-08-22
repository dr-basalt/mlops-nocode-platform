# Exemple d'utilisation du module Terraform K3s
# Auteur: dr-basalt
# Date: 2025-08-22

terraform {
  required_providers {
    libvirt = {
      source  = "dmacvicar/libvirt"
      version = "0.7.0"
    }
  }
}

provider "libvirt" {
  uri = "qemu:///system"
}

module "k3s_cluster" {
  source = "../../modules/k3s"

  cluster_name           = "my-k3s-cluster"
  master_count           = 1
  worker_count           = 2
  master_memory          = 2048
  master_vcpu            = 2
  worker_memory          = 4096
  worker_vcpu            = 2
  master_disk_size       = 21474836480 # 20 Go
  worker_disk_size       = 42949672960 # 40 Go
  storage_pool           = "default"
  network_name           = "default"
  ssh_user               = "ubuntu"
  ssh_private_key_path   = "~/.ssh/id_rsa"
  ssh_authorized_key     = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ..." # Remplacer par votre clé publique
  k3s_version            = "v1.27.1+k3s1"
  k3s_token              = "my-k3s-secret-token"
  kubeconfig_output_path = "./kubeconfig.yaml"
}

output "k3s_master_ips" {
  description = "Adresses IP des nœuds master"
  value       = module.k3s_cluster.master_ips
}

output "k3s_worker_ips" {
  description = "Adresses IP des nœuds worker"
  value       = module.k3s_cluster.worker_ips
}

output "kubeconfig_path" {
  description = "Chemin vers le fichier kubeconfig généré"
  value       = module.k3s_cluster.kubeconfig_path
}