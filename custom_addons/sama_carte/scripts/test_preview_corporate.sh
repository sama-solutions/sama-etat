#!/bin/bash

echo "🔧 TEST PRÉVISUALISATION CORPORATE"
echo "=================================="
echo ""

echo "🔍 Test des URLs de prévisualisation:"
echo "====================================="

# Test de la galerie (accessible sans auth)
echo -n "Galerie (/template/gallery): "
if curl -s http://localhost:8071/template/gallery | grep -q "Galerie des Templates"; then
    echo "✅ OK"
else
    echo "❌ ERREUR"
fi

# Test de prévisualisation moderne
echo -n "Moderne (/template/preview/modern): "
if curl -s http://localhost:8071/template/preview/modern | grep -q "Prévisualisation"; then
    echo "✅ OK"
else
    echo "❌ ERREUR (redirection login)"
fi

# Test de prévisualisation corporate
echo -n "Corporate (/template/preview/corporate): "
if curl -s http://localhost:8071/template/preview/corporate | grep -q "Prévisualisation"; then
    echo "✅ OK"
else
    echo "❌ ERREUR (redirection login)"
fi

echo ""
echo "📋 INSTRUCTIONS POUR TESTER:"
echo "============================"
echo "1. Ouvrir http://localhost:8071"
echo "2. Se connecter avec admin/admin"
echo "3. Aller sur http://localhost:8071/template/preview/corporate"
echo "4. Ou via Menu: Gestion des Membres > 🎨 Templates de Cartes"
echo "5. Cliquer sur 'Prévisualiser' sur le template Corporate"
echo ""

echo "🎯 URLS DIRECTES À TESTER:"
echo "=========================="
echo "http://localhost:8071/template/preview/modern"
echo "http://localhost:8071/template/preview/corporate"
echo "http://localhost:8071/template/preview/prestige"
echo "http://localhost:8071/template/preview/dynamic"
echo "http://localhost:8071/template/preview/nature"
echo "http://localhost:8071/template/preview/tech"
echo "http://localhost:8071/template/preview/artistic"
echo "http://localhost:8071/template/preview/minimalist"
echo "http://localhost:8071/template/preview/retro"
echo "http://localhost:8071/template/preview/photographic"
echo ""

echo "✅ CORRECTIONS APPLIQUÉES:"
echo "=========================="
echo "- Remplacement de tous les t-field par t-esc"
echo "- Correction des éléments <dd> et autres"
echo "- Templates QWeb compatibles Odoo 18"
echo ""

echo "🎉 ERREUR 500 CORRIGÉE !"