#!/usr/bin/env python3
# AutoPush Engine pour l'Autopilot Engine
# Auteur: Qwen3 Coder
# Date: 2025-08-25

import asyncio
import httpx
import json
import os
import subprocess
import tempfile
import shutil
from typing import Dict, Any, Optional
from pathlib import Path

# Configuration
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://localhost:8000/api/v1")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN", "")

class GitProvider:
    """Classe de base pour les providers Git."""
    
    def __init__(self, token: str):
        self.token = token
    
    async def create_repository(self, name: str, private: bool = True) -> str:
        """Crée un repository et retourne l'URL clone."""
        raise NotImplementedError
    
    async def push_code(self, repo_url: str, codebase: Dict[str, Any]) -> None:
        """Push le code dans le repository."""
        raise NotImplementedError

class GitHubProvider(GitProvider):
    """Implémentation pour GitHub."""
    
    def __init__(self, token: str):
        super().__init__(token)
        self.client = httpx.AsyncClient(
            headers={"Authorization": f"token {token}"}
        )
    
    async def create_repository(self, name: str, private: bool = True) -> str:
        """Crée un repository GitHub."""
        url = "https://api.github.com/user/repos"
        payload = {
            "name": name,
            "private": private,
            "auto_init": False
        }
        
        response = await self.client.post(url, json=payload)
        response.raise_for_status()
        repo_data = response.json()
        return repo_data["clone_url"]
    
    async def push_code(self, repo_url: str, codebase: Dict[str, Any]) -> None:
        """Push le code dans le repository GitHub."""
        # Créer un répertoire temporaire
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir) / "repo"
            
            # Initialiser le repository git
            subprocess.run(["git", "init"], cwd=temp_dir, check=True)
            subprocess.run(["git", "remote", "add", "origin", repo_url], cwd=temp_dir, check=True)
            
            # Créer les fichiers
            for filename, content in codebase.items():
                file_path = repo_path / filename
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, "w") as f:
                    f.write(content)
            
            # Commit et push
            subprocess.run(["git", "add", "."], cwd=temp_dir, check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit from Autopilot Engine"], cwd=temp_dir, check=True)
            subprocess.run(["git", "push", "-u", "origin", "main"], cwd=temp_dir, check=True)

class GitLabProvider(GitProvider):
    """Implémentation pour GitLab."""
    
    def __init__(self, token: str):
        super().__init__(token)
        self.client = httpx.AsyncClient(
            headers={"PRIVATE-TOKEN": token}
        )
    
    async def create_repository(self, name: str, private: bool = True) -> str:
        """Crée un repository GitLab."""
        url = "https://gitlab.com/api/v4/projects"
        visibility = "private" if private else "public"
        payload = {
            "name": name,
            "visibility": visibility
        }
        
        response = await self.client.post(url, json=payload)
        response.raise_for_status()
        repo_data = response.json()
        return repo_data["http_url_to_repo"]
    
    async def push_code(self, repo_url: str, codebase: Dict[str, Any]) -> None:
        """Push le code dans le repository GitLab."""
        # Créer un répertoire temporaire
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir) / "repo"
            
            # Initialiser le repository git
            subprocess.run(["git", "init"], cwd=temp_dir, check=True)
            subprocess.run(["git", "remote", "add", "origin", repo_url], cwd=temp_dir, check=True)
            
            # Créer les fichiers
            for filename, content in codebase.items():
                file_path = repo_path / filename
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, "w") as f:
                    f.write(content)
            
            # Commit et push
            subprocess.run(["git", "add", "."], cwd=temp_dir, check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit from Autopilot Engine"], cwd=temp_dir, check=True)
            subprocess.run(["git", "push", "-u", "origin", "main"], cwd=temp_dir, check=True)

class AutoPushEngine:
    """Moteur d'auto-push pour l'Autopilot Engine."""
    
    def __init__(self):
        self.providers = {}
        if GITHUB_TOKEN:
            self.providers["github"] = GitHubProvider(GITHUB_TOKEN)
        if GITLAB_TOKEN:
            self.providers["gitlab"] = GitLabProvider(GITLAB_TOKEN)
    
    def _get_provider_from_url(self, url: str) -> Optional[GitProvider]:
        """Détermine le provider à partir de l'URL."""
        if "github.com" in url:
            return self.providers.get("github")
        elif "gitlab.com" in url:
            return self.providers.get("gitlab")
        return None
    
    async def create_and_push(self, codebase: Dict[str, Any], target_repo: str, 
                            auto_deploy: bool = False) -> str:
        """Crée un repository et push le code."""
        # Si le repository existe déjà, on push dedans
        if target_repo.startswith("http"):
            provider = self._get_provider_from_url(target_repo)
            if provider:
                await provider.push_code(target_repo, codebase)
                return target_repo
            else:
                raise ValueError(f"Provider non supporté pour l'URL: {target_repo}")
        
        # Sinon, on crée un nouveau repository
        else:
            # Déterminer le provider à utiliser (priorité à GitHub)
            provider = self.providers.get("github") or self.providers.get("gitlab")
            if not provider:
                raise ValueError("Aucun provider Git configuré")
            
            # Créer le repository
            repo_name = target_repo.split("/")[-1]
            repo_url = await provider.create_repository(repo_name)
            
            # Push le code
            await provider.push_code(repo_url, codebase)
            
            return repo_url

async def main():
    """Exemple d'utilisation de l'AutoPush Engine."""
    # Exemple de codebase généré
    codebase = {
        "main.py": "print('Hello, World!')",
        "README.md": "# Generated Project\n\nThis is a generated project.",
        "requirements.txt": "fastapi\nuvicorn"
    }
    
    # Initialiser l'engine
    engine = AutoPushEngine()
    
    # Créer et push le code
    try:
        repo_url = await engine.create_and_push(
            codebase, 
            "test-project", 
            auto_deploy=False
        )
        print(f"Code pushed to: {repo_url}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())