#!/bin/bash

# Installation en arrière-plan avec vérification

echo "🏛️  SAMA SYNDICAT - INSTALLATION EN ARRIÈRE-PLAN"
echo "================================================"

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
DB_NAME="sama_syndicat_bg_$(date +%s)"
DB_USER="odoo"
DB_PASSWORD="odoo"
PORT=8070
LOG_FILE="/tmp/sama_install_bg.log"
PID_FILE="/tmp/sama_install.pid"

# Activer l'environnement virtuel
source $VENV_PATH/bin/activate

# Arrêter les processus sur le port
pkill -f "xmlrpc-port=$PORT" 2>/dev/null || true
sleep 2

# Supprimer et recréer la base
echo "🗄️  Préparation de la base de données..."
export PGPASSWORD=$DB_PASSWORD
dropdb -U $DB_USER --if-exists $DB_NAME 2>/dev/null || true
createdb -U $DB_USER -O $DB_USER $DB_NAME

if [ $? -ne 0 ]; then
    echo "❌ Échec de création de la base"
    exit 1
fi

echo "✅ Base créée: $DB_NAME"

# Lancer l'installation en arrière-plan
echo "📦 Lancement de l'installation en arrière-plan..."
echo "📄 Log: $LOG_FILE"

cd $ODOO_PATH

# Installation avec timeout de 10 minutes
nohup timeout 600 python3 odoo-bin \
    --addons-path=/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat \
    --database=$DB_NAME \
    --db_user=$DB_USER \
    --db_password=$DB_PASSWORD \
    --init=sama_syndicat \
    --stop-after-init \
    --log-level=info \
    --without-demo=all \
    > $LOG_FILE 2>&1 &

INSTALL_PID=$!
echo $INSTALL_PID > $PID_FILE

echo "🔄 PID du processus d'installation: $INSTALL_PID"

# Attendre et vérifier périodiquement
echo "⏳ Attente de l'installation (max 10 minutes)..."

for i in {1..60}; do
    sleep 10
    
    # Vérifier si le processus est toujours en cours
    if ! kill -0 $INSTALL_PID 2>/dev/null; then
        echo "✅ Processus d'installation terminé"
        break
    fi
    
    echo "⏳ Installation en cours... (${i}0s)"
    
    # Afficher les dernières lignes du log
    if [ -f $LOG_FILE ]; then
        echo "📄 Dernière ligne du log:"
        tail -1 $LOG_FILE
    fi
done

# Vérifier le résultat
wait $INSTALL_PID 2>/dev/null
INSTALL_RESULT=$?

echo ""
echo "📋 RÉSULTAT DE L'INSTALLATION"
echo "============================="

if [ $INSTALL_RESULT -eq 0 ]; then
    echo "✅ Installation terminée avec succès!"
    
    # Vérifier l'état du module
    MODULE_STATE=$(PGPASSWORD=$DB_PASSWORD psql -U $DB_USER -d $DB_NAME -tAc "SELECT state FROM ir_module_module WHERE name='sama_syndicat';" 2>/dev/null)
    
    if [ "$MODULE_STATE" = "installed" ]; then
        echo "✅ Module sama_syndicat installé et activé"
        
        # Statistiques
        MODELS_COUNT=$(PGPASSWORD=$DB_PASSWORD psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM ir_model WHERE model LIKE 'syndicat.%';" 2>/dev/null)
        VIEWS_COUNT=$(PGPASSWORD=$DB_PASSWORD psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM ir_ui_view WHERE model LIKE 'syndicat.%';" 2>/dev/null)
        MENUS_COUNT=$(PGPASSWORD=$DB_PASSWORD psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM ir_ui_menu WHERE name LIKE '%Syndicat%';" 2>/dev/null)
        
        echo "📊 Statistiques:"
        echo "   • Modèles: $MODELS_COUNT"
        echo "   • Vues: $VIEWS_COUNT"
        echo "   • Menus: $MENUS_COUNT"
        
        echo ""
        echo "🎉 INSTALLATION RÉUSSIE!"
        echo "========================"
        echo "🌐 Pour démarrer le serveur:"
        echo "   cd $ODOO_PATH"
        echo "   python3 odoo-bin --addons-path=/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat --database=$DB_NAME --xmlrpc-port=$PORT"
        echo ""
        echo "🔗 URL d'accès: http://localhost:$PORT"
        echo "🔑 Base: $DB_NAME"
        
    else
        echo "⚠️  Module installé mais état: $MODULE_STATE"
    fi
    
else
    echo "❌ Installation échouée (code: $INSTALL_RESULT)"
    
    echo ""
    echo "🔍 ANALYSE DES ERREURS:"
    echo "======================"
    
    if [ -f $LOG_FILE ]; then
        # Extraire les erreurs
        echo "❌ Erreurs trouvées:"
        grep -i "error\|critical\|failed\|exception" $LOG_FILE | tail -5
        
        echo ""
        echo "📄 Dernières lignes du log:"
        tail -10 $LOG_FILE
    fi
fi

# Nettoyage
rm -f $PID_FILE
unset PGPASSWORD

echo ""
echo "📄 Log complet disponible: $LOG_FILE"