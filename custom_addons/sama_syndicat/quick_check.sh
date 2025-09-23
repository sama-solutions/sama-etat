#!/bin/bash

# Vérification rapide de l'installation

echo "🔍 SAMA SYNDICAT - VÉRIFICATION RAPIDE"
echo "====================================="

DB_USER="odoo"
DB_PASSWORD="odoo"
export PGPASSWORD=$DB_PASSWORD

# Chercher les bases sama_syndicat récentes
echo "📊 Bases sama_syndicat récentes:"
RECENT_BASES=$(psql -U $DB_USER -d postgres -tAc "SELECT datname FROM pg_database WHERE datname LIKE 'sama_syndicat%' ORDER BY datname DESC LIMIT 5;" 2>/dev/null)

if [ -z "$RECENT_BASES" ]; then
    echo "❌ Aucune base sama_syndicat trouvée"
else
    echo "$RECENT_BASES" | while read db; do
        if [ ! -z "$db" ]; then
            echo ""
            echo "🔍 Base: $db"
            
            # Vérifier si le module est installé
            MODULE_STATE=$(psql -U $DB_USER -d "$db" -tAc "SELECT state FROM ir_module_module WHERE name='sama_syndicat';" 2>/dev/null)
            
            if [ "$MODULE_STATE" = "installed" ]; then
                echo "   ✅ Module INSTALLÉ ET ACTIVÉ"
                
                # Compter les éléments
                MODELS=$(psql -U $DB_USER -d "$db" -tAc "SELECT COUNT(*) FROM ir_model WHERE model LIKE 'syndicat.%';" 2>/dev/null)
                VIEWS=$(psql -U $DB_USER -d "$db" -tAc "SELECT COUNT(*) FROM ir_ui_view WHERE model LIKE 'syndicat.%';" 2>/dev/null)
                MENUS=$(psql -U $DB_USER -d "$db" -tAc "SELECT COUNT(*) FROM ir_ui_menu WHERE name LIKE '%Syndicat%';" 2>/dev/null)
                
                echo "   📊 $MODELS modèles, $VIEWS vues, $MENUS menus"
                
                echo ""
                echo "🎉 BASE FONCTIONNELLE TROUVÉE!"
                echo "=============================="
                echo "🌐 Pour démarrer le serveur:"
                echo "   cd /var/odoo/odoo18"
                echo "   python3 odoo-bin --addons-path=/home/grand-as/psagsn/custom_addons --database=$db --xmlrpc-port=8070"
                echo ""
                echo "🔗 URL d'accès: http://localhost:8070"
                echo "👤 admin/admin"
                
                # Arrêter après la première base fonctionnelle
                break
                
            elif [ "$MODULE_STATE" = "to install" ]; then
                echo "   ⏳ Module en cours d'installation"
            elif [ "$MODULE_STATE" = "to upgrade" ]; then
                echo "   🔄 Module en cours de mise à jour"
            elif [ -z "$MODULE_STATE" ]; then
                echo "   ❌ Module non trouvé (base non initialisée)"
            else
                echo "   ⚠️  État: $MODULE_STATE"
            fi
        fi
    done
fi

# Vérifier les processus d'installation en cours
echo ""
echo "🔍 Processus d'installation en cours:"
INSTALL_PROCESSES=$(ps aux | grep "odoo-bin.*init.*sama_syndicat" | grep -v grep)
if [ -z "$INSTALL_PROCESSES" ]; then
    echo "❌ Aucun processus d'installation en cours"
else
    echo "✅ Installation en cours détectée:"
    echo "$INSTALL_PROCESSES"
fi

# Vérifier les logs récents
echo ""
echo "📄 Logs d'installation récents:"
if [ -f /tmp/sama_install_fixed.log ]; then
    echo "✅ Log trouvé: /tmp/sama_install_fixed.log"
    echo "📄 Dernières lignes:"
    tail -5 /tmp/sama_install_fixed.log
else
    echo "❌ Aucun log d'installation récent"
fi

unset PGPASSWORD