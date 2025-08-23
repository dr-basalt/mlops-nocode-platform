import sys
import os
import pytest
from fastapi.testclient import TestClient

# Ajouter le chemin de l'application au sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api', 'fastapi'))

# Importer l'application FastAPI
from app.main import app

@pytest.fixture(scope="module")
def client():
    """Fixture pour créer un client de test pour l'API FastAPI."""
    with TestClient(app) as c:
        yield c