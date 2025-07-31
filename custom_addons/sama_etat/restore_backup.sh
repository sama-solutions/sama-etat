#!/bin/bash

# SAMA ÉTAT - Quick Restore Script
# ================================
# This script provides quick restoration options for SAMA ÉTAT backups
# Use with caution - always test in development environment first

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKUP_BASE_DIR="/home/grand-as/backups"
PROJECT_DIR="/home/grand-as/psagsn/custom_addons"
PROJECT_NAME="sama_etat"

# Logging functions
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] ✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] ⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ❌ $1${NC}"
}

# Function to show available backups
show_available_backups() {
    echo ""
    echo "📋 Available SAMA ÉTAT Backups:"
    echo "==============================="

    if [ -d "$BACKUP_BASE_DIR" ]; then
        ls -la "$BACKUP_BASE_DIR" | grep sama_etat_backup || echo "No backups found"
        echo ""
        ls -la "$BACKUP_BASE_DIR" | grep sama_etat_complete_backup || echo "No compressed backups found"
    else
        log_error "Backup directory not found: $BACKUP_BASE_DIR"
        return 1
    fi
}

# Function to validate backup
validate_backup() {
    local backup_path=$1

    log "Validating backup: $backup_path"

    if [[ "$backup_path" == *.tar.gz ]]; then
        # Test compressed archive
        if tar -tzf "$backup_path" >/dev/null 2>&1; then
            log_success "Archive integrity verified"
            return 0
        else
            log_error "Archive is corrupted"
            return 1
        fi
    elif [ -d "$backup_path" ]; then
        # Test directory backup
        if [ -d "$backup_path/source_code/sama_etat" ]; then
            log_success "Directory backup structure verified"
            return 0
        else
            log_error "Backup directory structure is invalid"
            return 1
        fi
    else
        log_error "Backup path not found: $backup_path"
        return 1
    fi
}

# Function to restore source code only
restore_source_only() {
    local backup_path=$1
    local create_backup_current=${2:-true}

    log "Starting source code restoration..."

    # Create backup of current version if requested
    if [ "$create_backup_current" = true ] && [ -d "$PROJECT_DIR/$PROJECT_NAME" ]; then
        local current_backup="${PROJECT_DIR}/${PROJECT_NAME}_current_backup_$(date +%Y%m%d_%H%M%S)"
        log "Creating backup of current version: $current_backup"
        cp -r "$PROJECT_DIR/$PROJECT_NAME" "$current_backup"
        log_success "Current version backed up to: $current_backup"
    fi

    # Remove current version
    if [ -d "$PROJECT_DIR/$PROJECT_NAME" ]; then
        log_warning "Removing current SAMA ÉTAT installation..."
        rm -rf "$PROJECT_DIR/$PROJECT_NAME"
    fi

    # Extract backup
    if [[ "$backup_path" == *.tar.gz ]]; then
        log "Extracting from compressed backup..."
        cd "$PROJECT_DIR"
        tar -xzf "$backup_path" --strip-components=2 "*/source_code/sama_etat"
    else
        log "Copying from directory backup..."
        cp -r "$backup_path/source_code/sama_etat" "$PROJECT_DIR/"
    fi

    log_success "Source code restored successfully"
}

# Function to restore database
restore_database() {
    local backup_path=$1
    local db_name=$2

    log "Starting database restoration for: $db_name"

    # Find SQL file
    local sql_file=""
    if [[ "$backup_path" == *.tar.gz ]]; then
        # Extract database files
        local temp_dir="/tmp/sama_etat_restore_$$"
        mkdir -p "$temp_dir"
        tar -xzf "$backup_path" -C "$temp_dir" "*/database/"
        sql_file=$(find "$temp_dir" -name "${db_name}_*.sql" | head -1)
    else
        sql_file=$(find "$backup_path/database" -name "${db_name}_*.sql" | head -1)
    fi

    if [ -z "$sql_file" ] || [ ! -f "$sql_file" ]; then
        log_error "Database backup file not found for: $db_name"
        return 1
    fi

    log "Found database backup: $sql_file"

    # Ask for confirmation
    echo ""
    log_warning "⚠️  WARNING: This will completely replace the database '$db_name'"
    read -p "Are you sure you want to continue? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        log "Database restoration cancelled"
        return 1
    fi

    # Drop and recreate database
    log "Dropping existing database..."
    dropdb "$db_name" 2>/dev/null || log_warning "Database $db_name didn't exist"

    log "Creating new database..."
    createdb "$db_name"

    log "Restoring database from backup..."
    psql "$db_name" < "$sql_file"

    log_success "Database restored successfully"

    # Cleanup temp directory if used
    if [[ "$backup_path" == *.tar.gz ]] && [ -d "/tmp/sama_etat_restore_$$" ]; then
        rm -rf "/tmp/sama_etat_restore_$$"
    fi
}

