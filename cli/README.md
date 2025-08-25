# CLI pour l'Autopilot Engine

Ce CLI permet d'interagir avec l'Autopilot Engine de la plateforme MLOps No-Code.

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

### Analyser un blueprint

```bash
python cline-integration.py analyze --blueprint "Créer une application de chat en temps réel avec Next.js et FastAPI"
```

### Générer un projet

```bash
python cline-integration.py generate \
  --blueprint "Créer une application de chat en temps réel avec Next.js et FastAPI" \
  --target-repo "https://github.com/user/chat-app" \
  --stack "nextjs,fastapi,postgresql" \
  --ui-system "shadcn" \
  --autopilot \
  --deploy
```

## Configuration

Le CLI peut être configuré via des variables d'environnement :

- `API_GATEWAY_URL`: URL de l'API Gateway (par défaut: `http://localhost:8000/api/v1`)
- `GITHUB_TOKEN`: Token d'accès GitHub pour le push automatique
- `GITLAB_TOKEN`: Token d'accès GitLab pour le push automatique

Exemple de configuration :

```bash
export API_GATEWAY_URL="http://api.example.com/api/v1"
export GITHUB_TOKEN="votre_token_github"