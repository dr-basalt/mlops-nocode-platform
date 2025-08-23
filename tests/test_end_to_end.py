import pytest
import os
import sys
import subprocess
import time
import requests
import json

# Ajouter le chemin des scripts au sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'orchestrator', 'windmill', 'scripts'))

def test_end_to_end_pipeline_deployment():
    """Test de bout en bout du déploiement d'un pipeline ML."""
    # 1. Vérifier les ressources système
    print("1. Vérification des ressources système...")
    result = subprocess.run(
        ["/home/coder/wait_for_resources.sh", "--wait"],
        capture_output=True,
        text=True,
        timeout=60
    )
    assert result.returncode == 0, "Resource check failed"
    
    # 2. Déployer un pipeline via l'API Gateway
    print("2. Déploiement d'un pipeline via l'API Gateway...")
    api_url = "http://localhost:8000"  # URL de l'API Gateway en développement local
    
    # Données de test pour le déploiement d'un pipeline
    pipeline_config = {
        "name": "End-to-End Test Pipeline",
        "description": "Pipeline de test pour les tests de bout en bout",
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
            },
            {
                "id": "node3",
                "type": "model",
                "config": {
                    "model_type": "sklearn",
                    "algorithm": "random_forest"
                }
            },
            {
                "id": "node4",
                "type": "deployment",
                "config": {
                    "endpoint": "/api/v1/predict"
                }
            }
        ],
        "compute_requirements": {
            "cpu": "2",
            "memory": "4Gi"
        },
        "deployment_target": "k3s-local"
    }
    
    try:
        response = requests.post(
            f"{api_url}/pipelines/deploy",
            json=pipeline_config,
            timeout=30
        )
        assert response.status_code == 200, f"Pipeline deployment failed with status code {response.status_code}"
        
        json_response = response.json()
        assert "pipeline_id" in json_response, "Missing 'pipeline_id' in deployment response"
        assert "status" in json_response, "Missing 'status' in deployment response"
        assert json_response["status"] == "initiated", f"Pipeline deployment status is not 'initiated': {json_response['status']}"
        
        pipeline_id = json_response["pipeline_id"]
        print(f"   Pipeline déployé avec ID: {pipeline_id}")
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Pipeline deployment failed with exception: {e}")
    
    # 3. Attendre que le déploiement soit terminé
    print("3. Attente de la fin du déploiement...")
    max_wait_time = 120  # 2 minutes maximum
    start_time = time.time()
    
    while time.time() - start_time < max_wait_time:
        try:
            response = requests.get(
                f"{api_url}/pipelines/{pipeline_id}/status",
                timeout=30
            )
            assert response.status_code == 200, f"Pipeline status check failed with status code {response.status_code}"
            
            json_response = response.json()
            assert "status" in json_response, "Missing 'status' in status response"
            
            if json_response["status"] == "running":
                print("   Pipeline en cours d'exécution")
                break
            elif json_response["status"] == "completed":
                print("   Pipeline terminé avec succès")
                break
            elif json_response["status"] == "failed":
                pytest.fail(f"Pipeline deployment failed: {json_response.get('details', 'Unknown error')}")
            
            print(f"   Statut du pipeline: {json_response['status']}")
            time.sleep(10)  # Attendre 10 secondes avant de revérifier
            
        except requests.exceptions.RequestException as e:
            print(f"   Erreur lors de la vérification du statut: {e}")
            time.sleep(10)
    
    # 4. Vérifier que LiteLLM est déployé et fonctionne
    print("4. Vérification du déploiement de LiteLLM...")
    time.sleep(10)  # Attendre un moment pour que LiteLLM démarre
    
    try:
        response = requests.get("http://localhost:4000/health", timeout=30)
        assert response.status_code == 200, f"LiteLLM health check failed with status code {response.status_code}"
        
        json_response = response.json()
        assert "status" in json_response, "Missing 'status' in LiteLLM health check response"
        assert json_response["status"] == "healthy", f"LiteLLM is not healthy: {json_response['status']}"
        print("   LiteLLM est déployé et en bonne santé")
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"LiteLLM health check failed with exception: {e}")
    
    # 5. Vérifier que le monitoring est en place
    print("5. Vérification du monitoring...")
    try:
        # Vérifier que Prometheus est accessible
        response = requests.get("http://localhost:9090/-/healthy", timeout=30)
        assert response.status_code == 200, f"Prometheus health check failed with status code {response.status_code}"
        print("   Prometheus est en place")
        
        # Vérifier que Grafana est accessible
        response = requests.get("http://localhost:3000/api/health", timeout=30)
        assert response.status_code == 200, f"Grafana health check failed with status code {response.status_code}"
        print("   Grafana est en place")
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Monitoring check failed with exception: {e}")
    
    print("Test de bout en bout terminé avec succès!")

def test_end_to_end_pipeline_invocation():
    """Test de bout en bout de l'invoquation d'un pipeline ML."""
    # 1. Vérifier les ressources système
    print("1. Vérification des ressources système...")
    result = subprocess.run(
        ["/home/coder/wait_for_resources.sh", "--wait"],
        capture_output=True,
        text=True,
        timeout=60
    )
    assert result.returncode == 0, "Resource check failed"
    
    # 2. Invoquer un pipeline via l'API Gateway
    print("2. Invoquation d'un pipeline via l'API Gateway...")
    api_url = "http://localhost:8000"  # URL de l'API Gateway en développement local
    
    # Données de test pour l'invoquation d'un pipeline
    invocation_data = {
        "pipeline_id": "end_to_end_test_pipeline",
        "input_data": {
            "features": [1.0, 2.0, 3.0, 4.0]
        }
    }
    
    try:
        response = requests.post(
            f"{api_url}/pipelines/invoke",
            json=invocation_data,
            timeout=30
        )
        
        # Vérifier que la requête a été traitée (le pipeline peut ne pas exister, mais l'API doit répondre)
        assert response.status_code in [200, 404], f"Pipeline invocation failed with status code {response.status_code}"
        
        if response.status_code == 200:
            json_response = response.json()
            assert "result" in json_response, "Missing 'result' in invocation response"
            print("   Pipeline invoqué avec succès")
        elif response.status_code == 404:
            print("   Pipeline non trouvé (ce qui est acceptable pour ce test)")
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Pipeline invocation failed with exception: {e}")
    
    print("Test d'invoquation de bout en bout terminé!")