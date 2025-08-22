#cloud-config
hostname: ${instance_name}
manage_etc_hosts: true

users:
  - name: ${ssh_user}
    sudo: ['ALL=(ALL) NOPASSWD:ALL']
    ssh-authorized-keys:
      - ${ssh_authorized_key}

packages:
  - curl
  - wget
  - git
  - vim
  - htop
  - jq

runcmd:
  - echo "Cloud-init terminé pour ${instance_name}"