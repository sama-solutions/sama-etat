#!/bin/bash

# Installation immédiate en arrière-plan

echo "🏛️  SAMA SYNDICAT - INSTALLATION IMMÉDIATE"
echo "=========================================="

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
DB_NAME="sama_syndicat_now_$(date +%s)"
DB_USER="odoo"
DB_PASSWORD="odoo"
PORT=8070

echo "🔧 Base: $DB_NAME"

# Activer l'environnement virtuel
source $VENV_PATH/bin/activate

# Arrêter les processus sur le port
pkill -f "xmlrpc-port=$PORT" 2>/dev/null || true

# Créer la base
echo "🗄️  Création de la base..."
export PGPASSWORD=$DB_PASSWORD
createdb -U $DB_USER -O $DB_USER $DB_NAME

if [ $? -ne 0 ]; then
    echo "❌ Échec de création de la base"
    exit 1
fi

echo "✅ Base créée"

# Installation en arrière-plan
echo "📦 Installation en arrière-plan..."
cd $ODOO_PATH

nohup python3 odoo-bin \
    --addons-path=$ADDONS_PATH \
    --database=$DB_NAME \
    --db_user=$DB_USER \
    --db_password=$DB_PASSWORD \
    --init=sama_syndicat \
    --stop-after-init \
    --log-level=error \
    --without-demo=all \
    > /tmp/sama_install_now.log 2>&1 &

INSTALL_PID=$!
echo "🔄 Installation PID: $INSTALL_PID"

# Attendre 30 secondes puis vérifier
echo "⏳ Attente 30 secondes..."
sleep 30

# Vérifier si le processus est terminé
if ! kill -0 $INSTALL_PID 2>/dev/null; then
    echo "✅ Installation terminée"
    
    # Vérifier le résultat
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
        echo "🚀 Commande de démarrage:"
        echo "cd $ODOO_PATH && python3 odoo-bin --addons-path=$ADDONS_PATH --database=$DB_NAME --xmlrpc-port=$PORT"
        
    else
        echo "⚠️  État du module: $MODULE_STATE"
        echo "📄 Log: /tmp/sama_install_now.log"
    fi
else
    echo "⏳ Installation encore en cours..."
    echo "📄 Log: /tmp/sama_install_now.log"
    echo "🔄 PID: $INSTALL_PID"
fi

unset PGPASSWORD