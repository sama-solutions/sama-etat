#!/bin/bash

# Script de sauvegarde SAMA SYNDICAT V1 Stable
# Crée une archive complète du module avec horodatage

set -e  # Arrêter le script en cas d'erreur

# Configuration
MODULE_NAME="sama_syndicat"
VERSION="v1.0.0-stable"
BACKUP_DIR="$HOME/backups/sama_syndicat"
SOURCE_DIR="/home/grand-as/psagsn/custom_addons/sama_syndicat"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="${MODULE_NAME}_${VERSION}_${TIMESTAMP}"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   SAMA SYNDICAT V1 - SAUVEGARDE${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Fonction pour afficher les messages
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${PURPLE}[STEP]${NC} $1"
}

# Fonction pour créer le répertoire de sauvegarde
create_backup_dir() {
    log_step "Création du répertoire de sauvegarde..."
    
    if [ ! -d "$BACKUP_DIR" ]; then
        mkdir -p "$BACKUP_DIR"
        log_info "Répertoire créé: $BACKUP_DIR"
    else
        log_info "Répertoire existant: $BACKUP_DIR"
    fi
}

# Fonction pour vérifier l'espace disque
check_disk_space() {
    log_step "Vérification de l'espace disque..."
    
    # Taille du module source
    SOURCE_SIZE=$(du -sm "$SOURCE_DIR" | cut -f1)
    
    # Espace disponible dans le répertoire de sauvegarde
    AVAILABLE_SPACE=$(df -m "$BACKUP_DIR" | awk 'NR==2 {print $4}')
    
    # Marge de sécurité (3x la taille source)
    REQUIRED_SPACE=$((SOURCE_SIZE * 3))
    
    log_info "Taille du module: ${SOURCE_SIZE}MB"
    log_info "Espace disponible: ${AVAILABLE_SPACE}MB"
    log_info "Espace requis: ${REQUIRED_SPACE}MB"
    
    if [ $AVAILABLE_SPACE -lt $REQUIRED_SPACE ]; then
        log_error "Espace disque insuffisant!"
        log_error "Requis: ${REQUIRED_SPACE}MB, Disponible: ${AVAILABLE_SPACE}MB"
        exit 1
    else
        log_success "Espace disque suffisant"
    fi
}

# Fonction pour créer le fichier de métadonnées
create_metadata() {
    log_step "Création des métadonnées de sauvegarde..."
    
    METADATA_FILE="$BACKUP_DIR/${BACKUP_NAME}_metadata.txt"
    
    cat > "$METADATA_FILE" << EOF
SAMA SYNDICAT - Métadonnées de Sauvegarde V1 Stable
===================================================

Informations Générales:
-----------------------
Module: $MODULE_NAME
Version: $VERSION
Date de sauvegarde: $(date '+%Y-%m-%d %H:%M:%S')
Utilisateur: $(whoami)
Hostname: $(hostname)
Système: $(uname -a)

Chemins:
--------
Répertoire source: $SOURCE_DIR
Répertoire sauvegarde: $BACKUP_DIR
Nom de l'archive: ${BACKUP_NAME}.tar.gz

Contenu du Module:
------------------
$(find "$SOURCE_DIR" -type f | wc -l) fichiers
$(find "$SOURCE_DIR" -type d | wc -l) répertoires
Taille totale: $(du -sh "$SOURCE_DIR" | cut -f1)

Structure des Fichiers:
-----------------------
EOF

    # Ajouter la structure des fichiers
    tree "$SOURCE_DIR" >> "$METADATA_FILE" 2>/dev/null || find "$SOURCE_DIR" -type f | sort >> "$METADATA_FILE"
    
    echo "" >> "$METADATA_FILE"
    echo "Checksums MD5:" >> "$METADATA_FILE"
    echo "--------------" >> "$METADATA_FILE"
    find "$SOURCE_DIR" -type f -exec md5sum {} \; | sort >> "$METADATA_FILE"
    
    log_success "Métadonnées créées: $METADATA_FILE"
}

