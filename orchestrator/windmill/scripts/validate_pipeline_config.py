import json
from typing import Dict, Any

def main(pipeline_config: Dict[str, Any], pipeline_nodes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Script pour valider la configuration d'un pipeline.
    
    Args:
        pipeline_config: Configuration du pipeline.
        pipeline_nodes: Nodes du pipeline.
        
    Returns:
        Résultat de la validation.
    """
    try:
        # 1. Valider la configuration du pipeline
        if not pipeline_config.get("pipeline_name"):
            raise ValueError("Le nom du pipeline est requis.")
        
        if not pipeline_config.get("target_platform"):
            raise ValueError("La plateforme cible est requise.")
        
        # 2. Valider les nodes du pipeline
        if not pipeline_nodes:
            raise ValueError("Les nodes du pipeline sont requis.")
        
        # 3. Valider les types de nodes
        valid_node_types = ["data_source", "preprocessing", "model", "deployment"]
        for node in pipeline_nodes.get("nodes", []):
            if node.get("type") not in valid_node_types:
                raise ValueError(f"Type de node non valide: {node.get('type')}")
        
        # 4. Retourner un message de succès
        return {
            "status": "success",
            "message": "Configuration du pipeline validée avec succès."
        }
        
    except Exception as e:
        # En cas d"erreur, retourner un message d"erreur
        return {
            "status": "error",
            "message": f"Erreur lors de la validation de la configuration du pipeline: {str(e)}"
        }