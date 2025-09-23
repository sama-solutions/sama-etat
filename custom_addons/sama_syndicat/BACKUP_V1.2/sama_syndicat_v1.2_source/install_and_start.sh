#!/bin/bash

# Installation autonome immédiate SAMA SYNDICAT

echo "🏛️  SAMA SYNDICAT - INSTALLATION AUTONOME"
echo "========================================="

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
DB_NAME="sama_syndicat_auto_$(date +%s)"
DB_USER="odoo"
DB_PASSWORD="odoo"
PORT=8070

echo "🔧 Base: $DB_NAME"
echo "🔧 Port: $PORT"

# Activer l'environnement virtuel
source $VENV_PATH/bin/activate

# Arrêter les processus sur le port
pkill -f "xmlrpc-port=$PORT" 2>/dev/null || true
sleep 1

# Créer la base
echo "🗄️  Création de la base..."
export PGPASSWORD=$DB_PASSWORD
createdb -U $DB_USER -O $DB_USER $DB_NAME

if [ $? -ne 0 ]; then
    echo "❌ Échec de création de la base"
    exit 1
fi

echo "✅ Base créée"

# Installation du module
echo "📦 Installation du module sama_syndicat..."
cd $ODOO_PATH

timeout 180 python3 odoo-bin \
    --addons-path=$ADDONS_PATH \
    --database=$DB_NAME \
    --db_user=$DB_USER \
    --db_password=$DB_PASSWORD \
    --init=sama_syndicat \
    --stop-after-init \
    --log-level=error \
    --without-demo=all

INSTALL_RESULT=$?

if [ $INSTALL_RESULT -eq 0 ]; then
    echo "✅ Installation réussie!"
    
    # Vérifier l'installation
    MODULE_STATE=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT state FROM ir_module_module WHERE name='sama_syndicat';" 2>/dev/null)
    
    if [ "$MODULE_STATE" = "installed" ]; then
        echo "✅ Module sama_syndicat INSTALLÉ ET ACTIVÉ"
        
        echo ""
        echo "🎉 INSTALLATION RÉUSSIE!"
        echo "========================"
        echo "🌐 URL: http://localhost:$PORT"
        echo "🔑 Base: $DB_NAME"
        echo "👤 admin/admin"
        
        echo ""
        echo "🚀 Démarrage du serveur..."
        python3 odoo-bin \
            --addons-path=$ADDONS_PATH \
            --database=$DB_NAME \
            --db_user=$DB_USER \
            --db_password=$DB_PASSWORD \
            --xmlrpc-port=$PORT \
            --log-level=info
    else
        echo "⚠️  État du module: $MODULE_STATE"
    fi
else
    echo "❌ Installation échouée (code: $INSTALL_RESULT)"
fi

unset PGPASSWORD