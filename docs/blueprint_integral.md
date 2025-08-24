# Blueprint Intégral de la Plateforme MLOps No-Code Platform

## 1. Résumé Exécutif

La plateforme MLOps No-Code Platform est une solution complète pour déployer, gérer et surveiller des pipelines ML de manière no-code sur différentes plateformes cloud. Elle combine des outils open-source (Windmill, n8n, Terraform, K3s, LiteLLM, Prometheus, Grafana) avec une API Gateway personnalisée pour offrir une expérience unifiée de développement et d'orchestration ML.

## 2. Architecture Globale

```mermaid
graph TD
    A[Interface Utilisateur] --> B[API Gateway FastAPI]
    B --> C[Orchestrateur de Workflows n8n]
    B --> D[Interface No-Code Windmill]
    C --> E[Moteur d'Exécution Windmill]
    C --> F[Générateur d'IaC Terraform]
    F --> G[Cluster K3s Local]
    F --> H[Exoscale API]
    F --> I[Vast.ai API]
    F --> J[RunPod API]
    G --> K[Workloads ML]
    H --> K
    I --> K
    J --> K
    K --> L[LiteLLM Proxy]
    L --> M[Modèles LLM (Ollama, vLLM, etc.)]
    C --> N[Catalogue de Playbooks]
    N --> O[Versioning Git]
    O --> P[Assemblage de Pipelines]
    P --> Q[Assemblage de Meta-Pipelines]
    K --> R[Monitoring Prometheus/Grafana]
    R --> S[Tableau de Bord]
    A --> T[Interface de Chatbot (Future)]
```

## 3. Composants Principaux

### 3.1 API Gateway FastAPI

**Responsabilités :**
- Point d'entrée unique pour toutes les requêtes.
- Validation des configurations de pipeline.
- Orchestration des déploiements.
- Suivi des statuts de déploiement.

**Technologies :**
- FastAPI (Python)
- Pydantic pour la validation
- Uvicorn comme serveur ASGI

**Endpoints Principaux :**
- `POST /pipelines/deploy` : Déploie un pipeline ML.
- `GET /pipelines/{pipeline_id}/status` : Obtient le statut d'un pipeline.
- `GET /health` : Vérification de l'état de l'API.

**Fichier :** `api/fastapi/app/main.py`

### 3.2 Interface No-Code Windmill

**Responsabilités :**
- Interface visuelle pour configurer les pipelines ML.
- Éditeur de nodes pour assembler les composants.
- Gestion des applications, scripts et flows.
- Intégration avec l'API Gateway.

**Technologies :**
- Windmill (plateforme no-code open-source)
- Docker Compose pour le déploiement

**Composants :**
- **Application ML Pipeline Builder** : Interface pour construire et déployer des pipelines ML.
- **Scripts** : Scripts Python pour la validation, la génération de Terraform et le déploiement.
- **Flows** : Workflows d'orchestration.

**Fichiers :**
- `orchestrator/windmill/apps/ml_pipeline_builder.json`
- `orchestrator/windmill/scripts/`
- `orchestrator/windmill/flows/ml_pipeline_deployment.json`

### 3.3 Orchestrateur de Workflows n8n

**Responsabilités :**
- Exécution des workflows d'orchestration.
- Coordination entre les différents composants.
- Intégration avec l'API Gateway et Windmill.

**Technologies :**
- n8n (orchestrateur de workflows open-source)
- Docker Compose pour le déploiement

**Fichier :** `orchestrator/n8n/docker-compose.yml`

### 3.4 Générateur d'IaC Terraform

**Responsabilités :**
- Génération de code Terraform pour le provisionnement de l'infrastructure.
- Support pour plusieurs plateformes cloud.
- Intégration avec l'orchestrateur.

**Technologies :**
- Terraform (HashiCorp)
- Modules Terraform personnalisés

**Modules :**
- **K3s Local** : Déploiement d'un cluster K3s local.
- **Exoscale** : Provisionnement d'instances Exoscale.
- **Vast.ai** : Location de GPUs via Vast.ai (via API).
- **RunPod** : Provisionnement de pods RunPod.

**Fichiers :**
- `terraform/modules/k3s/`
- `terraform/modules/exoscale/`
- `terraform/modules/vastai/`
- `terraform/modules/runpod/`

### 3.5 Déploiement LiteLLM

**Responsabilités :**
- Déploiement d'un proxy LiteLLM pour exposer les modèles LLM.
- Routage intelligent vers différents backends (Ollama, vLLM, etc.).
- Intégration avec les pipelines ML.

**Technologies :**
- LiteLLM (proxy LLM open-source)
- Kubernetes (manifests)

**Fichier :** `k8s/manifests/litellm/litellm-proxy.yaml`

### 3.6 Monitoring Prometheus/Grafana

