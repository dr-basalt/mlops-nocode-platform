# Module Terraform pour déployer des instances Vast.ai
# Auteur: dr-basalt
# Date: 2025-08-22

# Ressource pour créer une instance Vast.ai
resource "null_resource" "vastai_instance" {
  count = var.instance_count

  triggers = {
    # Recréer la ressource si la configuration change
    instance_config = jsonencode(var.instance_config)
  }

  provisioner "local-exec" {
    command = <<EOT
      python3 ${path.module}/scripts/vastai_client.py create ${path.module}/templates/instance-config.json
    EOT

    environment = {
      VASTAI_API_KEY = var.vastai_api_key
    }
  }

  provisioner "local-exec" {
    when    = destroy
    command = <<EOT
      python3 ${path.module}/scripts/vastai_client.py destroy $${self.triggers.instance_id}
    EOT

    environment = {
      VASTAI_API_KEY = var.vastai_api_key
    }
  }
}

# Template pour la configuration de l'instance
data "template_file" "instance_config" {
  template = file("${path.module}/templates/instance-config.json.tpl")

  vars = {
    image           = var.instance_config.image
    disk_space      = var.instance_config.disk_space
    gpu_type        = var.instance_config.gpu_type
    gpu_count       = var.instance_config.gpu_count
    cpu_count       = var.instance_config.cpu_count
    ram             = var.instance_config.ram
    ssh_port        = var.instance_config.ssh_port
    label           = var.instance_config.label
  }
}

# Écrire la configuration de l'instance dans un fichier
resource "local_file" "instance_config" {
  content  = data.template_file.instance_config.rendered
  filename = "${path.module}/templates/instance-config.json"
}