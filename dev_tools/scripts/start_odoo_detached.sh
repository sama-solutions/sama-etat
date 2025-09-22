#!/bin/bash

# Kill any running Odoo processes
echo "Stopping any running Odoo processes..."
pkill -f "/var/odoo/odoo18/odoo-bin"

# Start Odoo in detached mode
echo "Starting Odoo on port 8070..."
nohup /var/odoo/odoo18-venv/bin/python3 /var/odoo/odoo18/odoo-bin -c /home/grand-as/psagsn/custom_addons/sama_etat/odoo.conf --http-port=8070 > /home/grand-as/psagsn/custom_addons/sama_etat/odoo.log 2>&1 &

echo "Odoo started in detached mode. Check the log file for details:"
echo "/home/grand-as/psagsn/custom_addons/sama_etat/odoo.log"

echo "You can access Odoo at: http://localhost:8070"
