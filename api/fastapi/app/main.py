from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn
import os
import json
import subprocess
import tempfile
from datetime import datetime

# Importer les configurations
from app.core.config import settings

# Créer l'instance de l'application FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API Gateway pour la plateforme MLOps No-Code",
    version="1.0.0",
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Stockage en mémoire pour les statuts de pipeline (à remplacer par une base de données en production)
pipeline_statuses: Dict[str, dict] = {}

# Modèles Pydantic pour la validation des données
class PipelineConfig(BaseModel):
    name: str
    description: Optional[str] = None
    nodes: List[dict]  # Liste des nœuds du pipeline (à définir plus précisément)
    compute_requirements: dict  # Exigences de calcul (GPU, CPU, mémoire, etc.)
    deployment_target: str  # Cible de déploiement (k3s-local, exoscale, vastai, runpod)

class PipelineDeploymentResponse(BaseModel):
    pipeline_id: str
    status: str
    message: str

class PipelineStatusResponse(BaseModel):
    pipeline_id: str
    status: str
    details: str
    timestamp: str

class HealthCheckResponse(BaseModel):
    status: str
    timestamp: str

def validate_pipeline_config(config: PipelineConfig) -> bool:
    """
    Valide la configuration du pipeline.
    
    Args:
        config: Configuration du pipeline.
        
    Returns:
        True si la configuration est valide, False sinon.
    """
    if not config.name:
        return False
    
    if not config.deployment_target:
        return False
    
    valid_targets = ["k3s-local", "exoscale", "vastai", "runpod"]
    if config.deployment_target not in valid_targets:
        return False
    
    return True

def generate_terraform_code(config: PipelineConfig) -> str:
    """
    Génère le code Terraform pour le déploiement du pipeline.
    
    Args:
        config: Configuration du pipeline.
        
    Returns:
        Code Terraform généré.
    """
    target_platform = config.deployment_target
    
    if target_platform == "k3s-local":
        return generate_k3s_terraform_code(config)
    elif target_platform == "exoscale":
        return generate_exoscale_terraform_code(config)
    elif target_platform == "vastai":
        return generate_vastai_terraform_code(config)
    elif target_platform == "runpod":
        return generate_runpod_terraform_code(config)
    else:
        raise ValueError(f"Plateforme cible non supportée: {target_platform}")

def generate_k3s_terraform_code(config: PipelineConfig) -> str:
    """
    Génère le code Terraform pour le déploiement sur K3s local.
    
    Args:
        config: Configuration du pipeline.
        
    Returns:
        Code Terraform généré.
    """
    # C"est un exemple simplifié. Dans la réalité, cela serait plus complexe.
    return f"""
terraform {{
  required_providers {{
    kubernetes = {{
      source  = "hashicorp/kubernetes"
      version = "2.20.0"
    }}
  }}
}}

provider "kubernetes" {{
  config_path = "~/.kube/config"
}}

resource "kubernetes_deployment" "ml_pipeline" {{
  metadata {{
    name = "{config.name.replace(" ", "-").lower()}"
    labels = {{
      app = "{config.name.replace(" ", "-").lower()}"
    }}
  }}

  spec {{
    replicas = 1

    selector {{
      match_labels = {{
        app = "{config.name.replace(" ", "-").lower()}"
      }}
    }}

    template {{
      metadata {{
        labels = {{
          app = "{config.name.replace(" ", "-").lower()}"
        }}
      }}

      spec {{
        container {{
          image = "nginx:latest"  # Exemple d"image
          name  = "{config.name.replace(" ", "-").lower()}"

          port {{
            container_port = 80
          }}
        }}
      }}
    }}
  }}
}}

resource "kubernetes_service" "ml_pipeline" {{
  metadata {{
    name = "{config.name.replace(" ", "-").lower()}"
  }}

  spec {{
    selector = {{
      app = "{config.name.replace(" ", "-").lower()}"
    }}

    port {{
      protocol    = "TCP"
      port        = 80
      target_port = 80
    }}

    type = "LoadBalancer"
  }}
}}
"""

def generate_exoscale_terraform_code(config: PipelineConfig) -> str:
    """
    Génère le code Terraform pour le déploiement sur Exoscale.
    
    Args:
        config: Configuration du pipeline.
        
    Returns:
        Code Terraform généré.
    """
    # C"est un exemple simplifié. Dans la réalité, cela serait plus complexe.
    return f"""
terraform {{
  required_providers {{
    exoscale = {{
      source  = "exoscale/exoscale"
      version = "0.50.0"
    }}
  }}
}}

provider "exoscale" {{
  key    = var.exoscale_api_key
  secret = var.exoscale_api_secret
}}

resource "exoscale_compute_instance" "ml_pipeline" {{
  name = "{config.name.replace(" ", "-").lower()}"
  type = "standard.medium"
  disk_size = 50
  image = "ubuntu-22.04"
  
  security_group_ids = [
    exoscale_security_group.ml_pipeline.id
  ]
}}

resource "exoscale_security_group" "ml_pipeline" {{
  name = "{config.name.replace(" ", "-").lower()}-sg"
}}

resource "exoscale_security_group_rule" "ml_pipeline_http" {{
  security_group_id = exoscale_security_group.ml_pipeline.id
  type              = "ingress"
  protocol          = "tcp"
  start_port        = 80
  end_port          = 80
  cidr              = "0.0.0.0/0"
}}
"""

