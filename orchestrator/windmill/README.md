# Interfaces Windmill pour les Playbooks

## Description

Ce dossier contient les interfaces Windmill pour la gestion des playbooks et l'assemblage de pipelines. Windmill est utilisé comme plateforme no-code pour orchestrer les déploiements ML.

## Structure

- `apps/` : Applications Windmill.
- `scripts/` : Scripts Windmill.
- `flows/` : Flows Windmill.

## Applications

### ML Pipeline Builder (`apps/ml_pipeline_builder.json`)

Application pour construire et déployer des pipelines ML de manière visuelle.

**Composants :**

1.  **Configuration du Pipeline** : Formulaire pour saisir le nom, la description et la plateforme cible du pipeline.
2.  **Éditeur de Nodes** : Éditeur visuel pour assembler les nodes du pipeline.
    *   **Source de Données** : Node pour définir la source des données (S3, Base de Données, API).
    *   **Prétraitement** : Node pour définir les opérations de prétraitement des données.
    *   **Modèle** : Node pour définir le modèle ML (Entraînement, Fine-tuning, Inférence).
    *   **Déploiement** : Node pour définir le type de déploiement (Point de terminaison API, Traitement par lots).

**Actions :**

*   **Déployer le Pipeline** : Action pour déclencher le déploiement du pipeline configuré.

## Scripts

### Déploiement de Pipeline (`scripts/deploy_pipeline.py`)

Script Python pour déployer un pipeline ML.

**Fonctionnalités :**

1.  Validation de la configuration du pipeline.
2.  Génération du code Terraform pour l'infrastructure.
3.  Déploiement de l'infrastructure via Terraform.
4.  Retour d'un message de succès ou d'erreur.

## Flows

### Déploiement de Pipeline ML (`flows/ml_pipeline_deployment.json`)

Flow pour orchestrer le déploiement d'un pipeline ML.

**Étapes :**

1.  **Validation de la Configuration** : Validation de la configuration du pipeline.
2.  **Génération de Terraform** : Génération du code Terraform.
3.  **Déploiement de l'Infrastructure** : Déploiement de l'infrastructure.
4.  **Déploiement du Pipeline** : Déploiement du pipeline.
5.  **Notification d'Achèvement** : Notification de l'achèvement du déploiement.

## Utilisation

1.  **Démarrer Windmill :**

    ```bash
    docker-compose up -d
    ```

2.  **Importer les Applications, Scripts et Flows :**

    *   Importer `apps/ml_pipeline_builder.json` dans Windmill.
    *   Importer les scripts de `scripts/` dans Windmill.
    *   Importer `flows/ml_pipeline_deployment.json` dans Windmill.

3.  **Utiliser l'Application :**

    *   Accéder à l'application "ML Pipeline Builder" dans l'interface Windmill.
    *   Configurer le pipeline en remplissant le formulaire et en assemblant les nodes.
    *   Cliquer sur "Déployer le Pipeline" pour lancer le déploiement.

## Développement

Pour modifier les applications, scripts ou flows :

1.  Éditer les fichiers JSON/Python dans `apps/`, `scripts/` ou `flows/`.
2.  Réimporter les fichiers modifiés dans Windmill.

## TODO

*   Ajouter plus d'exemples d'applications, de scripts et de flows.
*   Implémenter la gestion des versions des playbooks.
*   Implémenter l'assemblage fractal de pipelines.