**Responsabilités :**
- Surveillance des déploiements ML.
- Collecte de métriques de performance.
- Visualisation des données.

**Technologies :**
- Prometheus (système de monitoring)
- Grafana (plateforme de visualisation)
- Docker Compose pour le déploiement

**Fichiers :**
- `monitoring/prometheus/prometheus.yml`
- `monitoring/grafana/dashboards/`

### 3.7 Script de Throttling CPU

**Responsabilités :**
- Contrôle de la charge CPU et du load average pour éviter les limitations.
- Configuration via des variables d'environnement.
- Logging des événements.

**Technologies :**
- Python
- psutil (librairie de monitoring système)

**Fichier :** `cpu_throttler.py`

## 4. Interfaces et Flux de Données

### 4.1 Interface Utilisateur Principale

L'interface principale est l'application Windmill "ML Pipeline Builder" qui permet de :
1. Configurer un pipeline ML via un formulaire.
2. Assembler les nodes du pipeline visuellement.
3. Déployer le pipeline via un bouton.

### 4.2 Flux de Déploiement d'un Pipeline

1. L'utilisateur configure un pipeline dans Windmill.
2. Windmill déclenche un flow d'orchestration.
3. Le flow appelle l'API Gateway pour valider la configuration.
4. L'API Gateway génère le code Terraform.
5. L'API Gateway déclenche le déploiement via Terraform.
6. L'infrastructure est provisionnée.
7. Le pipeline ML est déployé.
8. L'utilisateur reçoit une notification de l'achèvement.

### 4.3 Flux de Surveillance

1. Prometheus collecte les métriques des déploiements.
2. Grafana affiche les métriques dans des dashboards.
3. L'utilisateur peut surveiller les performances via l'interface Grafana.

## 5. Structure du Projet

```
mlops-nocode-platform/
├── api/
│   └── fastapi/
│       ├── app/
│       │   ├── main.py
│       │   ├── core/
│       │   ├── models/
│       │   ├── schemas/
│       │   ├── routers/
│       │   └── __init__.py
│       ├── requirements.txt
│       ├── Dockerfile
│       └── README.md
├── orchestrator/
│   ├── windmill/
│   │   ├── apps/
│   │   ├── scripts/
│   │   ├── flows/
│   │   └── README.md
│   └── n8n/
│       └── docker-compose.yml
├── terraform/
│   ├── modules/
│   │   ├── k3s/
│   │   ├── exoscale/
│   │   ├── vastai/
│   │   └── runpod/
│   └── examples/
├── k8s/
│   └── manifests/
│       └── litellm/
├── monitoring/
│   ├── prometheus/
│   └── grafana/
├── docs/
│   ├── use_cases.md
│   ├── chatbot_code_generation.md
│   ├── fractal_composition.md
│   └── blueprint_integral.md
├── scripts/
│   └── init-tools.sh
├── tests/
│   └── test_cpu_throttler.py
├── cpu_throttler.py
├── resource_monitor.py
├── wait_for_resources.sh
├── install_throttler.sh
├── requirements.txt
├── README.md
└── blueprint_mlops_nocode_pipeline_orchestrator.md
```

## 6. Spécifications Techniques

### 6.1 API Gateway FastAPI

**Dépendances :**
- fastapi>=0.100.0,<0.101.0
- uvicorn[standard]>=0.23.0,<0.24.0
- pydantic>=2.0.0,<3.0.0
- pydantic-settings>=2.0.0,<3.0.0
- python-multipart>=0.0.6,<0.0.7

**Variables d'Environnement :**
- `DEBUG` : Mode debug (true/false)
- `SECRET_KEY` : Clé secrète pour les tokens JWT
- `DATABASE_URL` : URL de la base de données
- `N8N_API_URL` : URL de l'API n8n
- `N8N_API_KEY` : Clé API pour n8n
- `WINDMILL_API_URL` : URL de l'API Windmill
- `WINDMILL_API_KEY` : Clé API pour Windmill

### 6.2 Interface No-Code Windmill

**Dépendances :**
- Docker
- Docker Compose

**Variables d'Environnement :**
- Variables d'environnement Docker Compose (voir `orchestrator/windmill/docker-compose.yml`)

### 6.3 Orchestrateur de Workflows n8n

**Dépendances :**
- Docker
- Docker Compose

**Variables d'Environnement :**
- Variables d'environnement Docker Compose (voir `orchestrator/n8n/docker-compose.yml`)

### 6.4 Générateur d'IaC Terraform

**Dépendances :**
- Terraform (v1.5.7)
- Providers Terraform :
  - hashicorp/kubernetes
  - exoscale/exoscale
  - runpod/runpod

### 6.5 Déploiement LiteLLM

**Dépendances :**
- Kubernetes (kubectl)
- Helm (pour déploiements futurs)

