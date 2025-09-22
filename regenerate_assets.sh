#!/bin/bash

# Stop Odoo if it's running
echo "Stopping Odoo..."
pkill -f "/var/odoo/odoo18/odoo-bin"

# Remove existing assets
echo "Removing existing assets..."
rm -rf /home/grand-as/.local/share/Odoo/assets/*
rm -rf /home/grand-as/.local/share/Odoo/filestore/sama/*

# Restart Odoo with asset regeneration
echo "Starting Odoo with asset regeneration..."
nohup /var/odoo/odoo18-venv/bin/python3 /var/odoo/odoo18/odoo-bin -c /home/grand-as/psagsn/custom_addons/sama_etat/odoo.conf --http-port=8070 --dev=all --i18n-export=all.pot --i18n-export-overwrite --without-demo=all --stop-after-init -u base > /dev/null 2>&1 

echo "Restarting Odoo normally..."
nohup /var/odoo/odoo18-venv/bin/python3 /var/odoo/odoo18/odoo-bin -c /home/grand-as/psagsn/custom_addons/sama_etat/odoo.conf --http-port=8070 > /home/grand-as/psagsn/custom_addons/sama_etat/odoo.log 2>&1 &

echo "Assets regeneration complete. Please refresh your browser with Ctrl+F5"
