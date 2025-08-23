#!/bin/bash

# Script pour installer le throttler de CPU et de load average
# Auteur: dr-basalt
# Date: 2025-08-23

set -e  # Arrêter le script si une commande échoue

echo "=== Installation du CPU et Load Average Throttler ==="

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

# Déterminer le gestionnaire de paquets Python
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    error "pip ou pip3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

log "Utilisation de $PIP_CMD pour l'installation des paquets Python"

# Installer psutil
log "Installation de psutil..."
$PIP_CMD install psutil

# Vérifier l'installation
if python3 -c "import psutil" 2>/dev/null; then
    log "psutil installé avec succès"
else
    error "Échec de l'installation de psutil"
    exit 1
fi

# Créer un alias pour activer le throttling par défaut
log "Configuration de l'alias pour le throttling..."
echo "" >> ~/.bashrc
echo "# Alias pour le throttling CPU/load average" >> ~/.bashrc
echo "alias throttle-on='export THROTTLE_DISABLE=false'" >> ~/.bashrc
echo "alias throttle-off='export THROTTLE_DISABLE=true'" >> ~/.bashrc
echo "" >> ~/.bashrc

# Activer le throttling par défaut
log "Activation du throttling par défaut..."
echo "export THROTTLE_DISABLE=false" >> ~/.bashrc

log "Installation terminée avec succès !"

echo ""
echo "Pour utiliser le throttling :"
echo "  - Il est activé par défaut"
echo "  - Pour le désactiver temporairement : export THROTTLE_DISABLE=true"
echo "  - Pour le réactiver : export THROTTLE_DISABLE=false"
echo ""
echo "Vous pouvez aussi utiliser les alias :"
echo "  - throttle-on : Activer le throttling"
echo "  - throttle-off : Désactiver le throttling"
echo ""
echo "Pour que les changements soient pris en compte, exécutez :"
echo "  source ~/.bashrc"
echo ""
echo "Ou redémarrez votre terminal."