# API Gateway FastAPI pour la plateforme MLOps No-Code

## Description

Cette API Gateway est le point d'entrée central pour la plateforme MLOps No-Code. Elle fournit une interface RESTful pour gérer les pipelines ML, orchestrer les déploiements et surveiller l'état des services.

## Fonctionnalités

- **Gestion des pipelines**: Création, déploiement et surveillance des pipelines ML.
- **Orchestration**: Intégration avec n8n et Windmill pour l'exécution des workflows.
- **IaC**: Génération de code Terraform pour le provisionnement de l'infrastructure.
- **Sécurité**: Authentification et autorisation pour l'accès à l'API.
- **Monitoring**: Endpoints de santé et de métriques.

## Structure du projet

```
api/fastapi/
├── app/
│   ├── main.py              # Point d'entrée de l'application
│   ├── core/
│   │   └── config.py        # Configuration de l'application
│   ├── models/
│   │   └── __init__.py      # Modèles de données (Pydantic)
│   ├── schemas/
│   │   └── __init__.py      # Schémas de validation
│   ├── routers/
│   │   └── __init__.py      # Routeurs pour les différentes parties de l'API
│   └── __init__.py
├── requirements.txt         # Dépendances Python
└── Dockerfile              # Fichier Docker pour la conteneurisation
```

## Endpoints

### Racine

- `GET /` - Endpoint racine de l'API.

### Santé

- `GET /health` - Endpoint de vérification de l'état de l'API.

### Pipelines

- `POST /pipelines/deploy` - Déploie un pipeline ML.
- `GET /pipelines/{pipeline_id}/status` - Obtient le statut d'un pipeline.

## Dépendances

Les dépendances sont listées dans le fichier `requirements.txt` :

- `fastapi` - Framework web pour Python.
- `uvicorn` - Serveur ASGI pour exécuter l'application FastAPI.
- `pydantic` - Validation de données et sérialisation.
- `pydantic-settings` - Gestion des paramètres de configuration.
- `python-multipart` - Support pour le parsing des données multipart.

## Déploiement

### Avec Docker

1. Construire l'image Docker :
   ```bash
   docker build -t mlops-api-gateway .
   ```

2. Exécuter le conteneur :
   ```bash
   docker run -p 8000:8000 mlops-api-gateway
   ```

### Sans Docker

1. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

2. Exécuter l'application :
   ```bash
   python app/main.py
   ```

## Configuration

L'application peut être configurée via des variables d'environnement. Les paramètres configurables sont définis dans `app/core/config.py`.

## Développement

Pour développer l'API Gateway, vous pouvez exécuter l'application en mode reload :

```bash
uvicorn app.main:app --reload
```

Cela permet de recharger automatiquement l'application lorsque des modifications sont apportées au code source.