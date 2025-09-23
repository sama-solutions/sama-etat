#!/bin/bash

# Installation asynchrone avec suivi

echo "🏛️  SAMA SYNDICAT - INSTALLATION ASYNCHRONE"
echo "==========================================="

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
DB_NAME="sama_syndicat_async_$(date +%s)"
DB_USER="odoo"
DB_PASSWORD="odoo"
PORT=8070
LOG_FILE="/tmp/sama_install_async.log"
PID_FILE="/tmp/sama_install.pid"

echo "🔧 Configuration:"
echo "   Base: $DB_NAME"
echo "   Port: $PORT"
echo "   Log: $LOG_FILE"

# Activer l'environnement virtuel
source $VENV_PATH/bin/activate

# Arrêter les processus sur le port
pkill -f "xmlrpc-port=$PORT" 2>/dev/null || true
sleep 2

# Créer la base
echo "🗄️  Création de la base $DB_NAME..."
export PGPASSWORD=$DB_PASSWORD
createdb -U $DB_USER -O $DB_USER $DB_NAME

if [ $? -ne 0 ]; then
    echo "❌ Échec de création de la base"
    exit 1
fi

echo "✅ Base créée"

# Lancer l'installation en arrière-plan
echo "📦 Lancement de l'installation en arrière-plan..."
cd $ODOO_PATH

nohup python3 odoo-bin \
    --addons-path=$ADDONS_PATH \
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

echo "🔄 Installation lancée avec PID: $INSTALL_PID"
echo "📄 Log en temps réel: $LOG_FILE"
echo ""

# Fonction de suivi
follow_installation() {
    echo "⏳ Suivi de l'installation (Ctrl+C pour arrêter le suivi)..."
    echo "📄 Dernières lignes du log:"
    echo "=========================="
    
    while kill -0 $INSTALL_PID 2>/dev/null; do
        if [ -f $LOG_FILE ]; then
            tail -3 $LOG_FILE | sed 's/^/   /'
        fi
        sleep 5
        echo "   [$(date '+%H:%M:%S')] Installation en cours..."
    done
    
    echo ""
    echo "✅ Processus d'installation terminé"
}

# Démarrer le suivi
follow_installation &
FOLLOW_PID=$!

# Attendre la fin de l'installation
wait $INSTALL_PID
INSTALL_RESULT=$?

# Arrêter le suivi
kill $FOLLOW_PID 2>/dev/null || true

echo ""
echo "📋 RÉSULTAT DE L'INSTALLATION"
echo "============================="

if [ $INSTALL_RESULT -eq 0 ]; then
    echo "✅ Installation terminée avec succès!"
    
    # Vérifier l'installation
    MODULE_STATE=$(PGPASSWORD=$DB_PASSWORD psql -U $DB_USER -d $DB_NAME -tAc "SELECT state FROM ir_module_module WHERE name='sama_syndicat';" 2>/dev/null)
    
    if [ "$MODULE_STATE" = "installed" ]; then
        echo "✅ Module sama_syndicat installé et activé"
        
        # Statistiques
        MODELS_COUNT=$(PGPASSWORD=$DB_PASSWORD psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM ir_model WHERE model LIKE 'syndicat.%';" 2>/dev/null)
        VIEWS_COUNT=$(PGPASSWORD=$DB_PASSWORD psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM ir_ui_view WHERE model LIKE 'syndicat.%';" 2>/dev/null)
        MENUS_COUNT=$(PGPASSWORD=$DB_PASSWORD psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM ir_ui_menu WHERE name LIKE '%Syndicat%';" 2>/dev/null)
        
        echo ""
        echo "📊 STATISTIQUES D'INSTALLATION:"
        echo "   • Modèles créés: $MODELS_COUNT"
        echo "   • Vues créées: $VIEWS_COUNT"
        echo "   • Menus créés: $MENUS_COUNT"
        
        echo ""
        echo "🎉 INSTALLATION RÉUSSIE!"
        echo "========================"
        echo "🌐 URL d'accès: http://localhost:$PORT"
        echo "🔑 Base: $DB_NAME"
        echo "👤 Utilisateur: admin"
        echo "🔐 Mot de passe: admin"
        
        echo ""
        echo "🚀 Pour démarrer le serveur:"
        echo "cd $ODOO_PATH"
        echo "python3 odoo-bin --addons-path=$ADDONS_PATH --database=$DB_NAME --xmlrpc-port=$PORT"
        
    else
        echo "⚠️  Module installé mais état: $MODULE_STATE"
    fi
    
else
    echo "❌ Installation échouée (code: $INSTALL_RESULT)"
    echo ""
    echo "🔍 Dernières lignes du log:"
    tail -10 $LOG_FILE
fi

# Nettoyage
rm -f $PID_FILE
unset PGPASSWORD

echo ""
echo "📄 Log complet disponible: $LOG_FILE"