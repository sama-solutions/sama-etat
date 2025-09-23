#!/bin/bash

# Script de monitoring en temps réel pour SAMA SYNDICAT

echo "🔍 MONITORING TEMPS RÉEL - SAMA SYNDICAT"
echo "========================================"
echo ""

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

LOG_FILE="/var/log/odoo/odoo.log"

if [ ! -f "$LOG_FILE" ]; then
    echo -e "${RED}❌ Fichier de log non trouvé: $LOG_FILE${NC}"
    exit 1
fi

echo -e "${BLUE}📊 RÉSUMÉ ACTUEL DES LOGS SAMA SYNDICAT${NC}"
echo "======================================"

# Fonction pour afficher les statistiques actuelles
show_current_stats() {
    echo ""
    echo -e "${YELLOW}📈 STATISTIQUES ACTUELLES:${NC}"
    
    # Mentions directes
    DIRECT_MENTIONS=$(grep -i "sama_syndicat" "$LOG_FILE" | wc -l)
    echo "Mentions directes sama_syndicat: $DIRECT_MENTIONS"
    
    # Port 8070
    PORT_LOGS=$(grep "8070" "$LOG_FILE" | wc -l)
    echo "Activités port 8070: $PORT_LOGS"
    
    # Base de données
    DB_LOGS=$(grep -i "sama_syndicat_final" "$LOG_FILE" | wc -l)
    echo "Logs base de données: $DB_LOGS"
    
    # Processus actifs
    ACTIVE_PROCESSES=$(ps aux | grep -i "sama_syndicat\|8070" | grep -v grep | wc -l)
    echo "Processus actifs: $ACTIVE_PROCESSES"
    
    echo ""
    echo -e "${YELLOW}🕐 DERNIÈRES ACTIVITÉS:${NC}"
    
    # Dernières activités du port 8070
    echo "Dernière activité port 8070:"
    grep "8070" "$LOG_FILE" | tail -1 | cut -d' ' -f1-2 || echo "Aucune activité récente"
    
    # Dernière mention sama
    echo "Dernière mention 'sama':"
    grep -i "sama" "$LOG_FILE" | tail -1 | cut -d' ' -f1-2 || echo "Aucune mention récente"
    
    echo ""
}

# Fonction pour surveiller en temps réel
monitor_realtime() {
    echo -e "${GREEN}🔄 SURVEILLANCE EN TEMPS RÉEL${NC}"
    echo "=============================="
    echo "Appuyez sur Ctrl+C pour arrêter"
    echo ""
    
    # Créer un fichier temporaire pour suivre la position
    TEMP_FILE="/tmp/sama_syndicat_monitor_$$"
    echo "0" > "$TEMP_FILE"
    
    while true; do
        # Lire la position actuelle
        LAST_POS=$(cat "$TEMP_FILE")
        
        # Obtenir la taille actuelle du fichier
        CURRENT_SIZE=$(stat -c%s "$LOG_FILE" 2>/dev/null || echo "0")
        
        if [ "$CURRENT_SIZE" -gt "$LAST_POS" ]; then
            # Lire les nouvelles lignes
            NEW_LINES=$(tail -c +$((LAST_POS + 1)) "$LOG_FILE")
            
            # Filtrer les lignes intéressantes
            echo "$NEW_LINES" | while IFS= read -r line; do
                if [[ -n "$line" ]]; then
                    # Vérifier si la ligne contient des mots-clés intéressants
                    if echo "$line" | grep -qi "sama_syndicat\|8070\|syndicat\.\|sama_syndicat_final"; then
                        TIMESTAMP=$(date '+%H:%M:%S')
                        echo -e "${GREEN}[$TIMESTAMP]${NC} ${BLUE}SAMA:${NC} $line"
                    elif echo "$line" | grep -qi "error.*sama\|warning.*sama"; then
                        TIMESTAMP=$(date '+%H:%M:%S')
                        echo -e "${RED}[$TIMESTAMP]${NC} ${RED}ERROR:${NC} $line"
                    elif echo "$line" | grep -qi "loading.*sama\|module.*sama"; then
                        TIMESTAMP=$(date '+%H:%M:%S')
                        echo -e "${YELLOW}[$TIMESTAMP]${NC} ${PURPLE}MODULE:${NC} $line"
                    fi
                fi
            done
            
            # Mettre à jour la position
            echo "$CURRENT_SIZE" > "$TEMP_FILE"
        fi
        
        sleep 2
    done
    
    # Nettoyer
    rm -f "$TEMP_FILE"
}

# Fonction pour afficher l'aide
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -s, --stats     Afficher seulement les statistiques"
    echo "  -m, --monitor   Surveillance en temps réel"
    echo "  -h, --help      Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0              # Statistiques + surveillance"
    echo "  $0 -s           # Statistiques seulement"
    echo "  $0 -m           # Surveillance seulement"
}

# Fonction pour vérifier l'état du serveur
check_server_status() {
    echo -e "${BLUE}🖥️ ÉTAT DU SERVEUR${NC}"
    echo "=================="
    
    # Vérifier si le port 8070 est ouvert
    if lsof -i:8070 >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Port 8070: ACTIF${NC}"
        
        # Afficher les processus
        echo "Processus sur le port 8070:"
        lsof -i:8070 | grep -v COMMAND
    else
        echo -e "${RED}❌ Port 8070: INACTIF${NC}"
    fi
    
    # Vérifier les processus Odoo
    ODOO_PROCESSES=$(ps aux | grep -i odoo | grep -v grep | wc -l)
    if [ $ODOO_PROCESSES -gt 0 ]; then
        echo -e "${GREEN}✅ Processus Odoo: $ODOO_PROCESSES actif(s)${NC}"
    else
        echo -e "${RED}❌ Aucun processus Odoo actif${NC}"
    fi
    
    echo ""
}

# Traitement des arguments
case "${1:-}" in
    -s|--stats)
        check_server_status
        show_current_stats
        exit 0
        ;;
    -m|--monitor)
        monitor_realtime
        exit 0
        ;;
    -h|--help)
        show_help
        exit 0
        ;;
    "")
        # Mode par défaut: stats + monitoring
        check_server_status
        show_current_stats
        echo ""
        monitor_realtime
        ;;
    *)
        echo "Option inconnue: $1"
        show_help
        exit 1
        ;;
esac