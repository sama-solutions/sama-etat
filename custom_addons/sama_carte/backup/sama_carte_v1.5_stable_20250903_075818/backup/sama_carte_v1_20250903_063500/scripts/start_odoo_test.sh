#!/bin/bash

# Script de démarrage Odoo pour tests du module sama_carte
# Port dédié: 8070
# Base de données: sama_carte_test

set -e

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
DB_NAME="sama_carte_test"
DB_USER="odoo"
DB_PASSWORD="odoo"
PORT="8070"
LOG_LEVEL="info"

echo "=== Démarrage du test Odoo pour sama_carte ==="
echo "Port: $PORT"
echo "Base de données: $DB_NAME"
echo "Addons path: $ADDONS_PATH"

# Arrêter les processus existants sur le port
echo "Arrêt des processus existants sur le port $PORT..."
pkill -f "odoo.*--http-port=$PORT" || true
sleep 2

# Activation de l'environnement virtuel
echo "Activation de l'environnement virtuel..."
source $VENV_PATH/bin/activate

# Configuration PostgreSQL
export PGPASSWORD=$DB_PASSWORD

# Vérification de la base de données
echo "Vérification de la base de données..."
if psql -U $DB_USER -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    echo "Base de données $DB_NAME existe déjà"
else
    echo "ERREUR: Base de données $DB_NAME n'existe pas. Utilisez d'abord init_database.sh"
    exit 1
fi

# Démarrage d'Odoo
echo "Démarrage d'Odoo..."
cd $ODOO_PATH

python3 odoo-bin \
    --addons-path=/var/odoo/odoo18/addons,$ADDONS_PATH \
    --database=$DB_NAME \
    --db_user=$DB_USER \
    --db_password=$DB_PASSWORD \
    --http-port=$PORT \
    --log-level=$LOG_LEVEL \
    --dev=reload \
    --without-demo=all \
    --logfile=/tmp/odoo_sama_carte_test.log \
    "$@"