def generate_vastai_terraform_code(config: PipelineConfig) -> str:
    """
    Génère le code Terraform pour le déploiement sur Vast.ai.
    
    Args:
        config: Configuration du pipeline.
        
    Returns:
        Code Terraform généré.
    """
    # C"est un exemple simplifié. Dans la réalité, cela serait plus complexe.
    # Vast.ai n"a pas de provider Terraform officiel, donc cela serait implémenté via leur API.
    return f"""
# Vast.ai deployment
# This is a placeholder as Vast.ai does not have an official Terraform provider.
# Deployment would be done via their API.

# Example of what the configuration might look like:
# pipeline_name = {config.name}
# target_platform = {config.deployment_target}
# nodes = {json.dumps(config.nodes, indent=2)}
"""

def generate_runpod_terraform_code(config: PipelineConfig) -> str:
    """
    Génère le code Terraform pour le déploiement sur RunPod.
    
    Args:
        config: Configuration du pipeline.
        
    Returns:
        Code Terraform généré.
    """
    # C"est un exemple simplifié. Dans la réalité, cela serait plus complexe.
    return f"""
terraform {{
  required_providers {{
    runpod = {{
      source  = "runpod/runpod"
      version = "1.0.0"
    }}
  }}
}}

provider "runpod" {{
  api_key = var.runpod_api_key
}}

resource "runpod_pod" "ml_pipeline" {{
  name            = "{config.name.replace(" ", "-").lower()}"
  image_name      = "runpod/pytorch:2.0.1-py3.10-cuda11.8.0-devel-ubuntu22.04"
  gpu_type_id     = "NVIDIA GeForce RTX 4090"
  gpu_count       = 1
  container_disk_in_gb = 40
  volume_in_gb    = 0
  volume_mount_path = "/runpod-volume"
  cloud_type      = "ALL"
  min_vcpu_count  = 2
  min_memory_in_gb = 15
  docker_args     = ""
  ports           = ""
  env             = {{}}
  template_id     = ""
  container_name  = "runpod-container"
  start_ssh       = true
  is_public       = false
  shutdown_timeout = 5
}}
"""

def trigger_windmill_workflow(config: PipelineConfig, terraform_code: str) -> str:
    """
    Déclenche le workflow Windmill pour le déploiement du pipeline.
    
    Args:
        config: Configuration du pipeline.
        terraform_code: Code Terraform à déployer.
        
    Returns:
        ID du workflow déclenché.
    """
    # Pour l"instant, on simule le déclenchement du workflow
    # Dans la réalité, cela impliquerait un appel à l"API Windmill
    workflow_id = f"workflow_{config.name.replace(' ', '_')}_{int(datetime.utcnow().timestamp())}"
    
    # Mettre à jour le statut du pipeline
    pipeline_statuses[workflow_id] = {
        "status": "initiated",
        "details": f"Workflow {workflow_id} déclenché pour le déploiement du pipeline {config.name}.",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    return workflow_id

# Endpoints de l'API

@app.get("/", tags=["Root"])
async def read_root():
    """
    Endpoint racine de l'API.
    """
    return {"message": "Bienvenue sur l'API Gateway de la plateforme MLOps No-Code"}

@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check():
    """
    Endpoint de vérification de l'état de l'API.
    """
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat()
    )

@app.post("/pipelines/deploy", response_model=PipelineDeploymentResponse, tags=["Pipelines"])
async def deploy_pipeline(config: PipelineConfig):
    """
    Endpoint pour déployer un pipeline ML.
    """
    # 1. Validation de la configuration
    if not validate_pipeline_config(config):
        raise HTTPException(status_code=400, detail="Configuration du pipeline invalide.")
    
    # 2. Génération de l'IaC (Terraform)
    try:
        terraform_code = generate_terraform_code(config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération du code Terraform: {str(e)}")
    
    # 3. Déclenchement du workflow d'orchestration (Windmill)
    try:
        workflow_id = trigger_windmill_workflow(config, terraform_code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du déclenchement du workflow Windmill: {str(e)}")
    
    # 4. Retour d'un ID de suivi du déploiement
    pipeline_id = f"pipeline_{config.name.replace(' ', '_')}_{int(datetime.utcnow().timestamp())}"
    pipeline_statuses[pipeline_id] = {
        "status": "initiated",
        "details": f"Déploiement du pipeline '{config.name}' initié. Workflow ID: {workflow_id}",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    return PipelineDeploymentResponse(
        pipeline_id=pipeline_id,
        status="initiated",
        message=f"Déploiement du pipeline '{config.name}' initié. Veuillez suivre l'état du déploiement avec l'ID {pipeline_id}."
    )

@app.get("/pipelines/{pipeline_id}/status", response_model=PipelineStatusResponse, tags=["Pipelines"])
async def get_pipeline_status(pipeline_id: str):
    """
    Endpoint pour obtenir le statut d'un pipeline.
    """
    if pipeline_id not in pipeline_statuses:
        raise HTTPException(status_code=404, detail="Pipeline non trouvé.")
    
    status_info = pipeline_statuses[pipeline_id]
    return PipelineStatusResponse(
        pipeline_id=pipeline_id,
        status=status_info["status"],
        details=status_info["details"],
        timestamp=status_info["timestamp"]
    )

# Point d'entrée pour exécuter l'application avec uvicorn
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        log_level="info",
        reload=settings.DEBUG,
    )