# Fonction pour créer l'archive
create_archive() {
    log_step "Création de l'archive de sauvegarde..."
    
    ARCHIVE_PATH="$BACKUP_DIR/${BACKUP_NAME}.tar.gz"
    
    # Aller dans le répertoire parent pour inclure le nom du dossier dans l'archive
    cd "$(dirname "$SOURCE_DIR")"
    
    # Créer l'archive avec compression
    tar -czf "$ARCHIVE_PATH" \
        --exclude='*.pyc' \
        --exclude='__pycache__' \
        --exclude='*.log' \
        --exclude='.git' \
        --exclude='node_modules' \
        "$(basename "$SOURCE_DIR")"
    
    if [ $? -eq 0 ]; then
        log_success "Archive créée: $ARCHIVE_PATH"
        
        # Afficher la taille de l'archive
        ARCHIVE_SIZE=$(du -sh "$ARCHIVE_PATH" | cut -f1)
        log_info "Taille de l'archive: $ARCHIVE_SIZE"
        
        # Vérifier l'intégrité de l'archive
        log_info "Vérification de l'intégrité de l'archive..."
        if tar -tzf "$ARCHIVE_PATH" > /dev/null 2>&1; then
            log_success "Archive valide et intègre"
        else
            log_error "Archive corrompue!"
            exit 1
        fi
    else
        log_error "Échec de la création de l'archive"
        exit 1
    fi
}

# Fonction pour créer un checksum de l'archive
create_checksum() {
    log_step "Création du checksum de l'archive..."
    
    ARCHIVE_PATH="$BACKUP_DIR/${BACKUP_NAME}.tar.gz"
    CHECKSUM_FILE="$BACKUP_DIR/${BACKUP_NAME}.md5"
    
    cd "$BACKUP_DIR"
    md5sum "$(basename "$ARCHIVE_PATH")" > "$CHECKSUM_FILE"
    
    log_success "Checksum créé: $CHECKSUM_FILE"
    log_info "MD5: $(cat "$CHECKSUM_FILE")"
}

# Fonction pour nettoyer les anciennes sauvegardes
cleanup_old_backups() {
    log_step "Nettoyage des anciennes sauvegardes..."
    
    # Garder seulement les 5 dernières sauvegardes
    KEEP_COUNT=5
    
    # Compter les sauvegardes existantes
    BACKUP_COUNT=$(ls -1 "$BACKUP_DIR"/${MODULE_NAME}_*.tar.gz 2>/dev/null | wc -l)
    
    if [ $BACKUP_COUNT -gt $KEEP_COUNT ]; then
        log_info "Suppression des anciennes sauvegardes (garder les $KEEP_COUNT dernières)..."
        
        # Supprimer les plus anciennes
        ls -1t "$BACKUP_DIR"/${MODULE_NAME}_*.tar.gz | tail -n +$((KEEP_COUNT + 1)) | while read file; do
            log_info "Suppression: $(basename "$file")"
            rm -f "$file"
            # Supprimer aussi les fichiers associés
            rm -f "${file%.tar.gz}.md5"
            rm -f "${file%.tar.gz}_metadata.txt"
        done
        
        log_success "Nettoyage terminé"
    else
        log_info "Aucun nettoyage nécessaire ($BACKUP_COUNT sauvegardes)"
    fi
}

# Fonction pour afficher le résumé
show_summary() {
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}   SAUVEGARDE TERMINÉE AVEC SUCCÈS${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${YELLOW}Résumé de la sauvegarde:${NC}"
    echo -e "  📦 Archive: ${BACKUP_NAME}.tar.gz"
    echo -e "  📍 Emplacement: $BACKUP_DIR"
    echo -e "  📊 Taille: $(du -sh "$BACKUP_DIR/${BACKUP_NAME}.tar.gz" | cut -f1)"
    echo -e "  🕒 Date: $(date '+%Y-%m-%d %H:%M:%S')"
    echo -e "  ✅ Version: $VERSION"
    echo ""
    echo -e "${YELLOW}Fichiers créés:${NC}"
    echo -e "  • ${BACKUP_NAME}.tar.gz (archive principale)"
    echo -e "  • ${BACKUP_NAME}.md5 (checksum)"
    echo -e "  • ${BACKUP_NAME}_metadata.txt (métadonnées)"
    echo ""
    echo -e "${YELLOW}Pour restaurer cette sauvegarde:${NC}"
    echo -e "  tar -xzf $BACKUP_DIR/${BACKUP_NAME}.tar.gz"
    echo ""
}

