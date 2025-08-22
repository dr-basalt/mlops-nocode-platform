# Module Terraform pour Exoscale

## Description

Ce module Terraform permet de déployer des instances de calcul sur la plateforme cloud Exoscale. Il provisionne les instances, configure les groupes de sécurité et permet l'accès SSH.

## Fonctionnalités

- Provisionnement d'instances de calcul Exoscale.
- Configuration automatique des groupes de sécurité.
- Support pour les données utilisateur (cloud-init).
- Gestion des paires de clés SSH.

## Structure du module

```
terraform/modules/exoscale/
├── main.tf              # Ressources principales du module
├── variables.tf         # Variables d'entrée du module
├── outputs.tf           # Sorties du module
├── templates/           # Templates pour cloud-init
│   └── user-data.tpl    # Template pour la configuration utilisateur
└── README.md            # Documentation du module
```

## Variables

| Nom | Description | Type | Défaut |
|-----|-------------|------|--------|
| `exoscale_key` | Clé API Exoscale | `string` | `` |
| `exoscale_secret` | Secret API Exoscale | `string` | `` |
| `zone` | Zone Exoscale | `string` | `"ch-gva-2"` |
| `instance_count` | Nombre d'instances à créer | `number` | `1` |
| `instance_name` | Nom des instances | `string` | `"exoscale-instance"` |
| `template` | Template d'instance (image) | `string` | `"Linux Ubuntu 22.04 LTS 64-bit"` |
| `size` | Taille de l'instance | `string` | `"Medium"` |
| `disk_size` | Taille du disque (en Go) | `number` | `50` |
| `key_pair` | Nom de la paire de clés SSH | `string` | `` |
| `security_groups` | Liste des groupes de sécurité existants | `list(string)` | `[]` |
| `ssh_user` | Utilisateur SSH pour se connecter aux instances | `string` | `"ubuntu"` |
| `ssh_private_key_path` | Chemin vers la clé privée SSH | `string` | `"~/.ssh/id_rsa"` |
| `ssh_authorized_key` | Clé publique SSH à ajouter aux instances | `string` | `` |

## Sorties

| Nom | Description |
|-----|-------------|
| `instance_ips` | Adresses IP des instances |
| `instance_ids` | IDs des instances |
| `instance_names` | Noms des instances |
| `security_group_id` | ID du groupe de sécurité |

## Exemple d'utilisation

```hcl
module "exoscale_instances" {
  source = "./modules/exoscale"

  exoscale_key        = "EXOXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
  exoscale_secret     = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
  zone                = "ch-gva-2"
  instance_count      = 2
  instance_name       = "my-ml-instance"
  template            = "Linux Ubuntu 22.04 LTS 64-bit"
  size                = "Medium"
  disk_size           = 50
  key_pair            = "my-keypair"
  ssh_user            = "ubuntu"
  ssh_private_key_path = "~/.ssh/id_rsa"
  ssh_authorized_key   = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ..."
}

output "exoscale_instance_ips" {
  value = module.exoscale_instances.instance_ips
}

output "exoscale_instance_ids" {
  value = module.exoscale_instances.instance_ids
}
```

## Déploiement

1. Assurez-vous d'avoir Terraform installé.
2. Obtenez vos clés API Exoscale.
3. Remplacez les valeurs des variables dans l'exemple par vos propres valeurs.
4. Exécutez `terraform init` pour initialiser le module.
5. Exécutez `terraform plan` pour voir ce qui sera créé.
6. Exécutez `terraform apply` pour déployer les instances.

## Nettoyage

Pour supprimer les instances, exécutez `terraform destroy`.

## Remarques

- Assurez-vous de conserver vos clés API en lieu sûr.
- Le groupe de sécurité par défaut ouvre les ports 22, 80 et 443. Adaptez ces règles selon vos besoins.
- Le template utilisateur (`user-data.tpl`) peut être personnalisé pour installer des logiciels supplémentaires ou configurer l'instance.