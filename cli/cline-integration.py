#!/usr/bin/env python3
# Intégration Cline CLI avec l'Autopilot Engine
# Auteur: Qwen3 Coder
# Date: 2025-08-25

import argparse
import asyncio
import httpx
import json
import os
import sys
from typing import Dict, Any, Optional

# Configuration
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://localhost:8000/api/v1")
CLINE_CONFIG_PATH = os.path.expanduser("~/.config/cline/config.yaml")

class ClineIntegration:
    def __init__(self, api_gateway_url: str = API_GATEWAY_URL):
        self.api_gateway_url = api_gateway_url
        self.client = httpx.AsyncClient(timeout=300.0)
    
    async def analyze_blueprint(self, blueprint: str) -> Dict[str, Any]:
        """Analyse un blueprint avec le LLM de raisonnement."""
        url = f"{self.api_gateway_url}/autopilot/analyze-blueprint"
        response = await self.client.post(url, json=blueprint)
        response.raise_for_status()
        return response.json()
    
    async def generate_project(self, blueprint: str, target_repo: str, 
                             stack: Optional[str] = None, 
                             ui_system: str = "shadcn",
                             autopilot: bool = True, 
                             deploy: bool = False) -> Dict[str, Any]:
        """Génère un projet à partir d'un blueprint."""
        url = f"{self.api_gateway_url}/autopilot/execute-blueprint"
        
        payload = {
            "blueprint": blueprint,
            "target_repo": target_repo,
            "stack": stack,
            "ui_system": ui_system,
            "autopilot": autopilot,
            "deploy": deploy
        }
        
        response = await self.client.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    async def close(self):
        """Ferme le client HTTP."""
        await self.client.aclose()

async def main():
    parser = argparse.ArgumentParser(description="Intégration Cline CLI avec l'Autopilot Engine")
    parser.add_argument("command", choices=["analyze", "generate"], help="Commande à exécuter")
    parser.add_argument("--blueprint", "-b", required=True, help="Description du projet")
    parser.add_argument("--target-repo", "-r", help="URL du repository cible")
    parser.add_argument("--stack", "-s", help="Stack technologique")
    parser.add_argument("--ui-system", "-u", default="shadcn", help="Système UI")
    parser.add_argument("--autopilot", "-a", action="store_true", help="Activer le mode autopilot")
    parser.add_argument("--deploy", "-d", action="store_true", help="Déployer automatiquement")
    
    args = parser.parse_args()
    
    # Initialiser l'intégration
    cline = ClineIntegration()
    
    try:
        if args.command == "analyze":
            print("Analyse du blueprint en cours...")
            result = await cline.analyze_blueprint(args.blueprint)
            print(json.dumps(result, indent=2))
        
        elif args.command == "generate":
            if not args.target_repo:
                print("Erreur: --target-repo est requis pour la commande 'generate'", file=sys.stderr)
                sys.exit(1)
            
            print("Génération du projet en cours...")
            result = await cline.generate_project(
                blueprint=args.blueprint,
                target_repo=args.target_repo,
                stack=args.stack,
                ui_system=args.ui_system,
                autopilot=args.autopilot,
                deploy=args.deploy
            )
            print(json.dumps(result, indent=2))
    
    except httpx.HTTPStatusError as e:
        print(f"Erreur HTTP: {e.response.status_code} - {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Erreur: {str(e)}", file=sys.stderr)
        sys.exit(1)
    finally:
        await cline.close()

if __name__ == "__main__":
    asyncio.run(main())