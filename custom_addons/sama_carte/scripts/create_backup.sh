#!/bin/bash

# Script de sauvegarde complète du module sama_carte
# Crée une archive avec timestamp et informations de version

echo "🔄 CRÉATION SAUVEGARDE SAMA_CARTE"
echo "================================="
echo ""

# Variables
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
MODULE_NAME="sama_carte"
BACKUP_NAME="${MODULE_NAME}_v2.1_templates_fixed_${TIMESTAMP}"
BACKUP_DIR="../backups"
SOURCE_DIR="."

# Créer le répertoire de backup s'il n'existe pas
mkdir -p "$BACKUP_DIR"

echo "📁 Configuration:"
echo "  Source: $SOURCE_DIR"
echo "  Destination: $BACKUP_DIR/$BACKUP_NAME.tar.gz"
echo "  Timestamp: $TIMESTAMP"
echo ""

# Informations sur l'état actuel
echo "📊 État actuel du module:"
echo "========================"

# Compter les fichiers
total_files=$(find . -type f | wc -l)
echo "  📄 Fichiers total: $total_files"

# Taille du module
module_size=$(du -sh . | cut -f1)
echo "  📏 Taille: $module_size"

# Derniers commits
echo "  📝 Derniers commits:"
git log --oneline -5 | sed 's/^/    /'

echo ""

# Créer le fichier d'informations
echo "🔍 Création fichier d'informations..."
cat > "BACKUP_INFO_${TIMESTAMP}.md" << EOF
# SAUVEGARDE SAMA_CARTE - $(date)

## Informations Générales
- **Module**: sama_carte
- **Version**: 2.1 - Templates Fixed
- **Date**: $(date)
- **Timestamp**: $TIMESTAMP
- **Taille**: $module_size
- **Fichiers**: $total_files

## État des Templates
$(python3 -c "
import psycopg2
try:
    conn = psycopg2.connect(host='localhost', database='sama_carte_demo', user='odoo', password='odoo')
    cur = conn.cursor()
    cur.execute('SELECT name, technical_name, active, sequence FROM membership_card_template ORDER BY sequence, name')
    templates = cur.fetchall()
    print('### Templates Actifs:')
    for t in templates:
        if t[2]:  # active
            print(f'- ✅ {t[1]} - {t[0]} (séquence {t[3]})')
    print('\n### Templates Inactifs:')
    for t in templates:
        if not t[2]:  # inactive
            print(f'- ❌ {t[1]} - {t[0]} (séquence {t[3]})')
    conn.close()
except:
    print('❌ Impossible de récupérer l\'état des templates')
")

## Derniers Commits
\`\`\`
$(git log --oneline -10)
\`\`\`

## Fonctionnalités Principales
- ✅ Gestion des membres avec QR codes
- ✅ Templates de cartes personnalisables
- ✅ Backgrounds dynamiques
- ✅ Interface web publique
- ✅ Système d'impression PDF
- ✅ Filtrage intelligent des templates
- ✅ Interface d'administration

## Corrections Récentes
- ✅ Correction erreurs vues Odoo 18
- ✅ Filtrage templates actifs/inactifs
- ✅ Menus différenciés utilisateur/admin
- ✅ Background dans cadre uniquement
- ✅ Photo et QR en haut, tailles augmentées
- ✅ Libellés boutons clarifiés

## Structure Technique
- **Modèles**: membership.member, membership.card.template, membership.card.background
- **Vues**: Kanban, Liste, Formulaire, Graphique, Pivot, Calendrier
- **Contrôleurs**: Web publique, API, Debug
- **Templates**: QWeb pour cartes, backgrounds, galeries
- **Données**: Templates prédéfinis, backgrounds, séquences

## Tests Validés
- ✅ Interface Odoo stable
- ✅ Menus templates fonctionnels
- ✅ Filtrage automatique
- ✅ Création dynamique
- ✅ Navigation fluide
- ✅ Permissions respectées

EOF

echo "✅ Fichier d'informations créé"

# Créer l'archive
echo "📦 Création de l'archive..."
tar -czf "$BACKUP_DIR/$BACKUP_NAME.tar.gz" \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='*.log' \
    --exclude='.DS_Store' \
    --exclude='backup' \
    --exclude='backups' \
    .

# Vérifier la création
if [ -f "$BACKUP_DIR/$BACKUP_NAME.tar.gz" ]; then
    backup_size=$(du -sh "$BACKUP_DIR/$BACKUP_NAME.tar.gz" | cut -f1)
    echo "✅ Archive créée avec succès"
    echo "  📁 Fichier: $BACKUP_DIR/$BACKUP_NAME.tar.gz"
    echo "  📏 Taille: $backup_size"
    
    # Lister le contenu pour vérification
    echo ""
    echo "📋 Contenu de l'archive:"
    tar -tzf "$BACKUP_DIR/$BACKUP_NAME.tar.gz" | head -20
    if [ $(tar -tzf "$BACKUP_DIR/$BACKUP_NAME.tar.gz" | wc -l) -gt 20 ]; then
        echo "  ... et $(( $(tar -tzf "$BACKUP_DIR/$BACKUP_NAME.tar.gz" | wc -l) - 20 )) autres fichiers"
    fi
    
    # Nettoyer le fichier d'info temporaire
    rm -f "BACKUP_INFO_${TIMESTAMP}.md"
    
    echo ""
    echo "🎉 SAUVEGARDE TERMINÉE AVEC SUCCÈS !"
    echo "=================================="
    echo "📁 Archive: $BACKUP_DIR/$BACKUP_NAME.tar.gz"
    echo "📏 Taille: $backup_size"
    echo "📅 Date: $(date)"
    echo ""
    echo "💡 Pour restaurer:"
    echo "   cd /path/to/restore"
    echo "   tar -xzf $BACKUP_DIR/$BACKUP_NAME.tar.gz"
    
else
    echo "❌ Erreur lors de la création de l'archive"
    rm -f "BACKUP_INFO_${TIMESTAMP}.md"
    exit 1
fi