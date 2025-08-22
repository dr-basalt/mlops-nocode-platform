# Intégration n8n pour la plateforme MLOps No-Code

## Description

Cette intégration permet d'utiliser n8n comme orchestrateur de workflows pour la plateforme MLOps No-Code. n8n est un workflow automation tool open-source qui permet de connecter différents services et d'automatiser des tâches complexes.

## Structure du dossier

```
orchestrator/n8n/
├── docker-compose.yml    # Fichier Docker Compose pour déployer n8n
├── n8n_data/             # Données persistantes de n8n (générées automatiquement)
├── workflows/            # Dossier contenant les workflows n8n
│   └── test-workflow.json # Workflow de test
└── README.md             # Documentation de l'intégration
```

## Déploiement

### Prérequis

- Docker et Docker Compose installés.

### Démarrer n8n

1. Naviguez vers le dossier `orchestrator/n8n/` :
   ```bash
   cd orchestrator/n8n/
   ```

2. Démarrez les services avec Docker Compose :
   ```bash
   docker-compose up -d
   ```

3. Accédez à l'interface web de n8n à l'adresse `http://localhost:5678`.

### Arrêter n8n

Pour arrêter les services :
```bash
docker-compose down
```

## Workflows

### Workflow de test

Le fichier `workflows/test-workflow.json` contient un workflow de test simple qui :

1. Démarre le workflow.
2. Effectue une requête HTTP GET vers `https://httpbin.org/get`.
3. Affiche l'URL de la réponse dans le nœud Debug.

Ce workflow peut être importé dans l'interface web de n8n pour être exécuté.

## Configuration

Le fichier `docker-compose.yml` contient la configuration de n8n. Vous pouvez modifier les variables d'environnement pour personnaliser le déploiement :

- `N8N_PORT` : Port d'écoute de n8n (par défaut 5678).
- `N8N_HOST` : Hôte sur lequel n8n écoute (par défaut localhost).
- `GENERIC_TIMEZONE` : Fuseau horaire (par défaut Europe/Paris).
- `DB_TYPE` : Type de base de données (sqlite par défaut, peut être postgres).
- `N8N_BASIC_AUTH_ACTIVE` : Activation de l'authentification basique (false par défaut).

## Intégration avec l'API Gateway

L'API Gateway FastAPI peut déclencher des workflows n8n via l'API REST de n8n. La configuration de l'URL de l'API n8n se fait dans le fichier `api/fastapi/app/core/config.py` avec la variable `N8N_API_URL`.

## Sécurité

Pour une utilisation en production, il est recommandé de :

- Activer l'authentification basique ou l'authentification par jeton.
- Utiliser HTTPS.
- Configurer un reverse proxy (comme Nginx) devant n8n.
- Utiliser une base de données PostgreSQL au lieu de SQLite.