#!/bin/bash

# Démarre le serveur si le module est déjà installé, sinon l'installe

echo "🏛️  SAMA SYNDICAT - DÉMARRAGE INTELLIGENT"
echo "=========================================="

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
DB_NAME="sama_syndicat_smart"
DB_USER="odoo"
DB_PASSWORD="odoo"
PORT=8070

# Activer l'environnement virtuel
source $VENV_PATH/bin/activate

# Arrêter les processus sur le port
pkill -f "xmlrpc-port=$PORT" 2>/dev/null || true
sleep 2

# Vérifier si la base existe
echo "🔍 Vérification de la base de données..."
if psql -U $DB_USER -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    echo "✅ Base de données trouvée: $DB_NAME"
    
    # Vérifier si le module est installé
    MODULE_STATE=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT state FROM ir_module_module WHERE name='sama_syndicat';" 2>/dev/null)
    
    if [ "$MODULE_STATE" = "installed" ]; then
        echo "✅ Module sama_syndicat déjà installé"
        echo "🚀 Démarrage direct du serveur..."
        
        cd $ODOO_PATH
        python3 odoo-bin \
            --addons-path=$ADDONS_PATH \
            --database=$DB_NAME \
            --db_user=$DB_USER \
            --db_password=$DB_PASSWORD \
            --xmlrpc-port=$PORT \
            --log-level=info
            
    else
        echo "⚠️  Module non installé (état: $MODULE_STATE)"
        echo "📦 Installation du module..."
        
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
        
        if [ $? -eq 0 ]; then
            echo "✅ Installation réussie, démarrage du serveur..."
            python3 odoo-bin \
                --addons-path=$ADDONS_PATH \
                --database=$DB_NAME \
                --db_user=$DB_USER \
                --db_password=$DB_PASSWORD \
                --xmlrpc-port=$PORT \
                --log-level=info
        else
            echo "❌ Échec de l'installation"
            exit 1
        fi
    fi
    
else
    echo "📦 Base de données non trouvée, création et installation..."
    
    # Créer la base
    createdb -U $DB_USER -O $DB_USER $DB_NAME
    
    if [ $? -eq 0 ]; then
        echo "✅ Base créée: $DB_NAME"
        
        # Installer le module
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
        
        if [ $? -eq 0 ]; then
            echo "✅ Installation réussie, démarrage du serveur..."
            python3 odoo-bin \
                --addons-path=$ADDONS_PATH \
                --database=$DB_NAME \
                --db_user=$DB_USER \
                --db_password=$DB_PASSWORD \
                --xmlrpc-port=$PORT \
                --log-level=info
        else
            echo "❌ Échec de l'installation"
            exit 1
        fi
    else
        echo "❌ Échec de création de la base"
        exit 1
    fi
fi