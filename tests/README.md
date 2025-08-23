# Tests d'intégration pour la plateforme MLOps No-Code

## Description

Ce dossier contient les tests d'intégration pour la plateforme MLOps No-Code. Ces tests vérifient que tous les composants du système fonctionnent correctement ensemble.

## Structure des tests

- `test_api_gateway.py` : Tests de l'API Gateway FastAPI.
- `test_terraform_modules.py` : Tests des modules Terraform.
- `test_windmill_integration.py` : Tests de l'intégration Windmill.
- `test_lite_llm_deployment.py` : Tests du déploiement de LiteLLM.
- `test_end_to_end.py` : Tests de bout en bout.

## Dépendances

Les dépendances pour les tests sont listées dans `requirements.txt` :

- `pytest` : Framework de test pour Python.
- `pytest-cov` : Plugin pour la couverture de code.
- `pytest-asyncio` : Plugin pour les tests asynchrones.
- `httpx` : Client HTTP pour les tests d'API.
- `requests` : Client HTTP pour les tests d'intégration.

## Installation des dépendances

Pour installer les dépendances de test, exécutez :

```bash
pip install -r requirements.txt
```

## Exécution des tests

### Tous les tests

Pour exécuter tous les tests :

```bash
pytest
```

### Tests spécifiques

Pour exécuter un fichier de test spécifique :

```bash
pytest test_api_gateway.py
```

Pour exécuter un test spécifique :

```bash
pytest test_api_gateway.py::test_read_root
```

### Avec couverture de code

Pour exécuter les tests avec un rapport de couverture de code :

```bash
pytest --cov=../api/fastapi/app --cov-report=html --cov-report=term
```

Cela générera un rapport de couverture dans le dossier `htmlcov`.

## Configuration

Le fichier `conftest.py` contient la configuration des tests, notamment la création d'un client de test pour l'API FastAPI.

## Bonnes pratiques

- Les tests doivent être indépendants les uns des autres.
- Les tests doivent nettoyer après eux (par exemple, supprimer les fichiers temporaires).
- Les tests doivent utiliser des données de test réalistes.
- Les tests doivent vérifier à la fois les cas de succès et les cas d'erreur.
- Les tests doivent être rapides et fiables.

## Ressources

- [Documentation pytest](https://docs.pytest.org/)
- [Documentation FastAPI - Testing](https://fastapi.tiangolo.com/tutorial/testing/)