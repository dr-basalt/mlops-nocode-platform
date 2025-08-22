from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Nom du projet
    PROJECT_NAME: str = "MLOps No-Code Platform API Gateway"
    
    # Version de l'API
    API_V1_STR: str = "/api/v1"
    
    # Hôte et port
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Mode debug
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Clés secrètes (à remplacer par des variables d'environnement en production)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "my-secret-key-for-jwt-tokens")
    
    # Configuration de la base de données (exemple avec SQLite pour le développement)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    
    # Configuration de n8n
    N8N_API_URL: str = os.getenv("N8N_API_URL", "http://n8n:5678")
    N8N_API_KEY: str = os.getenv("N8N_API_KEY", "")
    
    # Configuration de Windmill
    WINDMILL_API_URL: str = os.getenv("WINDMILL_API_URL", "http://windmill:8000")
    WINDMILL_API_KEY: str = os.getenv("WINDMILL_API_KEY", "")
    
    # Configuration de Terraform
    TERRAFORM_WORKING_DIR: str = os.getenv("TERRAFORM_WORKING_DIR", "/tmp/terraform")
    
    class Config:
        case_sensitive = True

# Créer une instance des paramètres
settings = Settings()