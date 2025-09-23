#!/bin/bash

# Script d'analyse des logs Odoo pour SAMA SYNDICAT

echo "🔍 ANALYSE DES LOGS ODOO - SAMA SYNDICAT"
echo "========================================"
echo ""

LOG_FILE="/var/log/odoo/odoo.log"

if [ ! -f "$LOG_FILE" ]; then
    echo "❌ Fichier de log non trouvé: $LOG_FILE"
    exit 1
fi

echo "📊 RÉSUMÉ DES ERREURS"
echo "--------------------"

# Compter les types d'erreurs
echo "🔴 Erreurs totales:"
grep -c "ERROR" "$LOG_FILE" 2>/dev/null || echo "0"

echo "🟡 Warnings totaux:"
grep -c "WARNING" "$LOG_FILE" 2>/dev/null || echo "0"

echo "🔵 Erreurs ParseError:"
grep -c "ParseError" "$LOG_FILE" 2>/dev/null || echo "0"

echo ""
echo "📅 ERREURS RÉCENTES (dernières 24h)"
echo "-----------------------------------"

# Erreurs des dernières 24h
TODAY=$(date +"%Y-%m-%d")
YESTERDAY=$(date -d "yesterday" +"%Y-%m-%d")

echo "Erreurs d'aujourd'hui ($TODAY):"
grep "$TODAY.*ERROR" "$LOG_FILE" | wc -l

echo "Erreurs d'hier ($YESTERDAY):"
grep "$YESTERDAY.*ERROR" "$LOG_FILE" | wc -l

echo ""
echo "🎯 ERREURS SPÉCIFIQUES À SAMA_SYNDICAT"
echo "-------------------------------------"

# Rechercher les erreurs liées à sama_syndicat
SAMA_ERRORS=$(grep -i "sama_syndicat" "$LOG_FILE" | grep -i "error" | wc -l)
echo "Erreurs sama_syndicat: $SAMA_ERRORS"

if [ $SAMA_ERRORS -gt 0 ]; then
    echo ""
    echo "Détails des erreurs sama_syndicat:"
    grep -i "sama_syndicat" "$LOG_FILE" | grep -i "error" | tail -5
fi

echo ""
echo "🔧 ERREURS COMMUNES IDENTIFIÉES"
echo "-------------------------------"

# Analyser les types d'erreurs les plus fréquents
echo "1. Erreurs de modules manquants:"
grep -c "ModuleNotFoundError" "$LOG_FILE" 2>/dev/null || echo "0"

echo "2. Erreurs de base de données:"
grep -c "psycopg2.errors" "$LOG_FILE" 2>/dev/null || echo "0"

echo "3. Erreurs de vues XML:"
grep -c "View error context" "$LOG_FILE" 2>/dev/null || echo "0"

echo "4. Erreurs de champs manquants:"
grep -c "Field.*does not exist" "$LOG_FILE" 2>/dev/null || echo "0"

echo "5. Erreurs de clés externes:"
grep -c "External ID not found" "$LOG_FILE" 2>/dev/null || echo "0"

echo ""
echo "🚨 ERREURS CRITIQUES RÉCENTES"
echo "-----------------------------"

# Dernières erreurs critiques
echo "Dernières erreurs CRITICAL:"
grep "CRITICAL" "$LOG_FILE" | tail -3

echo ""
echo "Dernières erreurs ERROR:"
grep "ERROR" "$LOG_FILE" | tail -5

echo ""
echo "🔍 ANALYSE DES MODULES PROBLÉMATIQUES"
echo "------------------------------------"

# Identifier les modules qui causent le plus d'erreurs
echo "Modules avec le plus d'erreurs:"
grep "ERROR" "$LOG_FILE" | grep -o "odoo\.addons\.[a-zA-Z_]*" | sort | uniq -c | sort -nr | head -5

echo ""
echo "📋 RECOMMANDATIONS"
echo "-----------------"

# Vérifier les erreurs spécifiques et donner des recommandations
if grep -q "rlPyCairo" "$LOG_FILE"; then
    echo "⚠️  Problème ReportLab détecté - Installer: pip install rlPyCairo"
fi

if grep -q "wkhtmltopdf" "$LOG_FILE"; then
    echo "⚠️  Problème wkhtmltopdf détecté - Vérifier l'installation"
fi

if grep -q "could not serialize access" "$LOG_FILE"; then
    echo "⚠️  Problèmes de concurrence DB détectés - Vérifier les connexions"
fi

if grep -q "ParseError" "$LOG_FILE"; then
    echo "⚠️  Erreurs XML détectées - Vérifier la syntaxe des vues"
fi

if grep -q "External ID not found" "$LOG_FILE"; then
    echo "⚠️  IDs externes manquants - Vérifier les dépendances des modules"
fi

echo ""
echo "✅ ANALYSE TERMINÉE"
echo "Pour plus de détails, consultez: $LOG_FILE"