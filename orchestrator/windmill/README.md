# Intégration Windmill pour la plateforme MLOps No-Code

## Description

Cette intégration permet d'utiliser Windmill comme plateforme de scripts et d'orchestration pour la plateforme MLOps No-Code. Windmill est une plateforme open-source pour exécuter des scripts, créer des applications et orchestrer des workflows.

## Structure du dossier

```
orchestrator/windmill/
├── docker-compose.yml    # Fichier Docker Compose pour déployer Windmill
├── windmill_data/        # Données persistantes de Windmill (générées automatiquement)
├── postgres_data/        # Données persistantes de PostgreSQL (générées automatiquement)
├── scripts/              # Dossier contenant les scripts Windmill
│   └── test-script.py    # Script de test
└── README.md             # Documentation de l'intégration
```

## Déploiement

### Prérequis

- Docker et Docker Compose installés.

### Démarrer Windmill

1. Naviguez vers le dossier `orchestrator/windmill/` :
   ```bash
   cd orchestrator/windmill/
   ```

2. Démarrez les services avec Docker Compose :
   ```bash
   docker-compose up -d
   ```

3. Accédez à l'interface web de Windmill à l'adresse `http://localhost:8000`.

### Arrêter Windmill

Pour arrêter les services :
```bash
docker-compose down
```

## Scripts

### Script de test

Le fichier `scripts/test-script.py` contient plusieurs fonctions de test :

- `main()`: Fonction de salutation simple.
- `greet_with_time()`: Salue une personne en fonction de la période de la journée.
- `calculate_sum()`: Calcule la somme de deux nombres.
- `process_list()`: Traite une liste d'éléments.

Ces scripts peuvent être importés dans l'interface web de Windmill pour être exécutés.

## Configuration

Le fichier `docker-compose.yml` contient la configuration de Windmill. Vous pouvez modifier les variables d'environnement pour personnaliser le déploiement :

- `DATABASE_URL` : URL de connexion à la base de données PostgreSQL.
- `JWT_SECRET` : Clé secrète pour les jetons JWT (à changer en production).
- `BASE_URL` : URL de base de l'application Windmill.
- `MODE` : Mode de déploiement (standalone par défaut).
- `NUM_WORKERS` : Nombre de workers pour l'exécution des scripts.

## Intégration avec l'API Gateway

L'API Gateway FastAPI peut déclencher des scripts Windmill via l'API REST de Windmill. La configuration de l'URL de l'API Windmill se fait dans le fichier `api/fastapi/app/core/config.py` avec la variable `WINDMILL_API_URL`.

## Sécurité

Pour une utilisation en production, il est recommandé de :

- Changer la clé secrète JWT.
- Utiliser HTTPS.
- Configurer un reverse proxy (comme Nginx) devant Windmill.
- Utiliser un gestionnaire de secrets pour stocker les clés API et les mots de passe.
- Mettre en place des politiques d'accès et des rôles pour les utilisateurs.