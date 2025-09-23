#!/bin/bash

# Script de démarrage rapide pour SAMA SYNDICAT
# Version simplifiée

echo "🚀 Démarrage rapide de SAMA SYNDICAT..."

# Arrêter les processus sur le port 8070
echo "📋 Arrêt des processus sur le port 8070..."
sudo pkill -f "xmlrpc-port=8070" 2>/dev/null || true
sudo fuser -k 8070/tcp 2>/dev/null || true

# Attendre un peu
sleep 2

# Démarrer Odoo
echo "🔄 Démarrage d'Odoo..."
cd /var/odoo/odoo18

python3 odoo-bin \
  --addons-path=/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat \
  --database=sama_syndicat_final_1756812346 \
  --xmlrpc-port=8070 \
  --update=sama_syndicat \
  --log-level=info

echo "✅ Serveur arrêté."