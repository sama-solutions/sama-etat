#!/bin/bash

# Installation corrigée avec validation du manifeste

echo "🏛️  SAMA SYNDICAT - INSTALLATION CORRIGÉE"
echo "========================================"

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
DB_NAME="sama_syndicat_fixed_$(date +%s)"
DB_USER="odoo"
DB_PASSWORD="odoo"
PORT=8070

echo "🔧 Base: $DB_NAME"

# Activer l'environnement virtuel
source $VENV_PATH/bin/activate

# Étape 1: Validation du manifeste (robuste quel que soit le dossier courant)
echo "🔍 Validation du manifeste..."
MODULE_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$MODULE_DIR/fix_manifest.py"

if [ $? -ne 0 ]; then
    echo "❌ Erreur dans le manifeste"
    exit 1
fi

echo "✅ Manifeste validé"

# Étape 2: Arrêter uniquement les processus sur NOTRE port (pas les autres Odoo)
echo "🛑 Arrêt des processus sur le port $PORT..."
# Essayez avec lsof s'il est disponible, sinon fallback ps/grep
if command -v lsof >/dev/null 2>&1; then
  PIDS=$(lsof -t -i :$PORT 2>/dev/null || true)
  if [ -n "$PIDS" ]; then
    echo "$PIDS" | xargs -r kill -9 || true
  fi
else
  # fallback
  PIDS=$(ps aux | grep odoo-bin | grep "xmlrpc-port=$PORT" | awk '{print $2}')
  if [ -n "$PIDS" ]; then
    echo "$PIDS" | xargs -r kill -9 || true
  fi
fi
sleep 2

# Étape 3: Créer la base
echo "🗄️  Création de la base..."
export PGPASSWORD=$DB_PASSWORD

dropdb -U $DB_USER --if-exists $DB_NAME 2>/dev/null || true
createdb -U $DB_USER -O $DB_USER $DB_NAME

if [ $? -ne 0 ]; then
    echo "❌ Échec de création de la base"
    exit 1
fi

echo "✅ Base créée: $DB_NAME"

# Étape 4: Préparer un addons_path MINIMAL et VALIDE (core + notre module uniquement)
ADDONS_CORE1="/var/odoo/odoo18/odoo/addons"
ADDONS_CORE2="/var/odoo/odoo18/addons"
TMP_ADDONS_DIR="/tmp/addons_sama_syndicat"
mkdir -p "$TMP_ADDONS_DIR"
# Lien symbolique vers ce module uniquement pour éviter les manifests corrompus ailleurs
ln -sfn "$MODULE_DIR" "$TMP_ADDONS_DIR/sama_syndicat"
# Consigner le répertoire addons minimal pour démarrage ultérieur
echo "$TMP_ADDONS_DIR" > "$MODULE_DIR/.addons_min_path"


ADDONS_CLI="$ADDONS_CORE1"
if [ -d "$ADDONS_CORE2" ]; then
  ADDONS_CLI="$ADDONS_CLI,$ADDONS_CORE2"
fi
ADDONS_CLI="$ADDONS_CLI,$TMP_ADDONS_DIR"

echo "🧭 addons_path: $ADDONS_CLI"

# Étape 5: Installation avec logs détaillés
echo "📦 Installation du module sama_syndicat..."
echo "⏳ Cela peut prendre 2-5 minutes..."
cd $ODOO_PATH

# Installation avec timeout de 10 minutes et logs détaillés
timeout 600 python3 odoo-bin \
    --addons-path="$ADDONS_CLI" \
    --database=$DB_NAME \
    --db_user=$DB_USER \
    --db_password=$DB_PASSWORD \
    --init=sama_syndicat \
    --stop-after-init \
    --log-level=info \
    --without-demo=all \
    2>&1 | tee /tmp/sama_install_fixed.log

INSTALL_RESULT=$?

echo ""
echo "📋 RÉSULTAT DE L'INSTALLATION"
echo "============================="

