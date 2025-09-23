#!/bin/bash

# Installation forcée avec nouvelle base

echo "🏛️  SAMA SYNDICAT - INSTALLATION FORCÉE"
echo "======================================="

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
DB_NAME="sama_syndicat_force_$(date +%s)"
DB_USER="odoo"
DB_PASSWORD="odoo"
PORT=8070

echo "🔧 Configuration:"
echo "   Base: $DB_NAME"
echo "   Port: $PORT"
echo "   Addons: $ADDONS_PATH"

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

# Installation avec logs détaillés
echo "📦 Installation du module sama_syndicat..."
cd $ODOO_PATH

python3 odoo-bin \
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
echo "📋 RÉSULTAT"
echo "==========="

if [ $INSTALL_RESULT -eq 0 ]; then
    echo "✅ Installation réussie!"
    
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
        echo "🌐 Pour démarrer le serveur:"
        echo "   cd $ODOO_PATH"
        echo "   python3 odoo-bin --addons-path=$ADDONS_PATH --database=$DB_NAME --xmlrpc-port=$PORT"
        echo ""
        echo "🔗 URL d'accès: http://localhost:$PORT"
        echo "🔑 Base: $DB_NAME"
        echo "👤 Utilisateur: admin"
        echo "🔐 Mot de passe: admin"
        
        # Proposer de démarrer
        echo ""
        read -p "🚀 Démarrer le serveur maintenant ? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "🚀 Démarrage du serveur..."
            python3 odoo-bin \
                --addons-path=$ADDONS_PATH \
                --database=$DB_NAME \
                --db_user=$DB_USER \
                --db_password=$DB_PASSWORD \
                --xmlrpc-port=$PORT \
                --log-level=info
        fi
        
    else
        echo "⚠️  Module installé mais état: $MODULE_STATE"
    fi
    
else
    echo "❌ Installation échouée (code: $INSTALL_RESULT)"
fi

unset PGPASSWORD