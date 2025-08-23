import pytest
import os
import sys
import subprocess
import time
import requests

# Ajouter le chemin des scripts au sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'orchestrator', 'windmill', 'scripts'))

def test_lite_llm_deployment():
    """Test du déploiement de LiteLLM."""
    # Chemin vers le script de déploiement de LiteLLM
    script_path = os.path.join(
        os.path.dirname(__file__), 
        '..', 'orchestrator', 'windmill', 'scripts', 'deploy_lite_llm.py'
    )
    
    # Vérifier que le script existe
    if not os.path.exists(script_path):
        pytest.skip("Script de déploiement de LiteLLM non trouvé")
    
    # Exécuter le script avec des arguments de test
    try:
        # Utiliser le script wait_for_resources.sh pour vérifier les ressources avant l'exécution
        result = subprocess.run(
            [
                "/home/coder/wait_for_resources.sh",
                "--wait",
                "python3",
                script_path,
                "--test-mode"
            ],
            capture_output=True,
            text=True,
            timeout=120  # Timeout de 120 secondes
        )
        
        # Vérifier que l'exécution s'est terminée correctement
        assert result.returncode == 0, f"Script failed with return code {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"
        
    except subprocess.TimeoutExpired:
        pytest.fail("Script execution timed out")
    except Exception as e:
        pytest.fail(f"Script execution failed with exception: {e}")

def test_lite_llm_health_check():
    """Test de la vérification de l'état de LiteLLM."""
    # Attendre un moment pour que LiteLLM démarre
    time.sleep(10)
    
    # Vérifier que LiteLLM est accessible
    try:
        response = requests.get("http://localhost:4000/health", timeout=30)
        assert response.status_code == 200, f"LiteLLM health check failed with status code {response.status_code}"
        
        # Vérifier que la réponse contient les éléments attendus
        json_response = response.json()
        assert "status" in json_response, "Missing 'status' in LiteLLM health check response"
        assert json_response["status"] == "healthy", f"LiteLLM is not healthy: {json_response['status']}"
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"LiteLLM health check failed with exception: {e}")
    except Exception as e:
        pytest.fail(f"LiteLLM health check failed with unexpected exception: {e}")

def test_lite_llm_model_routing():
    """Test du routage des modèles LiteLLM."""
    # Attendre un moment pour que LiteLLM démarre
    time.sleep(5)
    
    # Vérifier que LiteLLM est accessible
    try:
        response = requests.get("http://localhost:4000/models", timeout=30)
        assert response.status_code == 200, f"LiteLLM models endpoint failed with status code {response.status_code}"
        
        # Vérifier que la réponse contient les éléments attendus
        json_response = response.json()
        assert "data" in json_response, "Missing 'data' in LiteLLM models response"
        assert isinstance(json_response["data"], list), "'data' should be a list in LiteLLM models response"
        
        # Vérifier qu'il y a au moins un modèle
        assert len(json_response["data"]) > 0, "No models found in LiteLLM"
        
    except requests.exceptions.RequestException as e:
        pytest.fail(f"LiteLLM models check failed with exception: {e}")
    except Exception as e:
        pytest.fail(f"LiteLLM models check failed with unexpected exception: {e}")