if [ $INSTALL_RESULT -eq 0 ]; then
    echo "✅ Installation terminée avec succès!"
    
    # Vérification détaillée
    MODULE_STATE=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT state FROM ir_module_module WHERE name='sama_syndicat';" 2>/dev/null)
    
    if [ "$MODULE_STATE" = "installed" ]; then
        echo "✅ Module sama_syndicat INSTALLÉ ET ACTIVÉ"
        
        # Statistiques complètes
        MODELS_COUNT=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM ir_model WHERE model LIKE 'syndicat.%';" 2>/dev/null)
        VIEWS_COUNT=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM ir_ui_view WHERE model LIKE 'syndicat.%';" 2>/dev/null)
        MENUS_COUNT=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM ir_ui_menu WHERE name LIKE '%Syndicat%';" 2>/dev/null)
        ACTIONS_COUNT=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM ir_act_window WHERE res_model LIKE 'syndicat.%';" 2>/dev/null)
        GROUPS_COUNT=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM res_groups WHERE name LIKE '%Syndicat%';" 2>/dev/null)
        
        echo ""
        echo "📊 ÉLÉMENTS CRÉÉS AVEC SUCCÈS:"
        echo "   • Modèles de données: $MODELS_COUNT"
        echo "   • Vues XML: $VIEWS_COUNT"
        echo "   • Menus: $MENUS_COUNT"
        echo "   • Actions: $ACTIONS_COUNT"
        echo "   • Groupes de sécurité: $GROUPS_COUNT"
        
        echo ""
        echo "🎉 SAMA SYNDICAT INSTALLÉ AVEC SUCCÈS!"
        echo "======================================"
        echo "🌐 URL d'accès: http://localhost:$PORT"
        echo "🔑 Base de données: $DB_NAME"
        echo "👤 Utilisateur: admin"
        echo "🔐 Mot de passe: admin"
        
        echo ""
        echo "🚀 COMMANDE DE DÉMARRAGE:"
        echo "cd $ODOO_PATH"
        echo "python3 odoo-bin --addons-path=$ADDONS_PATH --database=$DB_NAME --xmlrpc-port=$PORT --log-level=info"
        
        echo ""
        echo "🏛️ FONCTIONNALITÉS DISPONIBLES:"
        echo "   • 📊 Tableau de Bord - Analytics en temps réel"
        echo "   • 👥 Adhérents - Gestion complète des membres"
        echo "   • 🏛️ Assemblées - Vote électronique"
        echo "   • ⚖️ Revendications - Suivi des négociations"
        echo "   • 🚩 Actions Syndicales - Manifestations et grèves"
        echo "   • 📢 Communications - Multi-canaux avec analytics"
        echo "   • 🎓 Formations - Programmes et certifications"
        echo "   • 📋 Conventions - Conventions collectives"
        echo "   • 🤝 Médiations - Gestion des conflits"
        
        echo ""
        echo "🎯 PROCHAINES ÉTAPES:"
        echo "   1. Démarrer le serveur avec la commande ci-dessus"
        echo "   2. Accéder à http://localhost:$PORT"
        echo "   3. Se connecter avec admin/admin"
        echo "   4. Aller dans le menu 'Syndicat'"
        echo "   5. Commencer la configuration des adhérents"
        
    else
        echo "⚠️  Module installé mais état: $MODULE_STATE"
        echo "📄 Vérifiez les logs: /tmp/sama_install_fixed.log"
    fi
    
elif [ $INSTALL_RESULT -eq 124 ]; then
    echo "⏰ Installation interrompue par timeout (10 minutes)"
    echo "💡 L'installation peut avoir réussi partiellement"
    
    # Vérifier quand même
    MODULE_STATE=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT state FROM ir_module_module WHERE name='sama_syndicat';" 2>/dev/null)
    if [ "$MODULE_STATE" = "installed" ]; then
        echo "✅ Module finalement installé malgré le timeout!"
    else
        echo "❌ Module non installé après timeout"
    fi
    
else
    echo "❌ Installation échouée (code: $INSTALL_RESULT)"
    echo ""
    echo "🔍 ANALYSE DES ERREURS:"
    echo "======================"
    
    if [ -f /tmp/sama_install_fixed.log ]; then
        echo "❌ Dernières erreurs:"
        grep -i "error\|critical\|failed\|exception" /tmp/sama_install_fixed.log | tail -5
        
        echo ""
        echo "📄 Dernières lignes du log:"
        tail -10 /tmp/sama_install_fixed.log
    fi
fi

unset PGPASSWORD

echo ""
echo "📄 Log complet: /tmp/sama_install_fixed.log"
echo "🔧 Pour diagnostiquer: ./sama_syndicat/check_status.sh"