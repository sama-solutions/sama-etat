#!/bin/bash

# Installation directe SAMA SYNDICAT

echo "🏛️  SAMA SYNDICAT - INSTALLATION DIRECTE"
echo "========================================"

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
DB_NAME="sama_syndicat_direct"
DB_USER="odoo"
DB_PASSWORD="odoo"
PORT=8070

echo "🔧 Base: $DB_NAME"

# Activer l'environnement virtuel
source $VENV_PATH/bin/activate

# Arrêter les processus sur le port
pkill -f "xmlrpc-port=$PORT" 2>/dev/null || true

# Supprimer et recréer la base
echo "🗄️  Préparation de la base..."
export PGPASSWORD=$DB_PASSWORD
dropdb -U $DB_USER --if-exists $DB_NAME 2>/dev/null || true
createdb -U $DB_USER -O $DB_USER $DB_NAME

echo "✅ Base prête"

# Installation directe
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

if [ $RESULT -eq 0 ]; then
    echo ""
    echo "✅ INSTALLATION TERMINÉE"
    
    # Vérifier
    MODULE_STATE=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT state FROM ir_module_module WHERE name='sama_syndicat';" 2>/dev/null)
    
    if [ "$MODULE_STATE" = "installed" ]; then
        echo "✅ Module INSTALLÉ ET ACTIVÉ"
        
        # Compter les éléments créés
        MODELS=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM ir_model WHERE model LIKE 'syndicat.%';" 2>/dev/null)
        VIEWS=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM ir_ui_view WHERE model LIKE 'syndicat.%';" 2>/dev/null)
        MENUS=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM ir_ui_menu WHERE name LIKE '%Syndicat%';" 2>/dev/null)
        
        echo ""
        echo "📊 ÉLÉMENTS CRÉÉS:"
        echo "   • Modèles: $MODELS"
        echo "   • Vues: $VIEWS"
        echo "   • Menus: $MENUS"
        
        echo ""
        echo "🎉 SAMA SYNDICAT INSTALLÉ AVEC SUCCÈS!"
        echo "======================================"
        echo "🌐 URL: http://localhost:$PORT"
        echo "🔑 Base: $DB_NAME"
        echo "👤 admin/admin"
        
        echo ""
        echo "🚀 DÉMARRAGE:"
        echo "cd $ODOO_PATH"
        echo "python3 odoo-bin --addons-path=$ADDONS_PATH --database=$DB_NAME --xmlrpc-port=$PORT"
        
    else
        echo "⚠️  État: $MODULE_STATE"
    fi
else
    echo "❌ Échec installation (code: $RESULT)"
fi

unset PGPASSWORD