from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os

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

class HealthCheckResponse(BaseModel):
    status: str
    timestamp: str

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
    from datetime import datetime
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat()
    )

@app.post("/pipelines/deploy", response_model=PipelineDeploymentResponse, tags=["Pipelines"])
async def deploy_pipeline(config: PipelineConfig):
    """
    Endpoint pour déployer un pipeline ML.
    """
    # TODO: Implémenter la logique de déploiement
    # Cela impliquera:
    # 1. Validation de la configuration
    # 2. Génération de l'IaC (Terraform)
    # 3. Déclenchement du workflow d'orchestration (n8n/Windmill)
    # 4. Retour d'un ID de suivi du déploiement
    
    # Pour l'instant, retourner une réponse simulée
    return PipelineDeploymentResponse(
        pipeline_id=f"pipeline_{config.name.replace(' ', '_')}",
        status="initiated",
        message=f"Déploiement du pipeline '{config.name}' initié. Veuillez suivre l'état du déploiement."
    )

@app.get("/pipelines/{pipeline_id}/status", tags=["Pipelines"])
async def get_pipeline_status(pipeline_id: str):
    """
    Endpoint pour obtenir le statut d'un pipeline.
    """
    # TODO: Implémenter la logique pour récupérer le statut du pipeline
    # Cela pourrait impliquer une requête à une base de données ou à un service d'orchestration
    
    # Pour l'instant, retourner une réponse simulée
    return {
        "pipeline_id": pipeline_id,
        "status": "running",
        "details": "Le pipeline est en cours d'exécution."
    }

# Point d'entrée pour exécuter l'application avec uvicorn
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        log_level="info",
        reload=settings.DEBUG,
    )