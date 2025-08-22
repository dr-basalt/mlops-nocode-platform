# Module Terraform pour déployer un cluster K3s
# Auteur: dr-basalt
# Date: 2025-08-22

# Ressource pour provisionner une machine virtuelle (exemple avec libvirt)
# Note: Ce module suppose que vous avez un fournisseur libvirt configuré.
# Vous pouvez l'adapter à d'autres fournisseurs (AWS, GCP, etc.) selon vos besoins.

resource "libvirt_domain" "k3s_master" {
  count = var.master_count

  name = "${var.cluster_name}-master-${count.index}"
  memory = var.master_memory
  vcpu   = var.master_vcpu

  cloudinit = libvirt_cloudinit_disk.k3s_cloudinit.id

  network_interface {
    network_name = var.network_name
    hostname     = "${var.cluster_name}-master-${count.index}"
  }

  disk {
    volume_id = libvirt_volume.k3s_master_volume[count.index].id
  }

  graphics {
    type        = "spice"
    listen_type = "address"
    autoport    = true
  }

  provisioner "remote-exec" {
    inline = [
      "sudo hostnamectl set-hostname ${var.cluster_name}-master-${count.index}",
      "sudo sed -i 's/127.0.1.1.*/127.0.1.1 ${var.cluster_name}-master-${count.index}/' /etc/hosts"
    ]

    connection {
      type        = "ssh"
      user        = var.ssh_user
      private_key = file(var.ssh_private_key_path)
      host        = self.network_interface.0.addresses.0
    }
  }
}

resource "libvirt_domain" "k3s_worker" {
  count = var.worker_count

  name = "${var.cluster_name}-worker-${count.index}"
  memory = var.worker_memory
  vcpu   = var.worker_vcpu

  cloudinit = libvirt_cloudinit_disk.k3s_cloudinit.id

  network_interface {
    network_name = var.network_name
    hostname     = "${var.cluster_name}-worker-${count.index}"
  }

  disk {
    volume_id = libvirt_volume.k3s_worker_volume[count.index].id
  }

  graphics {
    type        = "spice"
    listen_type = "address"
    autoport    = true
  }

  provisioner "remote-exec" {
    inline = [
      "sudo hostnamectl set-hostname ${var.cluster_name}-worker-${count.index}",
      "sudo sed -i 's/127.0.1.1.*/127.0.1.1 ${var.cluster_name}-worker-${count.index}/' /etc/hosts"
    ]

    connection {
      type        = "ssh"
      user        = var.ssh_user
      private_key = file(var.ssh_private_key_path)
      host        = self.network_interface.0.addresses.0
    }
  }
}

# Volumes pour les machines virtuelles
resource "libvirt_volume" "k3s_master_volume" {
  count = var.master_count

  name   = "${var.cluster_name}-master-${count.index}-volume"
  pool   = var.storage_pool
  size   = var.master_disk_size
  format = "qcow2"
}

resource "libvirt_volume" "k3s_worker_volume" {
  count = var.worker_count

  name   = "${var.cluster_name}-worker-${count.index}-volume"
  pool   = var.storage_pool
  size   = var.worker_disk_size
  format = "qcow2"
}

# Cloud-init pour la configuration initiale des machines
resource "libvirt_cloudinit_disk" "k3s_cloudinit" {
  name           = "${var.cluster_name}-cloudinit.iso"
  pool           = var.storage_pool
  user_data      = data.template_file.user_data.rendered
  network_config = data.template_file.network_config.rendered
}

# Données de template pour cloud-init
data "template_file" "user_data" {
  template = file("${path.module}/templates/user-data.tpl")

  vars = {
    ssh_authorized_key = var.ssh_authorized_key
    k3s_version        = var.k3s_version
    k3s_token          = var.k3s_token
    master_ip          = var.master_count > 0 ? libvirt_domain.k3s_master[0].network_interface.0.addresses.0 : ""
  }
}

data "template_file" "network_config" {
  template = file("${path.module}/templates/network-config.tpl")

  vars = {
    network_name = var.network_name
  }
}

# Script pour installer K3s sur les nœuds
resource "null_resource" "install_k3s_master" {
  count = var.master_count

  depends_on = [libvirt_domain.k3s_master]

  provisioner "remote-exec" {
    inline = [
      "curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=${var.k3s_version} sh -s - server --token ${var.k3s_token} --cluster-init"
    ]

    connection {
      type        = "ssh"
      user        = var.ssh_user
      private_key = file(var.ssh_private_key_path)
      host        = libvirt_domain.k3s_master[count.index].network_interface.0.addresses.0
    }
  }
}

resource "null_resource" "install_k3s_worker" {
  count = var.worker_count

  depends_on = [null_resource.install_k3s_master]

  provisioner "remote-exec" {
    inline = [
      "curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=${var.k3s_version} K3S_URL=https://${libvirt_domain.k3s_master[0].network_interface.0.addresses.0}:6443 K3S_TOKEN=${var.k3s_token} sh -"
    ]

    connection {
      type        = "ssh"
      user        = var.ssh_user
      private_key = file(var.ssh_private_key_path)
      host        = libvirt_domain.k3s_worker[count.index].network_interface.0.addresses.0
    }
  }
}

# Ressource pour récupérer le kubeconfig
resource "null_resource" "get_kubeconfig" {
  depends_on = [null_resource.install_k3s_master]

  provisioner "remote-exec" {
    inline = [
      "sudo cat /etc/rancher/k3s/k3s.yaml"
    ]

    connection {
      type        = "ssh"
      user        = var.ssh_user
      private_key = file(var.ssh_private_key_path)
      host        = libvirt_domain.k3s_master[0].network_interface.0.addresses.0
    }
  }

  provisioner "local-exec" {
    command = "ssh -o StrictHostKeyChecking=no ${var.ssh_user}@${libvirt_domain.k3s_master[0].network_interface.0.addresses.0} 'sudo cat /etc/rancher/k3s/k3s.yaml' > ${var.kubeconfig_output_path}"
  }
}