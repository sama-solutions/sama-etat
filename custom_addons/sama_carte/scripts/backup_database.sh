#!/bin/bash

# Script de sauvegarde de la base de données sama_carte_demo

echo "🗄️ SAUVEGARDE BASE DE DONNÉES"
echo "============================="
echo ""

# Variables
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DB_NAME="sama_carte_demo"
BACKUP_DIR="../backups"
BACKUP_FILE="${BACKUP_DIR}/sama_carte_db_${TIMESTAMP}.sql"

# Créer le répertoire de backup s'il n'existe pas
mkdir -p "$BACKUP_DIR"

echo "📊 Configuration:"
echo "  Base de données: $DB_NAME"
echo "  Fichier: $BACKUP_FILE"
echo "  Timestamp: $TIMESTAMP"
echo ""

# Vérifier la connexion à la base
echo "🔍 Vérification de la base de données..."
export PGPASSWORD=odoo
if pg_isready -h localhost -U odoo -d $DB_NAME > /dev/null 2>&1; then
    echo "✅ Connexion à la base de données OK"
else
    echo "❌ Impossible de se connecter à la base de données"
    exit 1
fi

# Informations sur la base
echo ""
echo "📈 Informations sur la base:"
psql -h localhost -U odoo -d $DB_NAME -t -c "
SELECT 
    'Membres: ' || COUNT(*) 
FROM membership_member;
" 2>/dev/null

psql -h localhost -U odoo -d $DB_NAME -t -c "
SELECT 
    'Templates: ' || COUNT(*) || ' (Actifs: ' || SUM(CASE WHEN active THEN 1 ELSE 0 END) || ')'
FROM membership_card_template;
" 2>/dev/null

psql -h localhost -U odoo -d $DB_NAME -t -c "
SELECT 
    'Backgrounds: ' || COUNT(*)
FROM membership_card_background;
" 2>/dev/null

echo ""

# Créer la sauvegarde
echo "💾 Création de la sauvegarde..."
pg_dump -h localhost -U odoo -d $DB_NAME > "$BACKUP_FILE" 2>/dev/null

# Vérifier la création
if [ -f "$BACKUP_FILE" ]; then
    backup_size=$(du -sh "$BACKUP_FILE" | cut -f1)
    lines=$(wc -l < "$BACKUP_FILE")
    
    echo "✅ Sauvegarde créée avec succès"
    echo "  📁 Fichier: $BACKUP_FILE"
    echo "  📏 Taille: $backup_size"
    echo "  📄 Lignes: $lines"
    
    # Compresser la sauvegarde
    echo ""
    echo "🗜️ Compression de la sauvegarde..."
    gzip "$BACKUP_FILE"
    
    if [ -f "${BACKUP_FILE}.gz" ]; then
        compressed_size=$(du -sh "${BACKUP_FILE}.gz" | cut -f1)
        echo "✅ Compression réussie"
        echo "  📁 Fichier compressé: ${BACKUP_FILE}.gz"
        echo "  📏 Taille compressée: $compressed_size"
        
        echo ""
        echo "🎉 SAUVEGARDE BASE DE DONNÉES TERMINÉE !"
        echo "======================================="
        echo "📁 Archive: ${BACKUP_FILE}.gz"
        echo "📏 Taille: $compressed_size"
        echo "📅 Date: $(date)"
        echo ""
        echo "💡 Pour restaurer:"
        echo "   gunzip ${BACKUP_FILE}.gz"
        echo "   psql -h localhost -U odoo -d nouvelle_base < $BACKUP_FILE"
        
    else
        echo "⚠️ Compression échouée, mais sauvegarde disponible non compressée"
    fi
    
else
    echo "❌ Erreur lors de la création de la sauvegarde"
    exit 1
fi