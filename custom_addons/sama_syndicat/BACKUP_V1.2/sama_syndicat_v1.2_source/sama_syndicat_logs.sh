#!/bin/bash

# Script pour extraire les logs spécifiques au module SAMA SYNDICAT

echo "📋 LOGS SPÉCIFIQUES - SAMA SYNDICAT"
echo "==================================="
echo ""

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

LOG_FILE="/var/log/odoo/odoo.log"
OUTPUT_FILE="sama_syndicat_logs_$(date +%Y%m%d_%H%M%S).txt"

if [ ! -f "$LOG_FILE" ]; then
    echo -e "${RED}❌ Fichier de log non trouvé: $LOG_FILE${NC}"
    exit 1
fi

echo -e "${BLUE}🔍 Recherche des logs sama_syndicat...${NC}"
echo ""

# Créer le fichier de sortie
cat > "$OUTPUT_FILE" << EOF
LOGS SAMA SYNDICAT - $(date)
============================

EOF

# 1. Rechercher toutes les mentions de sama_syndicat
echo -e "${YELLOW}📊 MENTIONS DIRECTES DE 'sama_syndicat':${NC}"
DIRECT_MENTIONS=$(grep -i "sama_syndicat" "$LOG_FILE" | wc -l)
echo "Nombre total de mentions: $DIRECT_MENTIONS"

if [ $DIRECT_MENTIONS -gt 0 ]; then
    echo ""
    echo "Détails des mentions:"
    grep -i "sama_syndicat" "$LOG_FILE" | tail -20
    
    # Ajouter au fichier de sortie
    echo "=== MENTIONS DIRECTES ===" >> "$OUTPUT_FILE"
    grep -i "sama_syndicat" "$LOG_FILE" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
else
    echo -e "${GREEN}✅ Aucune mention directe trouvée${NC}"
fi

echo ""
echo -e "${YELLOW}📊 RECHERCHE PAR PATTERNS SPÉCIFIQUES:${NC}"

# 2. Rechercher les logs liés au port 8070 (notre port)
echo ""
echo -e "${BLUE}🔌 Logs du port 8070:${NC}"
PORT_LOGS=$(grep "8070" "$LOG_FILE" | wc -l)
echo "Mentions du port 8070: $PORT_LOGS"

if [ $PORT_LOGS -gt 0 ]; then
    echo "Dernières activités sur le port 8070:"
    grep "8070" "$LOG_FILE" | tail -10
    
    echo "=== LOGS PORT 8070 ===" >> "$OUTPUT_FILE"
    grep "8070" "$LOG_FILE" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
fi

# 3. Rechercher les logs de la base de données sama_syndicat
echo ""
echo -e "${BLUE}🗄️ Logs de la base de données:${NC}"
DB_LOGS=$(grep -i "sama_syndicat_final" "$LOG_FILE" | wc -l)
echo "Mentions de la base sama_syndicat_final: $DB_LOGS"

if [ $DB_LOGS -gt 0 ]; then
    echo "Dernières activités de la base:"
    grep -i "sama_syndicat_final" "$LOG_FILE" | tail -10
    
    echo "=== LOGS BASE DE DONNÉES ===" >> "$OUTPUT_FILE"
    grep -i "sama_syndicat_final" "$LOG_FILE" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
fi

# 4. Rechercher les logs du répertoire du module
echo ""
echo -e "${BLUE}📁 Logs du répertoire du module:${NC}"
DIR_LOGS=$(grep -i "/tmp/addons_sama_syndicat\|/home/grand-as/psagsn/custom_addons/sama_syndicat" "$LOG_FILE" | wc -l)
echo "Mentions du répertoire: $DIR_LOGS"

if [ $DIR_LOGS -gt 0 ]; then
    echo "Accès au répertoire du module:"
    grep -i "/tmp/addons_sama_syndicat\|/home/grand-as/psagsn/custom_addons/sama_syndicat" "$LOG_FILE" | tail -10
    
    echo "=== LOGS RÉPERTOIRE MODULE ===" >> "$OUTPUT_FILE"
    grep -i "/tmp/addons_sama_syndicat\|/home/grand-as/psagsn/custom_addons/sama_syndicat" "$LOG_FILE" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
fi

# 5. Rechercher les logs de chargement de modules
echo ""
echo -e "${BLUE}⚙️ Logs de chargement de modules:${NC}"
MODULE_LOADING=$(grep -i "loading.*sama" "$LOG_FILE" | wc -l)
echo "Chargements de modules sama: $MODULE_LOADING"

