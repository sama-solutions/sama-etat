#!/bin/bash

# Installation forcée avec base propre

echo "🏛️  SAMA SYNDICAT - INSTALLATION FORCÉE PROPRE"
echo "=============================================="

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
DB_NAME="sama_syndicat_clean_$(date +%s)"
DB_USER="odoo"
DB_PASSWORD="odoo"
PORT=8070

echo "🔧 Nouvelle base: $DB_NAME"

# Activer l'environnement virtuel
source $VENV_PATH/bin/activate

# Arrêter tous les processus Odoo
echo "🛑 Arrêt de tous les processus Odoo..."
pkill -f odoo-bin 2>/dev/null || true
pkill -f "xmlrpc-port" 2>/dev/null || true
sleep 2

# Créer une base complètement propre
echo "🗄️  Création d'une base propre..."
export PGPASSWORD=$DB_PASSWORD

# Supprimer si elle existe déjà
dropdb -U $DB_USER --if-exists $DB_NAME 2>/dev/null || true

# Créer la nouvelle base
createdb -U $DB_USER -O $DB_USER $DB_NAME

if [ $? -ne 0 ]; then
    echo "❌ Échec de création de la base"
    exit 1
fi

echo "✅ Base propre créée: $DB_NAME"

# Installation avec logs visibles
echo "📦 Installation du module sama_syndicat..."
echo "⏳ Cela peut prendre 2-3 minutes..."
cd $ODOO_PATH

# Installation avec timeout de 5 minutes
timeout 300 python3 odoo-bin \
    --addons-path=$ADDONS_PATH \
    --database=$DB_NAME \
    --db_user=$DB_USER \
    --db_password=$DB_PASSWORD \
    --init=sama_syndicat \
    --stop-after-init \
    --log-level=info \
    --without-demo=all

INSTALL_RESULT=$?

echo ""
echo "📋 RÉSULTAT DE L'INSTALLATION"
echo "============================="

if [ $INSTALL_RESULT -eq 0 ]; then
    echo "✅ Installation terminée avec succès!"
    
    # Vérification complète
    MODULE_STATE=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT state FROM ir_module_module WHERE name='sama_syndicat';" 2>/dev/null)
    
    if [ "$MODULE_STATE" = "installed" ]; then
        echo "✅ Module sama_syndicat INSTALLÉ ET ACTIVÉ"
        
        # Statistiques détaillées
        MODELS_COUNT=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM ir_model WHERE model LIKE 'syndicat.%';" 2>/dev/null)
        VIEWS_COUNT=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM ir_ui_view WHERE model LIKE 'syndicat.%';" 2>/dev/null)
        MENUS_COUNT=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM ir_ui_menu WHERE name LIKE '%Syndicat%';" 2>/dev/null)
        ACTIONS_COUNT=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM ir_act_window WHERE res_model LIKE 'syndicat.%';" 2>/dev/null)
        
        echo ""
        echo "📊 ÉLÉMENTS CRÉÉS AVEC SUCCÈS:"
        echo "   • Modèles de données: $MODELS_COUNT"
        echo "   • Vues XML: $VIEWS_COUNT"
        echo "   • Menus: $MENUS_COUNT"
        echo "   • Actions: $ACTIONS_COUNT"
        
        echo ""
        echo "🎉 SAMA SYNDICAT INSTALLÉ AVEC SUCCÈS!"
        echo "======================================"
        echo "🌐 URL d'accès: http://localhost:$PORT"
        echo "🔑 Base de données: $DB_NAME"
        echo "👤 Utilisateur: admin"
        echo "🔐 Mot de passe: admin"
        
        echo ""
        echo "🚀 COMMANDE DE DÉMARRAGE:"
        echo "cd $ODOO_PATH"
        echo "python3 odoo-bin --addons-path=$ADDONS_PATH --database=$DB_NAME --xmlrpc-port=$PORT"
        
        echo ""
        echo "🏛️ FONCTIONNALITÉS DISPONIBLES:"
        echo "   • Gestion des adhérents et cotisations"
        echo "   • Assemblées avec vote électronique"
        echo "   • Revendications et négociations"
        echo "   • Actions syndicales et manifestations"
        echo "   • Communications multi-canaux"
        echo "   • Formations et certifications"
        echo "   • Conventions collectives"
        echo "   • Médiations et conflits"
        echo "   • Tableau de bord analytique"
        
    else
        echo "⚠️  Module installé mais état: $MODULE_STATE"
    fi
    
elif [ $INSTALL_RESULT -eq 124 ]; then
    echo "⏰ Installation interrompue par timeout (5 minutes)"
    echo "💡 L'installation peut avoir réussi partiellement"
    
    # Vérifier quand même
    MODULE_STATE=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT state FROM ir_module_module WHERE name='sama_syndicat';" 2>/dev/null)
    if [ "$MODULE_STATE" = "installed" ]; then
        echo "✅ Module finalement installé malgré le timeout!"
    fi
    
else
    echo "❌ Installation échouée (code: $INSTALL_RESULT)"
fi

unset PGPASSWORD

echo ""
echo "📄 Pour vérifier le statut: ./sama_syndicat/check_status.sh"