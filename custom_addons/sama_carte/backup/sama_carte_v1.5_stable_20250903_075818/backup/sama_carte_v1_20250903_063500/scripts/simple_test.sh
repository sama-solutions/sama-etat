#!/bin/bash

# Script de test simple pour sama_carte
set -e

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
DB_NAME="sama_carte_test"
DB_USER="odoo"
DB_PASSWORD="odoo"
PORT="8070"

echo "=== Test simple sama_carte ==="

# Arrêter les processus existants
echo "Arrêt des processus existants..."
pkill -f "odoo.*--http-port=$PORT" || true
sleep 2

# Activation de l'environnement virtuel
source $VENV_PATH/bin/activate

# Configuration PostgreSQL
export PGPASSWORD=$DB_PASSWORD

# Démarrage d'Odoo en arrière-plan
cd $ODOO_PATH

echo "Démarrage d'Odoo en arrière-plan..."
python3 odoo-bin \
    --addons-path=/var/odoo/odoo18/addons,$ADDONS_PATH \
    --database=$DB_NAME \
    --db_user=$DB_USER \
    --db_password=$DB_PASSWORD \
    --http-port=$PORT \
    --log-level=info \
    --logfile=/tmp/odoo_simple_test.log \
    --no-database-list \
    --workers=0 \
    > /tmp/odoo_simple_stdout.log 2>&1 &

ODOO_PID=$!
echo "Odoo démarré avec PID: $ODOO_PID"

# Attendre le démarrage
echo "Attente du démarrage (15 secondes)..."
sleep 15

# Test de connectivité
echo "Test de connectivité..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT | grep -q "200\|302"; then
    echo "✓ Serveur accessible sur http://localhost:$PORT"
    echo "✓ Module sama_carte prêt pour les tests"
    echo "✓ PID Odoo: $ODOO_PID"
    echo "✓ Logs: /tmp/odoo_simple_test.log"
    echo ""
    echo "Pour arrêter: kill $ODOO_PID"
    echo "Pour voir les logs: tail -f /tmp/odoo_simple_test.log"
else
    echo "✗ Serveur non accessible"
    echo "Logs d'erreur:"
    tail -20 /tmp/odoo_simple_test.log
    kill $ODOO_PID || true
    exit 1
fi