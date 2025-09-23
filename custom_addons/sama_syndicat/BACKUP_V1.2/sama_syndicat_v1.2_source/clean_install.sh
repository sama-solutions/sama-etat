#!/bin/bash

# Nettoyage complet et installation propre

echo "🧹 SAMA SYNDICAT - NETTOYAGE ET INSTALLATION PROPRE"
echo "=================================================="

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
DB_USER="odoo"
DB_PASSWORD="odoo"
PORT=8070
DB_NAME="sama_syndicat_final_$(date +%s)"

# Activer l'environnement virtuel
source $VENV_PATH/bin/activate

# Arrêter tous les processus Odoo
echo "🛑 Arrêt de tous les processus Odoo..."
pkill -f odoo-bin 2>/dev/null || true
sleep 2

# Nettoyer les anciennes bases de test
echo "🗑️  Nettoyage des anciennes bases de test..."
export PGPASSWORD=$DB_PASSWORD
psql -U $DB_USER -d postgres -tAc "SELECT datname FROM pg_database WHERE datname LIKE 'sama_syndicat_%';" | while read -r dbname; do
    if [ -n "$dbname" ]; then
        echo "   - Suppression de $dbname"
        dropdb -U $DB_USER --if-exists "$dbname"
    fi
done

echo "✅ Nettoyage terminé"

# Créer une nouvelle base propre
echo "🗄️  Création d'une nouvelle base propre: $DB_NAME..."
createdb -U $DB_USER -O $DB_USER $DB_NAME

if [ $? -ne 0 ]; then
    echo "❌ Échec de création de la base"
    exit 1
fi

echo "✅ Base propre créée"

# Installation directe
echo "📦 Installation du module sama_syndicat..."
cd $ODOO_PATH

python3 odoo-bin \
    --addons-path=/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat \
    --database=$DB_NAME \
    --db_user=$DB_USER \
    --db_password=$DB_PASSWORD \
    --init=sama_syndicat \
    --stop-after-init \
    --log-level=info \
    --without-demo=all

RESULT=$?

if [ $RESULT -eq 0 ]; then
    echo ""
    echo "🎉 INSTALLATION RÉUSSIE!"
    
    # Vérifier
    MODULE_STATE=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT state FROM ir_module_module WHERE name='sama_syndicat';" 2>/dev/null)
    
    if [ "$MODULE_STATE" = "installed" ]; then
        echo "✅ Module SAMA SYNDICAT INSTALLÉ ET ACTIVÉ"
        
        echo ""
        echo "🚀 Pour démarrer le serveur:"
        echo "cd $ODOO_PATH && python3 odoo-bin --addons-path=/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat --database=$DB_NAME --xmlrpc-port=$PORT"
        
    else
        echo "⚠️  État: $MODULE_STATE"
    fi
else
    echo "❌ Échec (code: $RESULT)"
fi

unset PGPASSWORD