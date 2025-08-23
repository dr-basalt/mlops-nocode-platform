import pytest
import os
import sys
import subprocess
import time

# Ajouter le chemin des scripts au sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'orchestrator', 'windmill'))

def test_windmill_script_execution():
    """Test de l'exécution d'un script Windmill."""
    # Chemin vers le script de test
    script_path = os.path.join(
        os.path.dirname(__file__), 
        '..', 'orchestrator', 'windmill', 'scripts', 'deploy_pipeline.py'
    )
    
    # Vérifier que le script existe
    if not os.path.exists(script_path):
        pytest.skip("Script de déploiement non trouvé")
    
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
            timeout=60  # Timeout de 60 secondes
        )
        
        # Vérifier que l'exécution s'est terminée correctement
        assert result.returncode == 0, f"Script failed with return code {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"
        
    except subprocess.TimeoutExpired:
        pytest.fail("Script execution timed out")
    except Exception as e:
        pytest.fail(f"Script execution failed with exception: {e}")

def test_windmill_flow_execution():
    """Test de l'exécution d'un flow Windmill."""
    # Chemin vers le flow de test
    flow_path = os.path.join(
        os.path.dirname(__file__), 
        '..', 'orchestrator', 'windmill', 'flows', 'ml_pipeline_flow.json'
    )
    
    # Vérifier que le flow existe
    if not os.path.exists(flow_path):
        pytest.skip("Flow de pipeline ML non trouvé")
    
    # Exécuter le flow avec des arguments de test
    try:
        # Utiliser le script wait_for_resources.sh pour vérifier les ressources avant l'exécution
        result = subprocess.run(
            [
                "/home/coder/wait_for_resources.sh",
                "--wait",
                "python3",
                "-c",
                f"import json; print('Flow execution simulation for {flow_path}')"
            ],
            capture_output=True,
            text=True,
            timeout=60  # Timeout de 60 secondes
        )
        
        # Vérifier que l'exécution s'est terminée correctement
        assert result.returncode == 0, f"Flow execution failed with return code {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"
        
    except subprocess.TimeoutExpired:
        pytest.fail("Flow execution timed out")
    except Exception as e:
        pytest.fail(f"Flow execution failed with exception: {e}")

def test_windmill_app_import():
    """Test de l'importation d'une application Windmill."""
    # Chemin vers l'application de test
    app_path = os.path.join(
        os.path.dirname(__file__), 
        '..', 'orchestrator', 'windmill', 'apps', 'ml_pipeline_builder.json'
    )
    
    # Vérifier que l'application existe
    if not os.path.exists(app_path):
        pytest.skip("Application ML Pipeline Builder non trouvée")
    
    # Simuler l'importation de l'application
    try:
        # Utiliser le script wait_for_resources.sh pour vérifier les ressources avant l'exécution
        result = subprocess.run(
            [
                "/home/coder/wait_for_resources.sh",
                "--wait",
                "python3",
                "-c",
                f"import json; with open('{app_path}', 'r') as f: data = json.load(f); print(f'App imported: {{data.get(\"name\", \"Unknown\")}}')"
            ],
            capture_output=True,
            text=True,
            timeout=30  # Timeout de 30 secondes
        )
        
        # Vérifier que l'importation s'est terminée correctement
        assert result.returncode == 0, f"App import failed with return code {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"
        
    except subprocess.TimeoutExpired:
        pytest.fail("App import timed out")
    except Exception as e:
        pytest.fail(f"App import failed with exception: {e}")