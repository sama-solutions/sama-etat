#!/bin/bash

# Script de mise à jour du module sama_carte
set -e

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
DB_NAME="sama_carte_test"
DB_USER="odoo"
DB_PASSWORD="odoo"

echo "=== Mise à jour du module sama_carte ==="

# Activation de l'environnement virtuel
source $VENV_PATH/bin/activate

# Configuration PostgreSQL
export PGPASSWORD=$DB_PASSWORD

# Mise à jour du module
cd $ODOO_PATH

echo "Mise à jour du module sama_carte..."
python3 odoo-bin \
    --addons-path=/var/odoo/odoo18/addons,$ADDONS_PATH \
    --database=$DB_NAME \
    --db_user=$DB_USER \
    --db_password=$DB_PASSWORD \
    -u sama_carte \
    --stop-after-init \
    --log-level=info \
    --logfile=/tmp/odoo_update_sama_carte.log

echo "Module sama_carte mis à jour avec succès!"
echo "Logs disponibles dans: /tmp/odoo_update_sama_carte.log"