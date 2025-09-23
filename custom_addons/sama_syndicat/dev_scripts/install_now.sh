#!/bin/bash

# Installation immédiate de sama_syndicat

echo "🏛️  SAMA SYNDICAT - INSTALLATION IMMÉDIATE"
echo "=========================================="

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
DB_NAME="sama_syndicat_now"
DB_USER="odoo"
DB_PASSWORD="odoo"
PORT=8070

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source $VENV_PATH/bin/activate

# Arrêter les processus sur le port
echo "🔍 Arrêt des processus sur le port $PORT..."
pkill -f "xmlrpc-port=$PORT" 2>/dev/null || true
sleep 2

# Validation syntaxique
echo "🔍 Validation syntaxique..."
python3 sama_syndicat/dev_scripts/validate_syntax.py
if [ $? -ne 0 ]; then
    echo "❌ Erreurs de syntaxe détectées"
    exit 1
fi

# Supprimer et recréer la base
echo "🗄️  Préparation de la base de données..."
dropdb -U $DB_USER --if-exists $DB_NAME 2>/dev/null || true
createdb -U $DB_USER -O $DB_USER $DB_NAME

if [ $? -ne 0 ]; then
    echo "❌ Échec de création de la base"
    exit 1
fi

# Installation du module
echo "📦 Installation du module sama_syndicat..."
cd $ODOO_PATH

timeout 300 python3 odoo-bin \
    --addons-path=$ADDONS_PATH \
    --database=$DB_NAME \
    --db_user=$DB_USER \
    --db_password=$DB_PASSWORD \
    --init=sama_syndicat \
    --stop-after-init \
    --log-level=info \
    --without-demo=all

if [ $? -eq 0 ]; then
    echo "✅ Module installé avec succès!"
    echo ""
    echo "🚀 Pour démarrer le serveur:"
    echo "cd $ODOO_PATH"
    echo "python3 odoo-bin --addons-path=$ADDONS_PATH --database=$DB_NAME --xmlrpc-port=$PORT --log-level=info"
    echo ""
    echo "🌐 URL d'accès: http://localhost:$PORT"
    echo "🔑 Base de données: $DB_NAME"
else
    echo "❌ Erreur lors de l'installation"
    exit 1
fi