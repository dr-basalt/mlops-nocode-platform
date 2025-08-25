# AutoPush Engine pour l'Autopilot Engine

Ce module permet de créer des repositories Git et de pusher automatiquement le code généré par l'Autopilot Engine.

## Fonctionnalités

- Création automatique de repositories GitHub et GitLab
- Push automatique du code généré
- Support pour les providers GitHub et GitLab
- Gestion des tokens d'accès

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

### En tant que module Python

```python
from git.autopush_engine import AutoPushEngine

# Initialiser l'engine
engine = AutoPushEngine()

# Exemple de codebase généré
codebase = {
    "main.py": "print('Hello, World!')",
    "README.md": "# Generated Project\n\nThis is a generated project.",
    "requirements.txt": "fastapi\nuvicorn"
}

# Créer et push le code
repo_url = await engine.create_and_push(
    codebase, 
    "test-project", 
    auto_deploy=False
)
print(f"Code pushed to: {repo_url}")
```

## Configuration

Le module peut être configuré via des variables d'environnement :

- `GITHUB_TOKEN`: Token d'accès GitHub
- `GITLAB_TOKEN`: Token d'accès GitLab

Exemple de configuration :

```bash
export GITHUB_TOKEN="votre_token_github"
export GITLAB_TOKEN="votre_token_gitlab"