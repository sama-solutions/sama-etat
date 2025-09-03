#!/bin/bash

# Script de cycle de test complet pour sama_carte
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="/tmp/sama_carte_test_cycle.log"

echo "=== Cycle de test sama_carte ===" | tee $LOG_FILE
echo "Début: $(date)" | tee -a $LOG_FILE

# Fonction pour afficher les logs en cas d'erreur
show_logs() {
    echo "=== ERREUR DÉTECTÉE ===" | tee -a $LOG_FILE
    echo "Logs Odoo:" | tee -a $LOG_FILE
    tail -50 /tmp/odoo_sama_carte_test.log 2>/dev/null || echo "Pas de logs Odoo disponibles"
    echo "Logs installation:" | tee -a $LOG_FILE
    tail -50 /tmp/odoo_install_sama_carte.log 2>/dev/null || echo "Pas de logs d'installation disponibles"
}

# Piège pour capturer les erreurs
trap show_logs ERR

# Étape 1: Initialisation de la base de données
echo "Étape 1: Initialisation de la base de données..." | tee -a $LOG_FILE
chmod +x $SCRIPT_DIR/init_database.sh
$SCRIPT_DIR/init_database.sh

# Étape 2: Installation du module
echo "Étape 2: Installation du module..." | tee -a $LOG_FILE
chmod +x $SCRIPT_DIR/install_module.sh
$SCRIPT_DIR/install_module.sh

# Étape 3: Démarrage d'Odoo en arrière-plan
echo "Étape 3: Démarrage d'Odoo..." | tee -a $LOG_FILE
chmod +x $SCRIPT_DIR/start_odoo_test.sh

# Démarrage en arrière-plan
$SCRIPT_DIR/start_odoo_test.sh &
ODOO_PID=$!

# Attendre que le serveur soit prêt
echo "Attente du démarrage du serveur..." | tee -a $LOG_FILE
sleep 15

# Vérifier si Odoo est démarré
if ! kill -0 $ODOO_PID 2>/dev/null; then
    echo "ERREUR: Odoo ne s'est pas démarré correctement" | tee -a $LOG_FILE
    show_logs
    exit 1
fi

# Étape 4: Tests de base
echo "Étape 4: Tests de connectivité..." | tee -a $LOG_FILE

# Test de connexion HTTP
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8070 | grep -q "200\|302"; then
    echo "✓ Serveur HTTP accessible" | tee -a $LOG_FILE
else
    echo "✗ Serveur HTTP non accessible" | tee -a $LOG_FILE
fi

# Test de la base de données
if psql -U odoo -d sama_carte_test -c "SELECT name FROM ir_module_module WHERE name='sama_carte' AND state='installed';" | grep -q sama_carte; then
    echo "✓ Module sama_carte installé en base" | tee -a $LOG_FILE
else
    echo "✗ Module sama_carte non trouvé en base" | tee -a $LOG_FILE
fi

echo "=== Tests terminés ===" | tee -a $LOG_FILE
echo "Fin: $(date)" | tee -a $LOG_FILE
echo "Odoo PID: $ODOO_PID" | tee -a $LOG_FILE
echo "Pour arrêter Odoo: kill $ODOO_PID" | tee -a $LOG_FILE
echo "Logs complets: $LOG_FILE" | tee -a $LOG_FILE
echo "Interface web: http://localhost:8070" | tee -a $LOG_FILE