# Fonction pour créer un script de restauration
create_restore_script() {
    log_step "Création du script de restauration..."
    
    RESTORE_SCRIPT="$BACKUP_DIR/restore_${BACKUP_NAME}.sh"
    
    cat > "$RESTORE_SCRIPT" << EOF
#!/bin/bash

# Script de restauration automatique pour SAMA SYNDICAT V1
# Archive: ${BACKUP_NAME}.tar.gz
# Créé le: $(date '+%Y-%m-%d %H:%M:%S')

set -e

ARCHIVE_PATH="$BACKUP_DIR/${BACKUP_NAME}.tar.gz"
RESTORE_PATH="/home/grand-as/psagsn/custom_addons"

echo "🔄 Restauration de SAMA SYNDICAT V1..."
echo "Archive: \$ARCHIVE_PATH"
echo "Destination: \$RESTORE_PATH"
echo ""

# Vérifier que l'archive existe
if [ ! -f "\$ARCHIVE_PATH" ]; then
    echo "❌ Archive non trouvée: \$ARCHIVE_PATH"
    exit 1
fi

# Vérifier l'intégrité
echo "🔍 Vérification de l'intégrité..."
if ! tar -tzf "\$ARCHIVE_PATH" > /dev/null 2>&1; then
    echo "❌ Archive corrompue!"
    exit 1
fi

# Sauvegarder la version actuelle si elle existe
if [ -d "\$RESTORE_PATH/sama_syndicat" ]; then
    echo "💾 Sauvegarde de la version actuelle..."
    mv "\$RESTORE_PATH/sama_syndicat" "\$RESTORE_PATH/sama_syndicat.backup.\$(date +%Y%m%d_%H%M%S)"
fi

# Extraire l'archive
echo "📦 Extraction de l'archive..."
cd "\$RESTORE_PATH"
tar -xzf "\$ARCHIVE_PATH"

echo "✅ Restauration terminée avec succès!"
echo "📍 Module restauré dans: \$RESTORE_PATH/sama_syndicat"
EOF

    chmod +x "$RESTORE_SCRIPT"
    log_success "Script de restauration créé: $RESTORE_SCRIPT"
}

# Fonction principale
main() {
    echo -e "${GREEN}Configuration de la sauvegarde:${NC}"
    echo -e "  Module: ${YELLOW}$MODULE_NAME${NC}"
    echo -e "  Version: ${YELLOW}$VERSION${NC}"
    echo -e "  Source: ${YELLOW}$SOURCE_DIR${NC}"
    echo -e "  Destination: ${YELLOW}$BACKUP_DIR${NC}"
    echo -e "  Archive: ${YELLOW}${BACKUP_NAME}.tar.gz${NC}"
    echo ""
    
    # Vérifier que le répertoire source existe
    if [ ! -d "$SOURCE_DIR" ]; then
        log_error "Répertoire source non trouvé: $SOURCE_DIR"
        exit 1
    fi
    
    # Exécuter les étapes de sauvegarde
    create_backup_dir
    check_disk_space
    create_metadata
    create_archive
    create_checksum
    create_restore_script
    cleanup_old_backups
    show_summary
    
    log_success "Sauvegarde V1 stable terminée avec succès!"
}

# Gestion des signaux pour un arrêt propre
trap 'log_warning "Sauvegarde interrompue par l'\''utilisateur"; exit 1' SIGINT SIGTERM

# Exécution du script principal
main