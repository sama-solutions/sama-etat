#!/bin/bash

# Script de restauration SAMA SYNDICAT V1.5
# Date: 02 Septembre 2025
# Version: 1.5 - Dashboards Modernes

echo "🔄 RESTAURATION SAMA SYNDICAT V1.5"
echo "=================================="

# Configuration
BACKUP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${1:-/tmp/addons_sama_syndicat/sama_syndicat}"
ODOO_BIN="${2:-/var/odoo/odoo18/odoo-bin}"
DATABASE="${3:-sama_syndicat_v1_5}"
PORT="${4:-8070}"

echo "📁 Répertoire de sauvegarde: $BACKUP_DIR"
echo "📁 Répertoire cible: $TARGET_DIR"
echo "🐍 Odoo binaire: $ODOO_BIN"
echo "🗄️ Base de données: $DATABASE"
echo "🌐 Port: $PORT"
echo ""

# Vérifications préliminaires
echo "🔍 Vérifications préliminaires..."

if [ ! -f "$ODOO_BIN" ]; then
    echo "❌ Erreur: Odoo non trouvé à $ODOO_BIN"
    echo "💡 Usage: $0 [target_dir] [odoo_bin] [database] [port]"
    exit 1
fi

if [ ! -d "$BACKUP_DIR/models" ]; then
    echo "❌ Erreur: Sauvegarde incomplète (dossier models manquant)"
    exit 1
fi

echo "✅ Vérifications OK"

# Création du répertoire cible
echo "📁 Création du répertoire cible..."
mkdir -p "$TARGET_DIR"
mkdir -p "$(dirname "$TARGET_DIR")"

# Copie des fichiers
echo "📋 Copie des fichiers de la V1.5..."

# Copier tous les dossiers et fichiers
cp -r "$BACKUP_DIR/models" "$TARGET_DIR/"
cp -r "$BACKUP_DIR/views" "$TARGET_DIR/"
cp -r "$BACKUP_DIR/static" "$TARGET_DIR/"
cp -r "$BACKUP_DIR/security" "$TARGET_DIR/"
cp -r "$BACKUP_DIR/data" "$TARGET_DIR/"
cp -r "$BACKUP_DIR/controllers" "$TARGET_DIR/"

# Copier les fichiers principaux
cp "$BACKUP_DIR/__manifest__.py" "$TARGET_DIR/"
cp "$BACKUP_DIR/__init__.py" "$TARGET_DIR/"

# Copier les scripts dans le répertoire cible
mkdir -p "$TARGET_DIR/scripts"
cp -r "$BACKUP_DIR/scripts/"* "$TARGET_DIR/"

# Copier la documentation
mkdir -p "$TARGET_DIR/documentation"
cp -r "$BACKUP_DIR/documentation/"* "$TARGET_DIR/"

echo "✅ Fichiers copiés avec succès"

# Arrêter les processus Odoo existants
echo "🛑 Arrêt des processus Odoo existants..."
pkill -f odoo-bin 2>/dev/null || true
sleep 2

# Démarrage d'Odoo avec la V1.5
echo "🚀 Démarrage d'Odoo avec SAMA SYNDICAT V1.5..."

cd "$TARGET_DIR"

# Construire le chemin des addons
ADDONS_PATH="/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,$(dirname "$TARGET_DIR")"

# Commande de démarrage
ODOO_CMD="python3 $ODOO_BIN --addons-path=$ADDONS_PATH --database=$DATABASE --xmlrpc-port=$PORT --dev=reload,xml --log-level=warn"

echo "📝 Commande: $ODOO_CMD"
echo ""

# Démarrer Odoo en arrière-plan
$ODOO_CMD &
ODOO_PID=$!

echo "⏳ Attente du démarrage d'Odoo (PID: $ODOO_PID)..."

# Attendre que Odoo soit prêt
MAX_WAIT=60
WAIT_TIME=0

while [ $WAIT_TIME -lt $MAX_WAIT ]; do
    if curl -s "http://localhost:$PORT/web/database/selector" > /dev/null 2>&1; then
        echo "✅ Odoo démarré avec succès !"
        break
    fi
    
    if ! kill -0 $ODOO_PID 2>/dev/null; then
        echo "❌ Odoo s'est arrêté de manière inattendue"
        exit 1
    fi
    
    sleep 2
    WAIT_TIME=$((WAIT_TIME + 2))
    echo "⏳ Attente... (${WAIT_TIME}s/${MAX_WAIT}s)"
done

if [ $WAIT_TIME -ge $MAX_WAIT ]; then
    echo "❌ Timeout - Odoo n'a pas démarré à temps"
    kill $ODOO_PID 2>/dev/null || true
    exit 1
fi

# Nettoyage des anciens menus (si le script existe)
if [ -f "clean_old_menus.py" ]; then
    echo "🧹 Nettoyage des anciens menus..."
    python3 clean_old_menus.py
fi

echo ""
echo "🎊 RESTAURATION SAMA SYNDICAT V1.5 TERMINÉE !"
echo "============================================="
echo ""
echo "📊 DASHBOARDS MODERNES DISPONIBLES:"
echo "├── 📊 Dashboard Principal (Cartes Modernes)"
echo "├── 👔 Dashboard Exécutif (Interface Premium)"
echo "└── 📋 Autres fonctionnalités complètes"
echo ""
echo "🌐 Interface web: http://localhost:$PORT/web"
echo "🔑 Connexion: admin/admin"
echo "📁 Module installé dans: $TARGET_DIR"
echo ""
echo "💡 INSTRUCTIONS:"
echo "1. Ouvrez http://localhost:$PORT/web"
echo "2. Connectez-vous (admin/admin)"
echo "3. Allez dans le menu Syndicat"
echo "4. Testez les dashboards modernes !"
echo ""
echo "🛠️ SCRIPTS DISPONIBLES:"
echo "├── start_modern_dashboards.py  - Démarrage avec dashboards modernes"
echo "├── clean_old_menus.py          - Nettoyage des anciens menus"
echo "├── force_menu_update.py        - Mise à jour forcée"
echo "└── apply_final_corrections.py  - Application des corrections"
echo ""
echo "🛑 Pour arrêter Odoo: pkill -f odoo-bin"
echo ""
echo "✅ SAMA SYNDICAT V1.5 OPÉRATIONNEL !"