### 6.6 Monitoring Prometheus/Grafana

**Dépendances :**
- Docker
- Docker Compose

### 6.7 Script de Throttling CPU

**Dépendances :**
- Python 3.8+
- psutil

**Variables d'Environnement :**
- `CPU_THRESHOLD` : Seuil d'utilisation CPU (par défaut 90.0)
- `LOAD_AVG_THRESHOLD` : Seuil de load average (par défaut 6.0)
- `CHECK_INTERVAL` : Intervalle de vérification (par défaut 0.1)
- `MAX_WAIT_TIME` : Temps d'attente maximum (par défaut 5.0)
- `THROTTLE_DISABLE` : Désactiver le throttling (par défaut false)
- `LOG_LEVEL` : Niveau de logging (par défaut INFO)

## 7. Reproductibilité sur VSCode/Kilocode avec Qwen3 Coder

### 7.1 Prérequis

- VSCode avec l'extension Kilocode installée
- Accès à Qwen3 Coder via Kilocode
- Docker et Docker Compose installés
- Python 3.8+ installé
- Git installé

### 7.2 Étapes de Reproductibilité

1.  **Cloner le Repository :**
    ```bash
    git clone https://github.com/dr-basalt/mlops-nocode-platform.git
    cd mlops-nocode-platform
    ```

2.  **Initialiser les Outils :**
    ```bash
    chmod +x scripts/init-tools.sh
    ./scripts/init-tools.sh
    ```

3.  **Démarrer les Services :**
    - Démarrer Windmill :
      ```bash
      cd orchestrator/windmill
      docker-compose up -d
      ```
    - Démarrer n8n :
      ```bash
      cd orchestrator/n8n
      docker-compose up -d
      ```
    - Démarrer Prometheus/Grafana :
      ```bash
      cd monitoring
      docker-compose up -d
      ```

4.  **Démarrer l'API Gateway :**
    ```bash
    cd api/fastapi
    pip install -r requirements.txt
    python app/main.py
    ```
    Ou avec Docker :
    ```bash
    cd api/fastapi
    docker build -t mlops-api-gateway .
    docker run -p 8000:8000 mlops-api-gateway
    ```

5.  **Configurer les Interfaces :**
    - Accéder à Windmill : `http://localhost:3000`
    - Accéder à n8n : `http://localhost:5678`
    - Accéder à Grafana : `http://localhost:3001`

6.  **Importer les Configurations :**
    - Dans Windmill, importer l'application `apps/ml_pipeline_builder.json`.
    - Dans Windmill, importer les scripts de `scripts/`.
    - Dans Windmill, importer le flow `flows/ml_pipeline_deployment.json`.

7.  **Tester le Déploiement :**
    - Utiliser l'application Windmill pour configurer et déployer un pipeline.
    - Vérifier le statut du déploiement via l'API Gateway.
    - Surveiller les performances via Grafana.

### 7.3 Utilisation avec Kilocode et Qwen3 Coder

1.  **Ouvrir le Projet dans VSCode :**
    - Ouvrir le dossier `mlops-nocode-platform` dans VSCode.

2.  **Utiliser Kilocode :**
    - Activer Kilocode dans VSCode.
    - Sélectionner Qwen3 Coder comme modèle.
    - Utiliser les commandes Kilocode pour :
      - Comprendre le code existant.
      - Générer de nouveaux composants.
      - Déboguer les problèmes.
      - Documenter le code.

3.  **Exemples de Commandes Kilocode :**
    - `@kilocode explain` : Expliquer un fichier ou une fonction.
    - `@kilocode generate` : Générer du code à partir d'une description.
    - `@kilocode debug` : Aider à déboguer un problème.
    - `@kilocode document` : Générer de la documentation.

## 8. Cas d'Utilisation

Voir `docs/use_cases.md` pour une description détaillée des cas d'utilisation et scénarios.

## 9. Analyses Avancées

### 9.1 Génération de Code Applicatif via Chatbot

Voir `docs/chatbot_code_generation.md` pour une analyse de la capacité de la plateforme à générer du code applicatif via un chatbot.

### 9.2 Composition Fractale de Playbooks, Pipelines et Meta-Pipelines

Voir `docs/fractal_composition.md` pour une analyse de la capacité de la plateforme à permettre une composition fractale avancée.

## 10. Conclusion

La plateforme MLOps No-Code Platform est une solution complète et modulaire pour le déploiement de pipelines ML. Elle est conçue pour être extensible et peut être facilement reproduite sur une stack VSCode/Kilocode avec Qwen3 Coder. Le blueprint fournit toutes les informations nécessaires pour un spécialiste MLOps, Vibe coding ou architecte AI pour analyser, comprendre et potentiellement étendre la plateforme.