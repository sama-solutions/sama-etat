#!/bin/bash

# Vérification du statut d'installation

echo "🔍 SAMA SYNDICAT - VÉRIFICATION DU STATUT"
echo "========================================"

# Configuration
DB_USER="odoo"
DB_PASSWORD="odoo"
PORT=8070

export PGPASSWORD=$DB_PASSWORD

echo "🔍 Recherche des bases sama_syndicat..."
BASES=$(psql -U $DB_USER -d postgres -tAc "SELECT datname FROM pg_database WHERE datname LIKE 'sama_syndicat%' ORDER BY datname;" 2>/dev/null)

if [ -z "$BASES" ]; then
    echo "❌ Aucune base sama_syndicat trouvée"
else
    echo "📊 Bases trouvées:"
    echo "$BASES" | while read db; do
        if [ ! -z "$db" ]; then
            echo "   • $db"
            
            # Vérifier si le module est installé
            MODULE_STATE=$(psql -U $DB_USER -d "$db" -tAc "SELECT state FROM ir_module_module WHERE name='sama_syndicat';" 2>/dev/null)
            
            if [ "$MODULE_STATE" = "installed" ]; then
                echo "     ✅ Module installé et activé"
                
                # Compter les éléments
                MODELS=$(psql -U $DB_USER -d "$db" -tAc "SELECT COUNT(*) FROM ir_model WHERE model LIKE 'syndicat.%';" 2>/dev/null)
                echo "     📊 $MODELS modèles syndicaux"
                
                echo ""
                echo "🎉 BASE FONCTIONNELLE TROUVÉE: $db"
                echo "🌐 Pour démarrer:"
                echo "   cd /var/odoo/odoo18"
                echo "   python3 odoo-bin --addons-path=/home/grand-as/psagsn/custom_addons --database=$db --xmlrpc-port=$PORT"
                echo ""
                
            elif [ "$MODULE_STATE" = "to install" ]; then
                echo "     ⏳ Module en cours d'installation"
            elif [ "$MODULE_STATE" = "to upgrade" ]; then
                echo "     🔄 Module en cours de mise à jour"
            elif [ -z "$MODULE_STATE" ]; then
                echo "     ❌ Module non trouvé (base non initialisée)"
            else
                echo "     ⚠️  État: $MODULE_STATE"
            fi
        fi
    done
fi

echo ""
echo "🔍 Processus Odoo en cours..."
ODOO_PROCESSES=$(ps aux | grep odoo-bin | grep -v grep)
if [ -z "$ODOO_PROCESSES" ]; then
    echo "❌ Aucun processus Odoo en cours"
else
    echo "✅ Processus Odoo détectés:"
    echo "$ODOO_PROCESSES" | while read line; do
        echo "   $line"
    done
fi

echo ""
echo "🔍 Ports en écoute..."
PORTS=$(netstat -tlnp 2>/dev/null | grep ":80" | head -3)
if [ -z "$PORTS" ]; then
    echo "❌ Aucun port 80xx en écoute"
else
    echo "📊 Ports actifs:"
    echo "$PORTS"
fi

unset PGPASSWORD