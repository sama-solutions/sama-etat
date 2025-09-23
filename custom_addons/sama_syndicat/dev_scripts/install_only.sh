#!/bin/bash

# Installation seulement (sans démarrage) pour voir les erreurs

echo "🏛️  SAMA SYNDICAT - INSTALLATION SEULEMENT"
echo "==========================================="

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
DB_NAME="sama_syndicat_install"
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

# Installation du module avec logs détaillés
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
    --without-demo=all \
    2>&1 | tee /tmp/sama_syndicat_install.log

INSTALL_RESULT=$?

echo ""
echo "📋 RÉSULTAT DE L'INSTALLATION"
echo "============================="

if [ $INSTALL_RESULT -eq 0 ]; then
    echo "✅ Installation terminée avec succès"
else
    echo "❌ Installation terminée avec des erreurs (code: $INSTALL_RESULT)"
fi

echo ""
echo "📄 Log complet sauvé dans: /tmp/sama_syndicat_install.log"
echo ""
echo "🔍 ANALYSE DES ERREURS:"
echo "======================"

# Extraire les erreurs du log
grep -i "error\|critical\|failed\|exception" /tmp/sama_syndicat_install.log | head -10

echo ""
echo "🔍 ANALYSE DES AVERTISSEMENTS:"
echo "=============================="

# Extraire les avertissements
grep -i "warning" /tmp/sama_syndicat_install.log | head -5

echo ""
echo "📊 STATISTIQUES DU LOG:"
echo "======================"
echo "Lignes totales: $(wc -l < /tmp/sama_syndicat_install.log)"
echo "Erreurs: $(grep -ci "error\|critical\|failed" /tmp/sama_syndicat_install.log)"
echo "Avertissements: $(grep -ci "warning" /tmp/sama_syndicat_install.log)"