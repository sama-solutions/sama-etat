#!/bin/bash

# Script de sauvegarde complète : module + base de données + état système

echo "🔄 SAUVEGARDE COMPLÈTE SAMA_CARTE"
echo "================================="
echo ""

# Variables
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="../backups"
COMPLETE_BACKUP="${BACKUP_DIR}/sama_carte_complete_${TIMESTAMP}"

# Créer le répertoire de backup
mkdir -p "$BACKUP_DIR"
mkdir -p "$COMPLETE_BACKUP"

echo "📁 Sauvegarde complète dans: $COMPLETE_BACKUP"
echo "📅 Timestamp: $TIMESTAMP"
echo ""

# 1. Sauvegarde du module
echo "📦 1. SAUVEGARDE DU MODULE"
echo "========================="
./scripts/create_backup.sh
if [ $? -eq 0 ]; then
    # Déplacer l'archive du module dans le dossier complet
    latest_module=$(ls -t ../backups/sama_carte_v2.1_templates_fixed_*.tar.gz | head -1)
    cp "$latest_module" "$COMPLETE_BACKUP/module.tar.gz"
    echo "✅ Module sauvegardé"
else
    echo "❌ Erreur sauvegarde module"
    exit 1
fi

echo ""

# 2. Sauvegarde de la base de données
echo "🗄️ 2. SAUVEGARDE BASE DE DONNÉES"
echo "==============================="
./scripts/backup_database.sh
if [ $? -eq 0 ]; then
    # Déplacer l'archive de la base dans le dossier complet
    latest_db=$(ls -t ../backups/sama_carte_db_*.sql.gz | head -1)
    cp "$latest_db" "$COMPLETE_BACKUP/database.sql.gz"
    echo "✅ Base de données sauvegardée"
else
    echo "❌ Erreur sauvegarde base de données"
    exit 1
fi

echo ""

# 3. État du système
echo "⚙️ 3. ÉTAT DU SYSTÈME"
echo "===================="

# Créer un fichier d'état système
cat > "$COMPLETE_BACKUP/system_state.md" << EOF
# ÉTAT SYSTÈME SAMA_CARTE - $(date)

## Informations Serveur
- **Date**: $(date)
- **Utilisateur**: $(whoami)
- **Répertoire**: $(pwd)
- **Système**: $(uname -a)

## État Odoo
- **Version**: 18.0
- **Port**: 8071
- **Base**: sama_carte_demo
- **Statut**: $(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8071" || echo "Non accessible")

## État Git
\`\`\`
$(git status --porcelain)
\`\`\`

### Derniers commits:
\`\`\`
$(git log --oneline -10)
\`\`\`

### Branche actuelle:
\`\`\`
$(git branch --show-current)
\`\`\`

## Configuration Templates
$(python3 -c "
import psycopg2
try:
    conn = psycopg2.connect(host='localhost', database='sama_carte_demo', user='odoo', password='odoo')
    cur = conn.cursor()
    
    # Templates actifs
    cur.execute('SELECT name, technical_name, sequence FROM membership_card_template WHERE active = true ORDER BY sequence')
    actifs = cur.fetchall()
    print('### Templates Actifs:')
    for t in actifs:
        print(f'- {t[2]}. {t[0]} ({t[1]})')
    
    # Statistiques
    cur.execute('SELECT COUNT(*) FROM membership_member')
    membres = cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM membership_card_template')
    templates = cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM membership_card_background')
    backgrounds = cur.fetchone()[0]
    
    print(f'\n### Statistiques:')
    print(f'- Membres: {membres}')
    print(f'- Templates: {templates}')
    print(f'- Backgrounds: {backgrounds}')
    
    conn.close()
except Exception as e:
    print(f'❌ Erreur: {e}')
")

## Fichiers Principaux
- **Module**: $(du -sh . | cut -f1)
- **Fichiers**: $(find . -type f | wc -l)
- **Répertoires**: $(find . -type d | wc -l)

## Tests Fonctionnels
- **Interface**: $(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8071" 2>/dev/null || echo "❌")
- **Login**: $(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8071/web/login" 2>/dev/null || echo "❌")

## Permissions
\`\`\`
$(ls -la | head -10)
\`\`\`

EOF

echo "✅ État système documenté"

# 4. Scripts de restauration
echo ""
echo "📝 4. SCRIPTS DE RESTAURATION"
echo "============================="

# Script de restauration
cat > "$COMPLETE_BACKUP/restore.sh" << 'EOF'
#!/bin/bash

echo "🔄 RESTAURATION SAMA_CARTE"
echo "=========================="
echo ""

if [ $# -eq 0 ]; then
    echo "Usage: $0 <répertoire_destination>"
    echo "Exemple: $0 /home/user/restored_sama_carte"
    exit 1
fi

DEST_DIR="$1"
CURRENT_DIR=$(dirname "$0")

echo "📁 Destination: $DEST_DIR"
echo "📁 Source: $CURRENT_DIR"
echo ""

# Créer le répertoire de destination
mkdir -p "$DEST_DIR"

# Restaurer le module
echo "📦 Restauration du module..."
cd "$DEST_DIR"
tar -xzf "$CURRENT_DIR/module.tar.gz"
echo "✅ Module restauré"

echo ""
echo "🗄️ Pour restaurer la base de données:"
echo "1. Créer une nouvelle base:"
echo "   createdb -h localhost -U odoo nouvelle_base"
echo "2. Restaurer les données:"
echo "   gunzip -c $CURRENT_DIR/database.sql.gz | psql -h localhost -U odoo -d nouvelle_base"
echo ""
echo "✅ Restauration terminée dans: $DEST_DIR"
EOF

chmod +x "$COMPLETE_BACKUP/restore.sh"
echo "✅ Script de restauration créé"

# 5. Créer l'archive finale
echo ""
echo "🗜️ 5. ARCHIVE FINALE"
echo "=================="

cd "$BACKUP_DIR"
tar -czf "sama_carte_complete_${TIMESTAMP}.tar.gz" "sama_carte_complete_${TIMESTAMP}/"

if [ -f "sama_carte_complete_${TIMESTAMP}.tar.gz" ]; then
    final_size=$(du -sh "sama_carte_complete_${TIMESTAMP}.tar.gz" | cut -f1)
    echo "✅ Archive finale créée"
    echo "  📁 Fichier: $BACKUP_DIR/sama_carte_complete_${TIMESTAMP}.tar.gz"
    echo "  📏 Taille: $final_size"
    
    # Nettoyer le dossier temporaire
    rm -rf "sama_carte_complete_${TIMESTAMP}/"
    
    echo ""
    echo "🎉 SAUVEGARDE COMPLÈTE TERMINÉE !"
    echo "================================="
    echo "📁 Archive: sama_carte_complete_${TIMESTAMP}.tar.gz"
    echo "📏 Taille: $final_size"
    echo "📅 Date: $(date)"
    echo ""
    echo "📋 Contenu:"
    echo "  - Module sama_carte complet"
    echo "  - Base de données sama_carte_demo"
    echo "  - État système et configuration"
    echo "  - Scripts de restauration"
    echo ""
    echo "💡 Pour restaurer:"
    echo "   tar -xzf sama_carte_complete_${TIMESTAMP}.tar.gz"
    echo "   cd sama_carte_complete_${TIMESTAMP}"
    echo "   ./restore.sh /path/to/destination"
    
else
    echo "❌ Erreur lors de la création de l'archive finale"
    exit 1
fi