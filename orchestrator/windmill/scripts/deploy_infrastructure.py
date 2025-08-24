import json
import os
import subprocess
import tempfile
from typing import Dict, Any

def main(terraform_code: str) -> Dict[str, Any]:
    """
    Script pour déployer l'infrastructure.
    
    Args:
        terraform_code: Code Terraform à déployer.
        
    Returns:
        Résultat du déploiement.
    """
    try:
        # 1. Écrire le code Terraform dans un fichier temporaire
        with tempfile.TemporaryDirectory() as tmpdir:
            terraform_file = os.path.join(tmpdir, "main.tf")
            with open(terraform_file, "w") as f:
                f.write(terraform_code)
            
            # 2. Initialiser Terraform
            print("Initialisation de Terraform...")
            subprocess.run(["terraform", "init"], cwd=tmpdir, check=True)
            
            # 3. Planifier le déploiement
            print("Planification du déploiement...")
            subprocess.run(["terraform", "plan"], cwd=tmpdir, check=True)
            
            # 4. Appliquer le déploiement
            print("Application du déploiement...")
            subprocess.run(["terraform", "apply", "-auto-approve"], cwd=tmpdir, check=True)
        
        # 5. Retourner un message de succès
        return {
            "status": "success",
            "message": "Infrastructure déployée avec succès."
        }
        
    except Exception as e:
        # En cas d"erreur, retourner un message d"erreur
        return {
            "status": "error",
            "message": f"Erreur lors du déploiement de l"infrastructure: {str(e)}"
        }