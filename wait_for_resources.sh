#!/bin/bash

# Script pour attendre que les ressources système soient en dessous des seuils avant d'exécuter une commande.

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

# Fonction pour vérifier si une commande existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Fonction pour vérifier les ressources
check_resources() {
    # Vérifier si psutil est installé
    if ! python3 -c "import psutil" 2>/dev/null; then
        error "psutil n'est pas installé. Veuillez exécuter le script d'installation : /home/coder/install_throttler.sh"
        return 1
    fi
    
    # Vérifier les ressources avec le script Python
    python3 /home/coder/resource_monitor.py --once --cpu-threshold 90 --load-avg-threshold 6
    
    # Retourner le code d'erreur du script Python
    return $?
}

# Fonction pour attendre que les ressources soient OK
wait_for_resources() {
    local max_wait_time=${1:-60}
    local check_interval=${2:-5}
    local start_time=$(date +%s)
    
    log "Surveillance des ressources (seuils: CPU < 90%, Load Avg 5min < 6)..."
    
    while true; do
        if check_resources; then
            log "Ressources OK, continuation..."
            return 0
        else
            local current_time=$(date +%s)
            local elapsed_time=$((current_time - start_time))
            
            if [ $elapsed_time -ge $max_wait_time ]; then
                error "Temps d'attente maximum dépassé."
                return 1
            fi
            
            warn "Ressources élevées, attente de $check_interval secondes..."
            sleep $check_interval
        fi
    done
}

# Fonction principale
main() {
    # Si aucun argument n'est passé, vérifier les ressources et sortir
    if [ $# -eq 0 ]; then
        check_resources
        exit $?
    fi
    
    # Si le premier argument est "--wait", attendre que les ressources soient OK
    if [ "$1" = "--wait" ]; then
        shift
        if ! wait_for_resources; then
            error "Impossible d'atteindre les seuils de ressources nécessaires."
            exit 1
        fi
    fi
    
    # Exécuter la commande passée en argument
    log "Exécution de la commande : $*"
    "$@"
}

# Exécuter la fonction principale
main "$@"