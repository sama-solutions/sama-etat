#!/bin/bash

# Script pour surveiller les logs du développement
# ================================================

# Charger la configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

log_info "=== Surveillance des logs Sama Jokoo ==="
log_info "Fichier de log: $LOG_FILE"
log_info "Appuyez sur Ctrl+C pour arrêter"

# Créer le fichier de log s'il n'existe pas
touch "$LOG_FILE"

# Surveiller les logs en temps réel
tail -f "$LOG_FILE" | while read line; do
    # Coloriser les logs selon le niveau
    if [[ $line == *"ERROR"* ]]; then
        echo -e "${RED}$line${NC}"
    elif [[ $line == *"WARNING"* ]]; then
        echo -e "${YELLOW}$line${NC}"
    elif [[ $line == *"INFO"* ]]; then
        echo -e "${BLUE}$line${NC}"
    elif [[ $line == *"DEBUG"* ]]; then
        echo -e "${NC}$line${NC}"
    else
        echo "$line"
    fi
done