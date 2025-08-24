import json
from typing import Dict, Any

def main(pipeline_config: Dict[str, Any], pipeline_nodes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Script pour générer le code Terraform.
    
    Args:
        pipeline_config: Configuration du pipeline.
        pipeline_nodes: Nodes du pipeline.
        
    Returns:
        Code Terraform généré.
    """
    try:
        # 1. Générer l"IaC (Terraform)
        print("Génération de l"IaC...")
        terraform_code = generate_terraform_code(pipeline_config, pipeline_nodes)
        
        # 2. Retourner le code Terraform généré
        return {
            "status": "success",
            "message": "Code Terraform généré avec succès.",
            "terraform_code": terraform_code
        }
        
    except Exception as e:
        # En cas d"erreur, retourner un message d"erreur
        return {
            "status": "error",
            "message": f"Erreur lors de la génération du code Terraform: {str(e)}"
        }

def generate_terraform_code(pipeline_config: Dict[str, Any], pipeline_nodes: Dict[str, Any]) -> str:
    """
    Génère le code Terraform pour le déploiement du pipeline.
    
    Args:
        pipeline_config: Configuration du pipeline.
        pipeline_nodes: Nodes du pipeline.
        
    Returns:
        Code Terraform généré.
    """
    target_platform = pipeline_config["target_platform"]
    
    if target_platform == "k3s-local":
        return generate_k3s_terraform_code(pipeline_config, pipeline_nodes)
    elif target_platform == "exoscale":
        return generate_exoscale_terraform_code(pipeline_config, pipeline_nodes)
    elif target_platform == "vastai":
        return generate_vastai_terraform_code(pipeline_config, pipeline_nodes)
    elif target_platform == "runpod":
        return generate_runpod_terraform_code(pipeline_config, pipeline_nodes)
    else:
        raise ValueError(f"Plateforme cible non supportée: {target_platform}")

def generate_k3s_terraform_code(pipeline_config: Dict[str, Any], pipeline_nodes: Dict[str, Any]) -> str:
    """
    Génère le code Terraform pour le déploiement sur K3s local.
    
    Args:
        pipeline_config: Configuration du pipeline.
        pipeline_nodes: Nodes du pipeline.
        
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
    name = "{pipeline_config["pipeline_name"].replace(" ", "-").lower()}"
    labels = {{
      app = "{pipeline_config["pipeline_name"].replace(" ", "-").lower()}"
    }}
  }}

  spec {{
    replicas = 1

    selector {{
      match_labels = {{
        app = "{pipeline_config["pipeline_name"].replace(" ", "-").lower()}"
      }}
    }}

    template {{
      metadata {{
        labels = {{
          app = "{pipeline_config["pipeline_name"].replace(" ", "-").lower()}"
        }}
      }}

      spec {{
        container {{
          image = "nginx:latest"  # Exemple d"image
          name  = "{pipeline_config["pipeline_name"].replace(" ", "-").lower()}"

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
    name = "{pipeline_config["pipeline_name"].replace(" ", "-").lower()}"
  }}

  spec {{
    selector = {{
      app = "{pipeline_config["pipeline_name"].replace(" ", "-").lower()}"
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

def generate_exoscale_terraform_code(pipeline_config: Dict[str, Any], pipeline_nodes: Dict[str, Any]) -> str:
    """
    Génère le code Terraform pour le déploiement sur Exoscale.
    
    Args:
        pipeline_config: Configuration du pipeline.
        pipeline_nodes: Nodes du pipeline.
        
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
  name = "{pipeline_config["pipeline_name"].replace(" ", "-").lower()}"
  type = "standard.medium"
  disk_size = 50
  image = "ubuntu-22.04"
  
  security_group_ids = [
    exoscale_security_group.ml_pipeline.id
  ]
}}

resource "exoscale_security_group" "ml_pipeline" {{
  name = "{pipeline_config["pipeline_name"].replace(" ", "-").lower()}-sg"
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

def generate_vastai_terraform_code(pipeline_config: Dict[str, Any], pipeline_nodes: Dict[str, Any]) -> str:
    """
    Génère le code Terraform pour le déploiement sur Vast.ai.
    
    Args:
        pipeline_config: Configuration du pipeline.
        pipeline_nodes: Nodes du pipeline.
        
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
# pipeline_name = {pipeline_config["pipeline_name"]}
# target_platform = {pipeline_config["target_platform"]}
# nodes = {json.dumps(pipeline_nodes, indent=2)}
"""

def generate_runpod_terraform_code(pipeline_config: Dict[str, Any], pipeline_nodes: Dict[str, Any]) -> str:
    """
    Génère le code Terraform pour le déploiement sur RunPod.
    
    Args:
        pipeline_config: Configuration du pipeline.
        pipeline_nodes: Nodes du pipeline.
        
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
  name            = "{pipeline_config["pipeline_name"].replace(" ", "-").lower()}"
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