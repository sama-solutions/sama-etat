#!/bin/bash

# Script de démarrage Odoo avec base de démonstration
set -e

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
DB_NAME="sama_carte_demo"
DB_USER="odoo"
DB_PASSWORD="odoo"
PORT="8071"

echo "=== Démarrage Odoo avec données de démonstration ==="
echo "Port: $PORT"
echo "Base de données: $DB_NAME"

# Arrêter les processus existants
echo "Arrêt des processus existants..."
pkill -f "odoo.*--http-port=$PORT" || true
sleep 2

# Activation de l'environnement virtuel
source $VENV_PATH/bin/activate

# Configuration PostgreSQL
export PGPASSWORD=$DB_PASSWORD

# Vérification de la base de données
echo "Vérification de la base de données..."
if psql -U $DB_USER -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    echo "Base de données $DB_NAME existe déjà"
else
    echo "ERREUR: Base de données $DB_NAME n'existe pas. Utilisez d'abord install_with_demo.sh"
    exit 1
fi

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
    --logfile=/tmp/odoo_demo.log \
    --no-database-list \
    --workers=0 \
    > /tmp/odoo_demo_stdout.log 2>&1 &

ODOO_PID=$!
echo "Odoo démarré avec PID: $ODOO_PID"

# Attendre le démarrage
echo "Attente du démarrage (15 secondes)..."
sleep 15

# Test de connectivité
echo "Test de connectivité..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT | grep -q "200\|302"; then
    echo "✅ Serveur accessible sur http://localhost:$PORT"
    echo "✅ Base de démonstration prête"
    echo "✅ PID Odoo: $ODOO_PID"
    echo "✅ Logs: /tmp/odoo_demo.log"
    echo ""
    echo "🎯 Interface: http://localhost:$PORT"
    echo "🎯 Login: admin / admin"
    echo "🎯 Menu: Gestion des Membres > Membres"
    echo ""
    echo "Pour arrêter: kill $ODOO_PID"
else
    echo "❌ Serveur non accessible"
    echo "Logs d'erreur:"
    tail -20 /tmp/odoo_demo.log
    kill $ODOO_PID || true
    exit 1
fi