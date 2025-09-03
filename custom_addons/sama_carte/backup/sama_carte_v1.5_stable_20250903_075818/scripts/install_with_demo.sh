#!/bin/bash

# Script d'installation du module sama_carte avec données de démonstration
set -e

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
DB_NAME="sama_carte_demo"
DB_USER="odoo"
DB_PASSWORD="odoo"

echo "=== Installation sama_carte avec données de démonstration ==="

# Activation de l'environnement virtuel
source $VENV_PATH/bin/activate

# Configuration PostgreSQL
export PGPASSWORD=$DB_PASSWORD

# Suppression de la base existante si elle existe
echo "Suppression de la base existante..."
dropdb -U $DB_USER $DB_NAME 2>/dev/null || true

# Création d'une nouvelle base
echo "Création de la base de données..."
createdb -U $DB_USER $DB_NAME

# Initialisation avec les modules de base
cd $ODOO_PATH

echo "Initialisation de la base avec les modules de base..."
python3 odoo-bin \
    --addons-path=/var/odoo/odoo18/addons \
    --database=$DB_NAME \
    --db_user=$DB_USER \
    --db_password=$DB_PASSWORD \
    -i base \
    --stop-after-init \
    --log-level=info \
    --logfile=/tmp/odoo_init_demo.log

echo "Installation du module sama_carte avec données de démonstration..."
python3 odoo-bin \
    --addons-path=/var/odoo/odoo18/addons,$ADDONS_PATH \
    --database=$DB_NAME \
    --db_user=$DB_USER \
    --db_password=$DB_PASSWORD \
    -i sama_carte \
    --stop-after-init \
    --log-level=info \
    --logfile=/tmp/odoo_install_demo.log

echo "✅ Module sama_carte installé avec données de démonstration!"
echo "Base de données: $DB_NAME"
echo "Logs: /tmp/odoo_install_demo.log"