if [ $MODULE_LOADING -gt 0 ]; then
    echo "Chargements de modules:"
    grep -i "loading.*sama" "$LOG_FILE" | tail -10
    
    echo "=== LOGS CHARGEMENT MODULES ===" >> "$OUTPUT_FILE"
    grep -i "loading.*sama" "$LOG_FILE" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
fi

# 6. Rechercher les erreurs liées aux modèles syndicat.*
echo ""
echo -e "${BLUE}🏗️ Logs des modèles syndicat.*:${NC}"
MODEL_LOGS=$(grep -i "syndicat\." "$LOG_FILE" | wc -l)
echo "Mentions des modèles syndicat.*: $MODEL_LOGS"

if [ $MODEL_LOGS -gt 0 ]; then
    echo "Activités des modèles syndicat:"
    grep -i "syndicat\." "$LOG_FILE" | tail -15
    
    echo "=== LOGS MODÈLES SYNDICAT ===" >> "$OUTPUT_FILE"
    grep -i "syndicat\." "$LOG_FILE" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
fi

# 7. Rechercher les logs récents (dernières 24h)
echo ""
echo -e "${BLUE}🕐 Logs récents (dernières 24h):${NC}"
TODAY=$(date +"%Y-%m-%d")
YESTERDAY=$(date -d "yesterday" +"%Y-%m-%d")

RECENT_SAMA=$(grep -E "$TODAY|$YESTERDAY" "$LOG_FILE" | grep -i "sama" | wc -l)
echo "Logs sama récents: $RECENT_SAMA"

if [ $RECENT_SAMA -gt 0 ]; then
    echo "Activités récentes:"
    grep -E "$TODAY|$YESTERDAY" "$LOG_FILE" | grep -i "sama" | tail -10
    
    echo "=== LOGS RÉCENTS ===" >> "$OUTPUT_FILE"
    grep -E "$TODAY|$YESTERDAY" "$LOG_FILE" | grep -i "sama" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
fi

# 8. Analyser les types de logs
echo ""
echo -e "${YELLOW}📈 ANALYSE PAR TYPE DE LOG:${NC}"

# Compter les différents types
INFO_COUNT=$(grep -i "sama" "$LOG_FILE" | grep -i "INFO" | wc -l)
ERROR_COUNT=$(grep -i "sama" "$LOG_FILE" | grep -i "ERROR" | wc -l)
WARNING_COUNT=$(grep -i "sama" "$LOG_FILE" | grep -i "WARNING" | wc -l)
DEBUG_COUNT=$(grep -i "sama" "$LOG_FILE" | grep -i "DEBUG" | wc -l)

echo "INFO: $INFO_COUNT"
echo "ERROR: $ERROR_COUNT"
echo "WARNING: $WARNING_COUNT"
echo "DEBUG: $DEBUG_COUNT"

# 9. Créer un résumé
echo ""
echo -e "${GREEN}📋 RÉSUMÉ SAMA SYNDICAT:${NC}"
echo "========================"
echo "Mentions directes: $DIRECT_MENTIONS"
echo "Logs port 8070: $PORT_LOGS"
echo "Logs base de données: $DB_LOGS"
echo "Logs répertoire: $DIR_LOGS"
echo "Logs chargement: $MODULE_LOADING"
echo "Logs modèles: $MODEL_LOGS"
echo "Logs récents: $RECENT_SAMA"
echo ""
echo "Types de logs:"
echo "- INFO: $INFO_COUNT"
echo "- ERROR: $ERROR_COUNT"
echo "- WARNING: $WARNING_COUNT"
echo "- DEBUG: $DEBUG_COUNT"

# Ajouter le résumé au fichier
cat >> "$OUTPUT_FILE" << EOF

=== RÉSUMÉ ===
Mentions directes: $DIRECT_MENTIONS
Logs port 8070: $PORT_LOGS
Logs base de données: $DB_LOGS
Logs répertoire: $DIR_LOGS
Logs chargement: $MODULE_LOADING
Logs modèles: $MODEL_LOGS
Logs récents: $RECENT_SAMA

Types de logs:
- INFO: $INFO_COUNT
- ERROR: $ERROR_COUNT
- WARNING: $WARNING_COUNT
- DEBUG: $DEBUG_COUNT
EOF

echo ""
echo -e "${GREEN}✅ Analyse terminée!${NC}"
echo -e "${BLUE}📄 Rapport sauvegardé dans: $OUTPUT_FILE${NC}"

# Afficher les dernières lignes du fichier de sortie
echo ""
echo -e "${YELLOW}📖 Aperçu du rapport:${NC}"
echo "===================="
tail -20 "$OUTPUT_FILE"