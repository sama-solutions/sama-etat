#!/bin/bash

# Vérification des logs d'installation

echo "🔍 SAMA SYNDICAT - VÉRIFICATION DES LOGS"
echo "========================================"

# Chercher les logs d'installation
LOG_FILES=(
    "/tmp/sama_syndicat_install.log"
    "/tmp/sama_install_simple.log"
    "/tmp/sama_install_bg.log"
)

echo "📄 Recherche des logs d'installation..."

for log_file in "${LOG_FILES[@]}"; do
    if [ -f "$log_file" ]; then
        echo ""
        echo "📄 LOG TROUVÉ: $log_file"
        echo "$(ls -lh $log_file)"
        echo ""
        
        # Analyser les erreurs
        echo "❌ ERREURS:"
        grep -i "error\|critical\|failed\|exception" "$log_file" | head -5
        
        echo ""
        echo "⚠️  AVERTISSEMENTS:"
        grep -i "warning" "$log_file" | head -3
        
        echo ""
        echo "📊 STATISTIQUES:"
        echo "   Lignes totales: $(wc -l < $log_file)"
        echo "   Erreurs: $(grep -ci "error\|critical\|failed" $log_file)"
        echo "   Avertissements: $(grep -ci "warning" $log_file)"
        
        echo ""
        echo "📄 DERNIÈRES LIGNES:"
        tail -10 "$log_file"
        
        echo ""
        echo "=" * 50
    fi
done

# Vérifier les processus Odoo en cours
echo ""
echo "🔍 PROCESSUS ODOO EN COURS:"
echo "=========================="
ps aux | grep odoo | grep -v grep

# Vérifier les bases de données sama_syndicat
echo ""
echo "🗄️  BASES DE DONNÉES SAMA_SYNDICAT:"
echo "=================================="
psql -U odoo -lqt | grep sama_syndicat

# Vérifier les ports utilisés
echo ""
echo "🌐 PORTS UTILISÉS:"
echo "================="
netstat -tlnp 2>/dev/null | grep :80 | head -5