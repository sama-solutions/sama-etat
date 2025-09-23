#!/bin/bash

# Installation rapide avec timeout court

echo "🏛️  SAMA SYNDICAT - INSTALLATION RAPIDE"
echo "======================================"

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
DB_NAME="sama_syndicat_quick_$(date +%s)"
DB_USER="odoo"
DB_PASSWORD="odoo"
PORT=8070

echo "🔧 Base: $DB_NAME"

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

# Installation avec timeout de 2 minutes
echo "📦 Installation du module (timeout 120s)..."
cd $ODOO_PATH

timeout 120 python3 odoo-bin \
    --addons-path=$ADDONS_PATH \
    --database=$DB_NAME \
    --db_user=$DB_USER \
    --db_password=$DB_PASSWORD \
    --init=sama_syndicat \
    --stop-after-init \
    --log-level=error \
    --without-demo=all \
    > /tmp/sama_quick_install.log 2>&1

INSTALL_RESULT=$?

echo ""
echo "📋 RÉSULTAT"
echo "==========="

if [ $INSTALL_RESULT -eq 0 ]; then
    echo "✅ Installation réussie!"
    
    # Vérifier rapidement
    MODULE_STATE=$(PGPASSWORD=$DB_PASSWORD psql -U $DB_USER -d $DB_NAME -tAc "SELECT state FROM ir_module_module WHERE name='sama_syndicat';" 2>/dev/null)
    
    if [ "$MODULE_STATE" = "installed" ]; then
        echo "✅ Module sama_syndicat INSTALLÉ ET ACTIVÉ"
        
        # Compter rapidement
        MODELS_COUNT=$(PGPASSWORD=$DB_PASSWORD psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM ir_model WHERE model LIKE 'syndicat.%';" 2>/dev/null)
        
        echo "📊 $MODELS_COUNT modèles syndicaux créés"
        echo ""
        echo "🎉 INSTALLATION RÉUSSIE!"
        echo "========================"
        echo "🌐 URL: http://localhost:$PORT"
        echo "🔑 Base: $DB_NAME"
        echo "👤 admin/admin"
        
        echo ""
        echo "🚀 COMMANDE DE DÉMARRAGE:"
        echo "cd $ODOO_PATH && python3 odoo-bin --addons-path=$ADDONS_PATH --database=$DB_NAME --xmlrpc-port=$PORT"
        
    else
        echo "⚠️  État du module: $MODULE_STATE"
    fi
    
elif [ $INSTALL_RESULT -eq 124 ]; then
    echo "⏰ Installation interrompue par timeout"
    echo "📄 Vérifiez le log: /tmp/sama_quick_install.log"
else
    echo "❌ Installation échouée (code: $INSTALL_RESULT)"
    echo "📄 Dernières lignes du log:"
    tail -5 /tmp/sama_quick_install.log
fi

unset PGPASSWORD