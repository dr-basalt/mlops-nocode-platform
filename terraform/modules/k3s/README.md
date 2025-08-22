# Module Terraform pour K3s

## Description

Ce module Terraform permet de déployer un cluster Kubernetes K3s sur des machines virtuelles libvirt. Il provisionne les nœuds master et worker, installe K3s et génère un fichier kubeconfig pour accéder au cluster.

## Fonctionnalités

- Provisionnement de nœuds master et worker.
- Installation automatique de K3s.
- Génération du fichier kubeconfig.
- Configuration réseau via cloud-init.
- Support pour plusieurs fournisseurs (libvirt, AWS, GCP, etc.).

## Structure du module

```
terraform/modules/k3s/
├── main.tf              # Ressources principales du module
├── variables.tf         # Variables d'entrée du module
├── outputs.tf           # Sorties du module
├── templates/           # Templates pour cloud-init
│   ├── user-data.tpl    # Template pour la configuration utilisateur
│   └── network-config.tpl # Template pour la configuration réseau
└── README.md            # Documentation du module
```

## Variables

| Nom | Description | Type | Défaut |
|-----|-------------|------|--------|
| `cluster_name` | Nom du cluster K3s | `string` | `"k3s-cluster"` |
| `master_count` | Nombre de nœuds master | `number` | `1` |
| `worker_count` | Nombre de nœuds worker | `number` | `2` |
| `master_memory` | Quantité de mémoire pour les nœuds master (en Mo) | `number` | `2048` |
| `master_vcpu` | Nombre de vCPU pour les nœuds master | `number` | `2` |
| `worker_memory` | Quantité de mémoire pour les nœuds worker (en Mo) | `number` | `4096` |
| `worker_vcpu` | Nombre de vCPU pour les nœuds worker | `number` | `2` |
| `master_disk_size` | Taille du disque pour les nœuds master (en octets) | `number` | `21474836480` |
| `worker_disk_size` | Taille du disque pour les nœuds worker (en octets) | `number` | `42949672960` |
| `storage_pool` | Nom du pool de stockage libvirt | `string` | `"default"` |
| `network_name` | Nom du réseau libvirt | `string` | `"default"` |
| `ssh_user` | Utilisateur SSH pour se connecter aux machines | `string` | `"ubuntu"` |
| `ssh_private_key_path` | Chemin vers la clé privée SSH | `string` | `"~/.ssh/id_rsa"` |
| `ssh_authorized_key` | Clé publique SSH à ajouter aux machines | `string` | `` |
| `k3s_version` | Version de K3s à installer | `string` | `"v1.27.1+k3s1"` |
| `k3s_token` | Jeton pour l'authentification du cluster K3s | `string` | `"my-k3s-secret-token"` |
| `kubeconfig_output_path` | Chemin où sauvegarder le fichier kubeconfig | `string` | `"./kubeconfig.yaml"` |

## Sorties

| Nom | Description |
|-----|-------------|
| `master_ips` | Adresses IP des nœuds master |
| `worker_ips` | Adresses IP des nœuds worker |
| `kubeconfig_path` | Chemin vers le fichier kubeconfig généré |
| `cluster_name` | Nom du cluster K3s |
| `master_count` | Nombre de nœuds master |
| `worker_count` | Nombre de nœuds worker |

## Exemple d'utilisation

```hcl
module "k3s_cluster" {
  source = "./modules/k3s"

  cluster_name           = "my-k3s-cluster"
  master_count           = 1
  worker_count           = 2
  ssh_authorized_key     = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ..."
  k3s_token              = "my-k3s-secret-token"
  kubeconfig_output_path = "./kubeconfig.yaml"
}

output "k3s_master_ips" {
  value = module.k3s_cluster.master_ips
}

output "k3s_worker_ips" {
  value = module.k3s_cluster.worker_ips
}

output "kubeconfig_path" {
  value = module.k3s_cluster.kubeconfig_path
}
```

## Déploiement

1. Assurez-vous d'avoir Terraform installé.
2. Configurez votre fournisseur libvirt (ou un autre fournisseur).
3. Remplacez la clé SSH dans l'exemple par votre clé publique.
4. Exécutez `terraform init` pour initialiser le module.
5. Exécutez `terraform plan` pour voir ce qui sera créé.
6. Exécutez `terraform apply` pour déployer le cluster.

## Nettoyage

Pour supprimer le cluster, exécutez `terraform destroy`.

## Remarques

- Ce module est conçu pour fonctionner avec libvirt. Pour d'autres fournisseurs, vous devrez adapter les ressources.
- Assurez-vous d'avoir suffisamment de ressources système pour exécuter le cluster.
- Le fichier kubeconfig généré peut être utilisé avec `kubectl` pour interagir avec le cluster.