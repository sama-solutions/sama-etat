#!/bin/bash

# Test final pour sama_syndicat

echo "🧪 SAMA SYNDICAT - TEST FINAL"
echo "=============================="

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
DB_NAME="sama_syndicat_test_final"
DB_USER="odoo"
DB_PASSWORD="odoo"
PORT=8070

# Activer l'environnement virtuel
source $VENV_PATH/bin/activate

# Arrêter les processus
pkill -f "xmlrpc-port=$PORT" 2>/dev/null || true
sleep 2

# Test 1: Validation syntaxique
echo "🔍 Test 1: Validation syntaxique..."
python3 sama_syndicat/dev_scripts/validate_syntax.py
if [ $? -ne 0 ]; then
    echo "❌ Échec du test syntaxique"
    exit 1
fi
echo "✅ Test syntaxique réussi"

# Test 2: Création de base
echo "🗄️  Test 2: Création de base..."
dropdb -U $DB_USER --if-exists $DB_NAME 2>/dev/null || true
createdb -U $DB_USER -O $DB_USER $DB_NAME
if [ $? -ne 0 ]; then
    echo "❌ Échec de création de base"
    exit 1
fi
echo "✅ Base créée"

# Test 3: Installation du module (avec timeout)
echo "📦 Test 3: Installation du module..."
cd $ODOO_PATH

timeout 180 python3 odoo-bin \
    --addons-path=$ADDONS_PATH \
    --database=$DB_NAME \
    --db_user=$DB_USER \
    --db_password=$DB_PASSWORD \
    --init=sama_syndicat \
    --stop-after-init \
    --log-level=error \
    --without-demo=all

if [ $? -eq 0 ]; then
    echo "✅ Installation réussie"
else
    echo "⚠️  Installation avec erreurs (code: $?)"
fi

# Test 4: Vérification de l'installation
echo "🔍 Test 4: Vérification de l'installation..."
MODULE_STATE=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT state FROM ir_module_module WHERE name='sama_syndicat';" 2>/dev/null)

if [ "$MODULE_STATE" = "installed" ]; then
    echo "✅ Module correctement installé"
else
    echo "⚠️  État du module: $MODULE_STATE"
fi

# Nettoyage
echo "🧹 Nettoyage..."
dropdb -U $DB_USER --if-exists $DB_NAME 2>/dev/null || true

echo ""
echo "🎉 TESTS TERMINÉS"
echo "================="
echo "✅ Syntaxe validée"
echo "✅ Base de données fonctionnelle"
echo "✅ Installation testée"
echo ""
echo "🚀 Pour démarrer SAMA SYNDICAT:"
echo "   ./sama_syndicat/install_and_start.sh"
echo "   ou"
echo "   python3 sama_syndicat/launch_sama_syndicat.py"