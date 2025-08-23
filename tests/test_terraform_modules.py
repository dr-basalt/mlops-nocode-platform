import pytest
import os
import tempfile
import subprocess
import sys

# Ajouter le chemin des scripts au sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'orchestrator', 'windmill', 'scripts'))

def test_terraform_k3s_module():
    """Test de la génération de code Terraform pour K3s."""
    # Importer le script de déploiement de pipeline
    try:
        from deploy_pipeline import generate_terraform_code
    except ImportError:
        pytest.skip("Script de déploiement non trouvé")
    
    # Configuration de test pour K3s
    pipeline_config = {
        "name": "Test K3s Pipeline",
        "deployment_target": "k3s-local",
        "compute_requirements": {
            "cpu": "2",
            "memory": "4Gi"
        }
    }
    
    # Générer le code Terraform
    terraform_code = generate_terraform_code(pipeline_config)
    
    # Vérifier que le code Terraform a été généré
    assert terraform_code is not None
    assert isinstance(terraform_code, str)
    assert len(terraform_code) > 0
    
    # Vérifier que le code contient des éléments spécifiques à K3s
    assert "k3s" in terraform_code.lower() or "kubernetes" in terraform_code.lower()

def test_terraform_exoscale_module():
    """Test de la génération de code Terraform pour Exoscale."""
    # Importer le script de déploiement de pipeline
    try:
        from deploy_pipeline import generate_terraform_code
    except ImportError:
        pytest.skip("Script de déploiement non trouvé")
    
    # Configuration de test pour Exoscale
    pipeline_config = {
        "name": "Test Exoscale Pipeline",
        "deployment_target": "exoscale",
        "compute_requirements": {
            "cpu": "2",
            "memory": "4Gi",
            "gpu": "1"
        }
    }
    
    # Générer le code Terraform
    terraform_code = generate_terraform_code(pipeline_config)
    
    # Vérifier que le code Terraform a été généré
    assert terraform_code is not None
    assert isinstance(terraform_code, str)
    assert len(terraform_code) > 0
    
    # Vérifier que le code contient des éléments spécifiques à Exoscale
    assert "exoscale" in terraform_code.lower()

def test_terraform_vastai_module():
    """Test de la génération de code Terraform pour Vast.ai."""
    # Importer le script de déploiement de pipeline
    try:
        from deploy_pipeline import generate_terraform_code
    except ImportError:
        pytest.skip("Script de déploiement non trouvé")
    
    # Configuration de test pour Vast.ai
    pipeline_config = {
        "name": "Test Vast.ai Pipeline",
        "deployment_target": "vastai",
        "compute_requirements": {
            "cpu": "8",
            "memory": "32Gi",
            "gpu": "1"
        }
    }
    
    # Générer le code Terraform
    terraform_code = generate_terraform_code(pipeline_config)
    
    # Vérifier que le code Terraform a été généré
    assert terraform_code is not None
    assert isinstance(terraform_code, str)
    assert len(terraform_code) > 0
    
    # Vérifier que le code contient des éléments spécifiques à Vast.ai
    assert "vastai" in terraform_code.lower()

def test_terraform_runpod_module():
    """Test de la génération de code Terraform pour RunPod."""
    # Importer le script de déploiement de pipeline
    try:
        from deploy_pipeline import generate_terraform_code
    except ImportError:
        pytest.skip("Script de déploiement non trouvé")
    
    # Configuration de test pour RunPod
    pipeline_config = {
        "name": "Test RunPod Pipeline",
        "deployment_target": "runpod",
        "compute_requirements": {
            "cpu": "4",
            "memory": "16Gi",
            "gpu": "1"
        }
    }
    
    # Générer le code Terraform
    terraform_code = generate_terraform_code(pipeline_config)
    
    # Vérifier que le code Terraform a été généré
    assert terraform_code is not None
    assert isinstance(terraform_code, str)
    assert len(terraform_code) > 0
    
    # Vérifier que le code contient des éléments spécifiques à RunPod
    assert "runpod" in terraform_code.lower()