#!/bin/bash

# Script pour arrêter les tests Odoo
echo "=== Arrêt des processus de test Odoo ==="

# Arrêter tous les processus Odoo sur le port 8070
echo "Arrêt des processus sur le port 8070..."
pkill -f "odoo.*--http-port=8070" || true

# Attendre un peu
sleep 2

# Vérifier qu'il n'y a plus de processus
if pgrep -f "odoo.*--http-port=8070" > /dev/null; then
    echo "Processus encore actifs, arrêt forcé..."
    pkill -9 -f "odoo.*--http-port=8070" || true
else
    echo "Tous les processus de test arrêtés"
fi

echo "Logs disponibles dans:"
echo "  - /tmp/odoo_sama_carte_test.log"
echo "  - /tmp/odoo_install_sama_carte.log"
echo "  - /tmp/sama_carte_test_cycle.log"