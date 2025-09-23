#!/bin/bash

# Installation minimale et directe

echo "🏛️  SAMA SYNDICAT - INSTALLATION MINIMALE"
echo "========================================"

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
DB_NAME="sama_syndicat_minimal"
DB_USER="odoo"
DB_PASSWORD="odoo"
PORT=8070

echo "🔧 Base: $DB_NAME"

# Activer l'environnement virtuel
source $VENV_PATH/bin/activate

# Arrêter les processus
pkill -f odoo-bin 2>/dev/null || true
sleep 1

# Créer la base
echo "🗄️  Création de la base..."
export PGPASSWORD=$DB_PASSWORD
dropdb -U $DB_USER --if-exists $DB_NAME 2>/dev/null || true
createdb -U $DB_USER -O $DB_USER $DB_NAME

echo "✅ Base créée"

# Installation directe sans timeout
echo "📦 Installation directe..."
cd $ODOO_PATH

python3 odoo-bin \
    --addons-path=$ADDONS_PATH \
    --database=$DB_NAME \
    --db_user=$DB_USER \
    --db_password=$DB_PASSWORD \
    --init=sama_syndicat \
    --stop-after-init \
    --log-level=error \
    --without-demo=all

RESULT=$?

echo ""
if [ $RESULT -eq 0 ]; then
    echo "✅ INSTALLATION RÉUSSIE!"
    
    # Vérifier
    MODULE_STATE=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT state FROM ir_module_module WHERE name='sama_syndicat';" 2>/dev/null)
    
    if [ "$MODULE_STATE" = "installed" ]; then
        echo "✅ Module INSTALLÉ ET ACTIVÉ"
        
        echo ""
        echo "🎉 SAMA SYNDICAT OPÉRATIONNEL!"
        echo "=============================="
        echo "🌐 URL: http://localhost:$PORT"
        echo "🔑 Base: $DB_NAME"
        echo "👤 admin/admin"
        
        echo ""
        echo "🚀 DÉMARRAGE:"
        echo "cd $ODOO_PATH && python3 odoo-bin --addons-path=$ADDONS_PATH --database=$DB_NAME --xmlrpc-port=$PORT"
        
    else
        echo "⚠️  État: $MODULE_STATE"
    fi
else
    echo "❌ Échec (code: $RESULT)"
fi

unset PGPASSWORD