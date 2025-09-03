#!/bin/bash

# Script d'installation du module sama_carte
set -e

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
DB_NAME="sama_carte_test"
DB_USER="odoo"
DB_PASSWORD="odoo"

echo "=== Installation du module sama_carte ==="

# Activation de l'environnement virtuel
source $VENV_PATH/bin/activate

# Installation du module
cd $ODOO_PATH

echo "Installation/Mise à jour du module sama_carte..."
python3 odoo-bin \
    --addons-path=/var/odoo/odoo18/addons,$ADDONS_PATH \
    --database=$DB_NAME \
    --db_user=$DB_USER \
    --db_password=$DB_PASSWORD \
    -i sama_carte \
    --stop-after-init \
    --log-level=info \
    --logfile=/tmp/odoo_install_sama_carte.log

echo "Module sama_carte installé avec succès!"
echo "Logs disponibles dans: /tmp/odoo_install_sama_carte.log"