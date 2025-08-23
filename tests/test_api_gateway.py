import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    """Test de l'endpoint racine de l'API."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue sur l'API Gateway de la plateforme MLOps No-Code"}

def test_health_check():
    """Test de l'endpoint de vérification de l'état de l'API."""
    response = client.get("/health")
    assert response.status_code == 200
    json_response = response.json()
    assert "status" in json_response
    assert json_response["status"] == "healthy"
    assert "timestamp" in json_response

def test_deploy_pipeline():
    """Test de l'endpoint de déploiement de pipeline."""
    # Données de test pour le déploiement d'un pipeline
    pipeline_config = {
        "name": "Test Pipeline",
        "description": "Pipeline de test pour les tests d'intégration",
        "nodes": [
            {
                "id": "node1",
                "type": "data_source",
                "config": {
                    "source": "test_data.csv"
                }
            },
            {
                "id": "node2",
                "type": "preprocessing",
                "config": {
                    "steps": ["normalize", "encode"]
                }
            }
        ],
        "compute_requirements": {
            "cpu": "2",
            "memory": "4Gi",
            "gpu": "1"
        },
        "deployment_target": "k3s-local"
    }
    
    response = client.post("/pipelines/deploy", json=pipeline_config)
    assert response.status_code == 200
    json_response = response.json()
    assert "pipeline_id" in json_response
    assert "status" in json_response
    assert json_response["status"] == "initiated"
    assert "message" in json_response

def test_get_pipeline_status():
    """Test de l'endpoint de récupération du statut d'un pipeline."""
    # Utiliser un pipeline_id simulé
    pipeline_id = "pipeline_test_status"
    
    response = client.get(f"/pipelines/{pipeline_id}/status")
    assert response.status_code == 200
    json_response = response.json()
    assert "pipeline_id" in json_response
    assert json_response["pipeline_id"] == pipeline_id
    assert "status" in json_response
    # Le statut peut varier, mais il doit exister
    assert json_response["status"] is not None
    assert "details" in json_response