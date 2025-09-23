#!/bin/bash

# Test d'installation simple et rapide

echo "🏛️  SAMA SYNDICAT - TEST INSTALLATION SIMPLE"
echo "============================================="

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
DB_NAME="sama_syndicat_test_simple"
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

# Supprimer et recréer la base
echo "🗄️  Préparation de la base de données..."
dropdb -U $DB_USER --if-exists $DB_NAME 2>/dev/null || true
createdb -U $DB_USER -O $DB_USER $DB_NAME

if [ $? -ne 0 ]; then
    echo "❌ Échec de création de la base"
    exit 1
fi

echo "✅ Base créée"

# Installation du module avec timeout court
echo "📦 Installation du module sama_syndicat (timeout 120s)..."
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
    > /tmp/sama_install_simple.log 2>&1

INSTALL_RESULT=$?

echo ""
echo "📋 RÉSULTAT DE L'INSTALLATION"
echo "============================="

if [ $INSTALL_RESULT -eq 0 ]; then
    echo "✅ Installation réussie!"
    
    # Vérifier que le module est installé
    MODULE_STATE=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT state FROM ir_module_module WHERE name='sama_syndicat';" 2>/dev/null)
    
    if [ "$MODULE_STATE" = "installed" ]; then
        echo "✅ Module correctement installé dans la base"
        
        # Compter les modèles créés
        MODELS_COUNT=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM ir_model WHERE model LIKE 'syndicat.%';" 2>/dev/null)
        echo "📊 Modèles créés: $MODELS_COUNT"
        
        # Compter les vues créées
        VIEWS_COUNT=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM ir_ui_view WHERE model LIKE 'syndicat.%';" 2>/dev/null)
        echo "📊 Vues créées: $VIEWS_COUNT"
        
        # Compter les menus créés
        MENUS_COUNT=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM ir_ui_menu WHERE name LIKE '%Syndicat%' OR name LIKE '%SAMA%';" 2>/dev/null)
        echo "📊 Menus créés: $MENUS_COUNT"
        
        echo ""
        echo "🎉 INSTALLATION RÉUSSIE!"
        echo "========================"
        echo "✅ Module sama_syndicat installé et activé"
        echo "✅ Base de données: $DB_NAME"
        echo "✅ $MODELS_COUNT modèles, $VIEWS_COUNT vues, $MENUS_COUNT menus"
        echo ""
        echo "🚀 Pour démarrer le serveur:"
        echo "cd $ODOO_PATH"
        echo "python3 odoo-bin --addons-path=$ADDONS_PATH --database=$DB_NAME --xmlrpc-port=$PORT"
        
    else
        echo "⚠️  Module installé mais état: $MODULE_STATE"
    fi
    
elif [ $INSTALL_RESULT -eq 124 ]; then
    echo "⏰ Installation interrompue par timeout (120s)"
    echo "⚠️  L'installation peut avoir réussi partiellement"
else
    echo "❌ Installation échouée (code: $INSTALL_RESULT)"
    echo ""
    echo "🔍 DERNIÈRES LIGNES DU LOG:"
    echo "=========================="
    tail -20 /tmp/sama_install_simple.log
fi

echo ""
echo "📄 Log complet: /tmp/sama_install_simple.log"

# Nettoyage optionnel
# dropdb -U $DB_USER --if-exists $DB_NAME 2>/dev/null || true