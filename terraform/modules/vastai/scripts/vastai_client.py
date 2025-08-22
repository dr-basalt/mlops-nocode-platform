#!/usr/bin/env python3
"""
Client Python pour l'API Vast.ai
Auteur: dr-basalt
Date: 2025-08-22
"""

import requests
import json
import sys
import os

class VastAIError(Exception):
    """Exception personnalisée pour les erreurs Vast.ai"""
    pass

class VastAIClient:
    """Client pour l'API Vast.ai"""
    
    def __init__(self, api_key):
        """
        Initialise le client Vast.ai.
        
        Args:
            api_key (str): Clé API Vast.ai.
        """
        self.api_key = api_key
        self.base_url = "https://console.vast.ai/api/v0"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def list_instances(self):
        """
        Liste les instances actives.
        
        Returns:
            dict: Réponse de l'API.
        """
        url = f"{self.base_url}/instances/"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise VastAIError(f"Erreur lors de la récupération des instances: {response.status_code} - {response.text}")
    
    def create_instance(self, instance_config):
        """
        Crée une nouvelle instance.
        
        Args:
            instance_config (dict): Configuration de l'instance.
            
        Returns:
            dict: Réponse de l'API.
        """
        url = f"{self.base_url}/instances/"
        response = requests.post(url, headers=self.headers, json=instance_config)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise VastAIError(f"Erreur lors de la création de l'instance: {response.status_code} - {response.text}")
    
    def destroy_instance(self, instance_id):
        """
        Détruit une instance.
        
        Args:
            instance_id (str): ID de l'instance à détruire.
            
        Returns:
            dict: Réponse de l'API.
        """
        url = f"{self.base_url}/instances/{instance_id}/"
        response = requests.delete(url, headers=self.headers)
        if response.status_code in [200, 204]:
            return {"status": "success", "message": f"Instance {instance_id} détruite"}
        else:
            raise VastAIError(f"Erreur lors de la destruction de l'instance: {response.status_code} - {response.text}")

def main():
    """Fonction principale pour l'utilisation en ligne de commande"""
    if len(sys.argv) < 2:
        print("Usage: vastai_client.py <action> [args...]")
        sys.exit(1)
    
    action = sys.argv[1]
    api_key = os.getenv("VASTAI_API_KEY")
    
    if not api_key:
        print("Erreur: VASTAI_API_KEY n'est pas définie.")
        sys.exit(1)
    
    client = VastAIClient(api_key)
    
    try:
        if action == "list":
            result = client.list_instances()
            print(json.dumps(result, indent=2))
        elif action == "create":
            if len(sys.argv) < 3:
                print("Usage: vastai_client.py create <config_file>")
                sys.exit(1)
            config_file = sys.argv[2]
            with open(config_file, 'r') as f:
                config = json.load(f)
            result = client.create_instance(config)
            print(json.dumps(result, indent=2))
        elif action == "destroy":
            if len(sys.argv) < 3:
                print("Usage: vastai_client.py destroy <instance_id>")
                sys.exit(1)
            instance_id = sys.argv[2]
            result = client.destroy_instance(instance_id)
            print(json.dumps(result, indent=2))
        else:
            print(f"Action inconnue: {action}")
            sys.exit(1)
    except VastAIError as e:
        print(f"Erreur Vast.ai: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()