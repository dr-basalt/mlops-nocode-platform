# Module Terraform pour déployer des instances Exoscale
# Auteur: dr-basalt
# Date: 2025-08-22

# Fournisseur Exoscale
provider "exoscale" {
  key    = var.exoscale_key
  secret = var.exoscale_secret
}

# Instance Compute
resource "exoscale_compute" "instance" {
  count = var.instance_count

  zone        = var.zone
  name        = "${var.instance_name}-${count.index}"
  display_name = "${var.instance_name}-${count.index}"
  template    = var.template
  size        = var.size
  disk_size   = var.disk_size
  key_pair    = var.key_pair
  security_groups = var.security_groups
  user_data   = data.template_file.user_data.rendered

  connection {
    type        = "ssh"
    user        = var.ssh_user
    private_key = file(var.ssh_private_key_path)
    host        = self.ip_address
  }

  # Provisionner l'instance avec des scripts
  provisioner "remote-exec" {
    inline = [
      "sudo hostnamectl set-hostname ${var.instance_name}-${count.index}",
      "sudo apt-get update",
      "sudo apt-get install -y curl wget git vim htop jq"
    ]
  }
}

# Groupe de sécurité
resource "exoscale_security_group" "sg" {
  count = length(var.security_groups) > 0 ? 0 : 1

  name        = "${var.instance_name}-sg"
  description = "Groupe de sécurité pour ${var.instance_name}"
}

# Règles de sécurité (exemple pour SSH et HTTP)
resource "exoscale_security_group_rule" "ssh" {
  count = length(var.security_groups) > 0 ? 0 : 1

  security_group_id = exoscale_security_group.sg[0].id
  type              = "INGRESS"
  protocol          = "TCP"
  start_port        = 22
  end_port          = 22
  cidr              = "0.0.0.0/0" # À restreindre en production
}

resource "exoscale_security_group_rule" "http" {
  count = length(var.security_groups) > 0 ? 0 : 1

  security_group_id = exoscale_security_group.sg[0].id
  type              = "INGRESS"
  protocol          = "TCP"
  start_port        = 80
  end_port          = 80
  cidr              = "0.0.0.0/0" # À restreindre en production
}

resource "exoscale_security_group_rule" "https" {
  count = length(var.security_groups) > 0 ? 0 : 1

  security_group_id = exoscale_security_group.sg[0].id
  type              = "INGRESS"
  protocol          = "TCP"
  start_port        = 443
  end_port          = 443
  cidr              = "0.0.0.0/0" # À restreindre en production
}

# Template pour les données utilisateur (cloud-init)
data "template_file" "user_data" {
  template = file("${path.module}/templates/user-data.tpl")

  vars = {
    ssh_authorized_key = var.ssh_authorized_key
  }
}