# Module Terraform: v0.diy Deployment

Ce module déploie [v0.diy](https://github.com/SujalXplores/v0.diy), un clone open source de v0.dev, sur un cluster Kubernetes.

## Fonctionnalités

- Déploiement de v0.diy avec Next.js
- Configuration de PostgreSQL et Redis
- Service Kubernetes avec Ingress (optionnel)
- Gestion des variables d'environnement

## Prérequis

- Terraform >= 1.0
- Kubernetes >= 1.20
- Helm >= 3.0
- Cluster Kubernetes accessible
- PostgreSQL et Redis déployés ou accessibles

## Utilisation

```hcl
module "v0_diy" {
  source = "./terraform/modules/v0_diy_deployment"

  namespace         = "v0-diy"
  image_repository  = "sujalxplores/v0.diy"
  image_tag         = "latest"
  replicas          = 1
  service_port      = 3000
  
  postgres_host     = "postgresql"
  postgres_port     = 5432
  postgres_database = "v0_diy"
  postgres_user     = "v0_diy"
  postgres_password = "v0_diy_password"
  
  redis_host        = "redis"
  redis_port        = 6379
}
```

## Variables

| Nom | Description | Type | Default | Requis |
|-----|-------------|------|---------|--------|
| namespace | Namespace Kubernetes pour le déploiement | `string` | `"v0-diy"` | non |
| image_repository | Repository de l'image Docker pour v0.diy | `string` | `"sujalxplores/v0.diy"` | non |
| image_tag | Tag de l'image Docker pour v0.diy | `string` | `"latest"` | non |
| replicas | Nombre de réplicas pour le déploiement | `number` | `1` | non |
| service_port | Port du service | `number` | `3000` | non |
| postgres_host | Hôte PostgreSQL | `string` | `"postgresql"` | non |
| postgres_port | Port PostgreSQL | `number` | `5432` | non |
| postgres_database | Nom de la base de données PostgreSQL | `string` | `"v0_diy"` | non |
| postgres_user | Utilisateur PostgreSQL | `string` | `"v0_diy"` | non |
| postgres_password | Mot de passe PostgreSQL | `string` | `""` | oui |
| redis_host | Hôte Redis | `string` | `"redis"` | non |
| redis_port | Port Redis | `number` | `6379` | non |

## Outputs

| Nom | Description |
|-----|-------------|
| namespace | Namespace Kubernetes utilisé pour le déploiement |
| service_name | Nom du service Kubernetes |
| service_port | Port du service Kubernetes |
| ingress_url | URL de l'ingress (si configuré) |

## Exemple complet

Pour un exemple complet d'utilisation de ce module, voir le répertoire `terraform/examples/v0_diy/`.

## Notes

- Ce module suppose que PostgreSQL et Redis sont déjà déployés ou accessibles dans le cluster.
- L'ingress est optionnel et peut être configuré selon les besoins.
- Les variables d'environnement sont configurées pour une instance locale par défaut.