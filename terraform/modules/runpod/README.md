# Module Terraform pour RunPod

## Description

Ce module Terraform permet de déployer des pods de calcul sur la plateforme cloud RunPod. Il utilise le fournisseur Terraform officiel pour RunPod.

## Fonctionnalités

- Provisionnement de pods de calcul RunPod.
- Configuration automatique via le fournisseur Terraform RunPod.
- Gestion des clés API.

## Structure du module

```
terraform/modules/runpod/
├── main.tf              # Ressources principales du module
├── variables.tf         # Variables d'entrée du module
├── outputs.tf           # Sorties du module
└── README.md            # Documentation du module
```

## Variables

| Nom | Description | Type | Défaut |
|-----|-------------|------|--------|
| `runpod_api_key` | Clé API RunPod | `string` | `` |
| `pod_count` | Nombre de pods à créer | `number` | `1` |
| `pod_name` | Nom des pods | `string` | `"runpod-pod"` |
| `image_name` | Nom de l'image Docker | `string` | `"runpod/pytorch:2.0.1-py3.10-cuda11.8.0-devel-ubuntu22.04"` |
| `gpu_type_id` | ID du type de GPU | `string` | `"NVIDIA GeForce RTX 4090"` |
| `gpu_count` | Nombre de GPU | `number` | `1` |
| `container_disk_in_gb` | Taille du disque du conteneur (en Go) | `number` | `40` |
| `volume_in_gb` | Taille du volume (en Go) | `number` | `0` |
| `volume_mount_path` | Chemin de montage du volume | `string` | `"/runpod-volume"` |
| `cloud_type` | Type de cloud | `string` | `"ALL"` |
| `min_vcpu_count` | Nombre minimum de vCPU | `number` | `2` |
| `min_memory_in_gb` | Mémoire RAM minimum (en Go) | `number` | `15` |
| `docker_args` | Arguments Docker | `string` | `""` |
| `ports` | Ports à exposer | `string` | `""` |
| `env` | Variables d'environnement | `map(string)` | `{}` |
| `template_id` | ID du template | `string` | `""` |
| `container_name` | Nom du conteneur | `string` | `"runpod-container"` |
| `start_ssh` | Démarrer SSH | `bool` | `true` |
| `is_public` | Le pod est-il public ? | `bool` | `false` |
| `shutdown_timeout` | Délai d'arrêt automatique (en secondes) | `number` | `5` |

## Sorties

| Nom | Description |
|-----|-------------|
| `pod_ids` | IDs des pods |
| `pod_names` | Noms des pods |
| `pod_urls` | URLs des pods |
| `pod_ssh_commands` | Commandes SSH pour accéder aux pods |

## Exemple d'utilisation

```hcl
module "runpod_pods" {
  source = "./modules/runpod"

  runpod_api_key       = "your-runpod-api-key"
  pod_count            = 1
  pod_name             = "my-ml-pod"
  image_name           = "runpod/pytorch:2.0.1-py3.10-cuda11.8.0-devel-ubuntu22.04"
  gpu_type_id          = "NVIDIA GeForce RTX 4090"
  gpu_count            = 1
  container_disk_in_gb = 40
  volume_in_gb         = 0
  volume_mount_path    = "/runpod-volume"
  cloud_type           = "ALL"
  min_vcpu_count       = 2
  min_memory_in_gb     = 15
  docker_args          = ""
  ports                = ""
  env                  = {}
  template_id          = ""
  container_name       = "runpod-container"
  start_ssh            = true
  is_public            = false
  shutdown_timeout     = 5
}

output "runpod_pod_ids" {
  value = module.runpod_pods.pod_ids
}

output "runpod_pod_names" {
  value = module.runpod_pods.pod_names
}

output "runpod_pod_urls" {
  value = module.runpod_pods.pod_urls
}
```

## Déploiement

1. Assurez-vous d'avoir Terraform installé.
2. Obtenez votre clé API RunPod.
3. Remplacez les valeurs des variables dans l'exemple par vos propres valeurs.
4. Exécutez `terraform init` pour initialiser le module.
5. Exécutez `terraform plan` pour voir ce qui sera créé.
6. Exécutez `terraform apply` pour déployer les pods.

## Nettoyage

Pour supprimer les pods, exécutez `terraform destroy`.

## Remarques

- Assurez-vous de conserver votre clé API en lieu sûr.
- Le module utilise le fournisseur Terraform officiel pour RunPod.
- Les variables `pod_ids`, `pod_names`, `pod_urls` et `pod_ssh_commands` sont disponibles en sortie pour interagir avec les pods créés.