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

log "Utilisation de $PIP_CMD pour la gestion des paquets Python"

# Créer un environnement virtuel
VENV_PATH="$HOME/throttler-venv"
log "Création de l'environnement virtuel dans $VENV_PATH..."
python3 -m venv "$VENV_PATH"

# Activer l'environnement virtuel
log "Activation de l'environnement virtuel..."
source "$VENV_PATH/bin/activate"

# Mettre à jour pip dans l'environnement virtuel
log "Mise à jour de pip..."
pip install --upgrade pip

# Installer psutil dans l'environnement virtuel
log "Installation de psutil dans l'environnement virtuel..."
pip install psutil

# Vérifier l'installation
if python3 -c "import psutil" 2>/dev/null; then
    log "psutil installé avec succès dans l'environnement virtuel"
else
    error "Échec de l'installation de psutil dans l'environnement virtuel"
    exit 1
fi

# Copier le script cpu_throttler.py dans l'environnement virtuel pour qu'il puisse trouver psutil
log "Copie du script cpu_throttler.py dans l'environnement virtuel..."
cp /home/coder/cpu_throttler.py "$VENV_PATH/bin/"

# Créer un alias pour activer le throttling par défaut
log "Configuration de l'alias pour le throttling..."
echo "" >> ~/.bashrc
echo "# Alias pour le throttling CPU/load average" >> ~/.bashrc
echo "alias throttle-on='export THROTTLE_DISABLE=false'" >> ~/.bashrc
echo "alias throttle-off='export THROTTLE_DISABLE=true'" >> ~/.bashrc
echo "alias throttle-run='$VENV_PATH/bin/python $VENV_PATH/bin/cpu_throttler.py'" >> ~/.bashrc
echo "" >> ~/.bashrc

# Activer le throttling par défaut
log "Activation du throttling par défaut..."
echo "export THROTTLE_DISABLE=false" >> ~/.bashrc

# Créer un script wrapper pour exécuter des commandes avec throttling
log "Création du script wrapper..."
cat > "$VENV_PATH/bin/throttle-wrapper.sh" << 'EOF'
#!/bin/bash
# Script wrapper pour exécuter des commandes avec throttling

# Activer l'environnement virtuel
source "$HOME/throttler-venv/bin/activate"

# Vérifier les ressources
python "$HOME/throttler-venv/bin/cpu_throttler.py" --cpu-threshold 85 --load-avg-threshold 5 --max-wait-time 10

# Exécuter la commande demandée
"$@"
EOF

chmod +x "$VENV_PATH/bin/throttle-wrapper.sh"

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
echo "  - throttle-run : Exécuter le script de monitoring"
echo ""
echo "Pour exécuter une commande avec throttling :"
echo "  $HOME/throttler-venv/bin/throttle-wrapper.sh python3 votre_script.py"
echo ""
echo "Pour que les changements soient pris en compte, exécutez :"
echo "  source ~/.bashrc"
echo ""
echo "Ou redémarrez votre terminal."