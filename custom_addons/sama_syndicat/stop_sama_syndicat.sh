#!/bin/bash

# Script d'arrêt pour SAMA SYNDICAT

echo "🛑 Arrêt de SAMA SYNDICAT..."

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PORT=8070

# Trouver et arrêter les processus Odoo sur le port 8070
echo -e "${YELLOW}Recherche des processus sur le port $PORT...${NC}"

# Méthode 1: Par port
PIDS_PORT=$(lsof -ti:$PORT 2>/dev/null || true)

# Méthode 2: Par nom de processus
PIDS_ODOO=$(pgrep -f "odoo-bin.*xmlrpc-port=$PORT" 2>/dev/null || true)

# Combiner les PIDs
ALL_PIDS="$PIDS_PORT $PIDS_ODOO"
UNIQUE_PIDS=$(echo $ALL_PIDS | tr ' ' '\n' | sort -u | tr '\n' ' ')

if [ -z "$UNIQUE_PIDS" ]; then
    echo -e "${GREEN}Aucun processus SAMA SYNDICAT trouvé sur le port $PORT${NC}"
    exit 0
fi

echo -e "${YELLOW}Processus trouvés: $UNIQUE_PIDS${NC}"

# Arrêt propre avec SIGTERM
echo -e "${YELLOW}Arrêt propre des processus...${NC}"
for PID in $UNIQUE_PIDS; do
    if [ ! -z "$PID" ]; then
        echo "Arrêt du processus $PID..."
        kill -TERM $PID 2>/dev/null || true
    fi
done

# Attendre 5 secondes
sleep 5

# Vérifier si des processus sont encore actifs
REMAINING=$(lsof -ti:$PORT 2>/dev/null || true)

if [ ! -z "$REMAINING" ]; then
    echo -e "${RED}Processus encore actifs, arrêt forcé...${NC}"
    for PID in $REMAINING; do
        echo "Arrêt forcé du processus $PID..."
        kill -KILL $PID 2>/dev/null || true
    done
    
    # Utiliser fuser en dernier recours
    fuser -k $PORT/tcp 2>/dev/null || true
fi

# Vérification finale
sleep 2
FINAL_CHECK=$(lsof -ti:$PORT 2>/dev/null || true)

if [ -z "$FINAL_CHECK" ]; then
    echo -e "${GREEN}✅ SAMA SYNDICAT arrêté avec succès${NC}"
    echo -e "${GREEN}Port $PORT libéré${NC}"
else
    echo -e "${RED}❌ Certains processus sont encore actifs${NC}"
    echo -e "${YELLOW}Processus restants: $FINAL_CHECK${NC}"
    exit 1
fi