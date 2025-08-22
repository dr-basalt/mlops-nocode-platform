# Module Terraform pour Vast.ai

## Description

Ce module Terraform permet de déployer des instances de calcul sur la plateforme cloud Vast.ai. Étant donné qu'il n'existe pas de fournisseur Terraform officiel pour Vast.ai, ce module utilise des scripts Python personnalisés pour interagir avec l'API Vast.ai via des ressources `null_resource`.

## Fonctionnalités

- Provisionnement d'instances de calcul Vast.ai.
- Configuration automatique via l'API Vast.ai.
- Gestion des clés API.

## Structure du module

```
terraform/modules/vastai/
├── main.tf              # Ressources principales du module
├── variables.tf         # Variables d'entrée du module
├── outputs.tf           # Sorties du module
├── scripts/             # Scripts pour interagir avec l'API Vast.ai
│   └── vastai_client.py # Client Python pour l'API Vast.ai
├── templates/           # Templates pour la configuration
│   └── instance-config.json.tpl # Template pour la configuration de l'instance
└── README.md            # Documentation du module
```

## Variables

| Nom | Description | Type | Défaut |
|-----|-------------|------|--------|
| `vastai_api_key` | Clé API Vast.ai | `string` | `` |
| `instance_count` | Nombre d'instances à créer | `number` | `1` |
| `instance_config` | Configuration de l'instance Vast.ai | `object` | Voir ci-dessous |

### Configuration de l'instance (`instance_config`)

| Nom | Description | Type | Défaut |
|-----|-------------|------|--------|
| `image` | Image Docker à utiliser | `string` | `"nvidia/cuda:11.0-devel-ubuntu20.04"` |
| `disk_space` | Espace disque (en Go) | `number` | `50` |
| `gpu_type` | Type de GPU | `string` | `"any"` |
| `gpu_count` | Nombre de GPU | `number` | `1` |
| `cpu_count` | Nombre de CPU | `number` | `4` |
| `ram` | Mémoire RAM (en Go) | `number` | `16` |
| `ssh_port` | Port SSH | `number` | `22` |
| `label` | Étiquette de l'instance | `string` | `"terraform-instance"` |

## Sorties

| Nom | Description |
|-----|-------------|
| `instance_count` | Nombre d'instances créées |
| `instance_config` | Configuration utilisée pour les instances |

## Exemple d'utilisation

```hcl
module "vastai_instances" {
  source = "./modules/vastai"

  vastai_api_key = "your-vastai-api-key"
  instance_count = 1
  instance_config = {
    image      = "nvidia/cuda:11.0-devel-ubuntu20.04"
    disk_space = 50
    gpu_type   = "RTX_4090"
    gpu_count  = 1
    cpu_count  = 4
    ram        = 16
    ssh_port   = 22
    label      = "my-ml-instance"
  }
}

output "vastai_instance_count" {
  value = module.vastai_instances.instance_count
}

output "vastai_instance_config" {
  value = module.vastai_instances.instance_config
}
```

## Déploiement

1. Assurez-vous d'avoir Terraform installé.
2. Obtenez votre clé API Vast.ai.
3. Remplacez les valeurs des variables dans l'exemple par vos propres valeurs.
4. Exécutez `terraform init` pour initialiser le module.
5. Exécutez `terraform plan` pour voir ce qui sera créé.
6. Exécutez `terraform apply` pour déployer les instances.

## Nettoyage

Pour supprimer les instances, exécutez `terraform destroy`.

## Remarques

- Ce module dépend de Python 3 et de la bibliothèque `requests`.
- Le script `vastai_client.py` doit être exécutable.
- Assurez-vous de conserver votre clé API en lieu sûr.
- Le module ne gère pas encore la récupération des adresses IP des instances créées. Cette fonctionnalité peut être ajoutée dans une version future.