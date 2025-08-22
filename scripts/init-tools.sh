#!/bin/bash

# Script d'initialisation des outils pour la plateforme MLOps No-Code
# Auteur: dr-basalt
# Date: 2025-08-22

set -e  # Arrêter le script si une commande échoue

echo "=== Initialisation des outils ==="

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier si l'utilisateur est root (pour certaines installations)
if [[ $EUID -eq 0 ]]; then
   error "Ce script ne doit pas être exécuté en tant que root"
   exit 1
fi

# Déterminer l'architecture du système
ARCH=$(uname -m)
if [[ "$ARCH" == "x86_64" ]]; then
    ARCH="amd64"
elif [[ "$ARCH" == "aarch64" ]]; then
    ARCH="arm64"
else
    error "Architecture non supportée: $ARCH"
    exit 1
fi

log "Architecture détectée: $ARCH"

# Créer un répertoire temporaire pour les téléchargements
TMP_DIR=$(mktemp -d)
log "Répertoire temporaire: $TMP_DIR"
trap 'rm -rf "$TMP_DIR"' EXIT

# Fonction pour télécharger et extraire une archive tar.gz
download_and_extract() {
    local url=$1
    local target_dir=$2
    local binary_name=$3
    
    log "Téléchargement de $binary_name..."
    wget -q -O "$TMP_DIR/${binary_name}.tar.gz" "$url"
    tar -xzf "$TMP_DIR/${binary_name}.tar.gz" -C "$TMP_DIR"
    
    # Déplacer le binaire vers le répertoire cible
    mkdir -p "$target_dir"
    mv "$TMP_DIR/$binary_name" "$target_dir/"
    chmod +x "$target_dir/$binary_name"
    
    log "$binary_name installé dans $target_dir"
}

# Fonction pour vérifier si un outil est déjà installé
is_installed() {
    command -v "$1" >/dev/null 2>&1
}

# Installer Terraform
install_terraform() {
    if is_installed "terraform"; then
        warn "Terraform est déjà installé"
        terraform version
        return
    fi
    
    log "Installation de Terraform..."
    # Version de Terraform à installer
    TERRAFORM_VERSION="1.5.7"
    
    # URL de téléchargement
    TERRAFORM_URL="https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_${ARCH}.zip"
    
    # Télécharger Terraform
    log "Téléchargement de Terraform $TERRAFORM_VERSION..."
    wget -q -O "$TMP_DIR/terraform.zip" "$TERRAFORM_URL"
    
    # Extraire Terraform
    unzip -q "$TMP_DIR/terraform.zip" -d "$TMP_DIR"
    
    # Déplacer Terraform vers /usr/local/bin
    sudo mkdir -p /usr/local/bin
    sudo mv "$TMP_DIR/terraform" /usr/local/bin/
    sudo chmod +x /usr/local/bin/terraform
    
    log "Terraform $TERRAFORM_VERSION installé avec succès"
    terraform version
}

# Installer kubectl
install_kubectl() {
    if is_installed "kubectl"; then
        warn "kubectl est déjà installé"
        kubectl version --client
        return
    fi
    
    log "Installation de kubectl..."
    # Version de kubectl à installer (correspond à la version de K3s recommandée)
    KUBECTL_VERSION="v1.27.1"
    
    # URL de téléchargement
    KUBECTL_URL="https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/${ARCH}/kubectl"
    
    # Télécharger kubectl
    log "Téléchargement de kubectl $KUBECTL_VERSION..."
    wget -q -O "$TMP_DIR/kubectl" "$KUBECTL_URL"
    
    # Déplacer kubectl vers /usr/local/bin
    sudo mkdir -p /usr/local/bin
    sudo mv "$TMP_DIR/kubectl" /usr/local/bin/
    sudo chmod +x /usr/local/bin/kubectl
    
    log "kubectl $KUBECTL_VERSION installé avec succès"
    kubectl version --client
}

# Installer Helm
install_helm() {
    if is_installed "helm"; then
        warn "Helm est déjà installé"
        helm version
        return
    fi
    
    log "Installation de Helm..."
    # Version de Helm à installer
    HELM_VERSION="v3.12.0"
    
    # URL de téléchargement
    HELM_URL="https://get.helm.sh/helm-${HELM_VERSION}-linux-${ARCH}.tar.gz"
    
    # Télécharger Helm
    log "Téléchargement de Helm $HELM_VERSION..."
    wget -q -O "$TMP_DIR/helm.tar.gz" "$HELM_URL"
    
    # Extraire Helm
    tar -xzf "$TMP_DIR/helm.tar.gz" -C "$TMP_DIR"
    
    # Déplacer Helm vers /usr/local/bin
    sudo mkdir -p /usr/local/bin
    sudo mv "$TMP_DIR/linux-${ARCH}/helm" /usr/local/bin/
    sudo chmod +x /usr/local/bin/helm
    
    log "Helm $HELM_VERSION installé avec succès"
    helm version
}

# Installer Docker (si nécessaire)
install_docker() {
    if is_installed "docker"; then
        warn "Docker est déjà installé"
        docker --version
        return
    fi
    
    log "Installation de Docker..."
    # Utiliser le script d'installation officiel
    curl -fsSL https://get.docker.com -o "$TMP_DIR/get-docker.sh"
    sh "$TMP_DIR/get-docker.sh"
    
    # Ajouter l'utilisateur courant au groupe docker
    sudo usermod -aG docker $USER
    
    log "Docker installé avec succès"
    docker --version
}

# Installer Docker Compose
install_docker_compose() {
    if is_installed "docker-compose"; then
        warn "Docker Compose est déjà installé"
        docker-compose --version
        return
    fi
    
    log "Installation de Docker Compose..."
    # Version de Docker Compose à installer
    DOCKER_COMPOSE_VERSION="v2.20.0"
    
    # URL de téléchargement
    DOCKER_COMPOSE_URL="https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-linux-${ARCH}"
    
    # Télécharger Docker Compose
    log "Téléchargement de Docker Compose $DOCKER_COMPOSE_VERSION..."
    sudo wget -q -O /usr/local/bin/docker-compose "$DOCKER_COMPOSE_URL"
    
    # Rendre le binaire exécutable
    sudo chmod +x /usr/local/bin/docker-compose
    
    log "Docker Compose $DOCKER_COMPOSE_VERSION installé avec succès"
    docker-compose --version
}

# Installer K3s
install_k3s() {
    log "Installation de K3s..."
    # Utiliser le script d'installation officiel
    curl -sfL https://get.k3s.io | sh -
    
    # Attendre que K3s soit prêt
    sleep 10
    
    # Vérifier l'état de K3s
    if systemctl is-active --quiet k3s; then
        log "K3s installé et démarré avec succès"
        kubectl get nodes
    else
        error "K3s n'a pas démarré correctement"
        exit 1
    fi
}

# Fonction principale
main() {
    log "Démarrage de l'installation des outils..."
    
    # Mettre à jour les paquets
    log "Mise à jour des paquets..."
    sudo apt-get update -y
    
    # Installer les dépendances nécessaires
    log "Installation des dépendances..."
    sudo apt-get install -y wget curl unzip tar
    
    # Installer les outils un par un
    install_terraform
    install_kubectl
    install_helm
    install_docker
    install_docker_compose
    install_k3s
    
    log "Installation des outils terminée avec succès!"
    log "Vous pouvez maintenant utiliser la plateforme MLOps No-Code."
}

# Exécuter la fonction principale
main "$@"