# Function to restart Odoo
restart_odoo() {
    log "Restarting Odoo service..."

    if systemctl is-active --quiet odoo; then
        sudo systemctl restart odoo
        log_success "Odoo service restarted"
    else
        log_warning "Odoo service was not running, starting it..."
        sudo systemctl start odoo
        if systemctl is-active --quiet odoo; then
            log_success "Odoo service started"
        else
            log_error "Failed to start Odoo service"
            return 1
        fi
    fi

    # Wait for Odoo to be ready
    log "Waiting for Odoo to be ready..."
    sleep 10
    log_success "Odoo should be ready now"
}

# Function for complete restoration
restore_complete() {
    local backup_path=$1
    local db_name=${2:-"sama_etat_db"}

    echo ""
    echo "🔄 COMPLETE RESTORATION"
    echo "======================"
    echo "Backup: $backup_path"
    echo "Database: $db_name"
    echo ""

    # Validate backup first
    if ! validate_backup "$backup_path"; then
        log_error "Backup validation failed. Aborting restoration."
        return 1
    fi

    # Confirm complete restoration
    log_warning "⚠️  WARNING: This will completely replace both source code and database"
    read -p "Are you absolutely sure? (type 'RESTORE' to confirm): " confirm
    if [ "$confirm" != "RESTORE" ]; then
        log "Complete restoration cancelled"
        return 1
    fi

    # Stop Odoo during restoration
    log "Stopping Odoo service for restoration..."
    sudo systemctl stop odoo

    # Restore source code
    restore_source_only "$backup_path" true

    # Restore database
    restore_database "$backup_path" "$db_name"

    # Restart Odoo
    restart_odoo

    log_success "🎉 Complete restoration completed successfully!"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Test SAMA ÉTAT functionality"
    echo "2. Verify map displays correctly"
    echo "3. Check all modules are working"
    echo "4. Test public dashboard access"
}

# Function to show help
show_help() {
    echo ""
    echo "🔧 SAMA ÉTAT Restore Script"
    echo "=========================="
    echo ""
    echo "Usage: $0 [OPTION] [BACKUP_PATH] [DATABASE_NAME]"
    echo ""
    echo "Options:"
    echo "  -l, --list           List available backups"
    echo "  -s, --source-only    Restore source code only"
    echo "  -d, --database-only  Restore database only"
    echo "  -c, --complete       Complete restoration (source + database)"
    echo "  -v, --validate       Validate backup integrity"
    echo "  -h, --help           Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --list"
    echo "  $0 --source-only /home/grand-as/backups/sama_etat_complete_backup_20250731_075319.tar.gz"
    echo "  $0 --complete /home/grand-as/backups/sama_etat_backup_20250731_075319 sama_etat_db"
    echo "  $0 --validate /home/grand-as/backups/sama_etat_complete_backup_20250731_075319.tar.gz"
    echo ""
    echo "⚠️  IMPORTANT:"
    echo "- Always test restoration in development environment first"
    echo "- Make sure you have current backups before restoration"
    echo "- Stop Odoo service manually if automatic restart fails"
    echo ""
}

# Main script logic
main() {
    case "$1" in
        -l|--list)
            show_available_backups
            ;;
        -s|--source-only)
            if [ -z "$2" ]; then
                log_error "Backup path required for source restoration"
                show_help
                return 1
            fi
            restore_source_only "$2"
            log "Don't forget to restart Odoo: sudo systemctl restart odoo"
            ;;
        -d|--database-only)
            if [ -z "$2" ]; then
                log_error "Backup path required for database restoration"
                show_help
                return 1
            fi
            restore_database "$2" "${3:-sama_etat_db}"
            ;;
        -c|--complete)
            if [ -z "$2" ]; then
                log_error "Backup path required for complete restoration"
                show_help
                return 1
            fi
            restore_complete "$2" "${3:-sama_etat_db}"
            ;;
        -v|--validate)
            if [ -z "$2" ]; then
                log_error "Backup path required for validation"
                show_help
                return 1
            fi
            validate_backup "$2"
            ;;
        -h|--help|"")
            show_help
            ;;
        *)
            log_error "Unknown option: $1"
            show_help
            return 1
            ;;
    esac
}

# Pre-flight checks
if [ "$(whoami)" != "grand-as" ]; then
    log_warning "Running as $(whoami), expected grand-as. Some operations may fail."
fi

# Check for required tools
for tool in tar psql createdb dropdb; do
    if ! command -v "$tool" &> /dev/null; then
        log_error "Required tool '$tool' is not installed"
        exit 1
    fi
done

# Run main function
main "$@"

# Exit with appropriate code
exit $?
