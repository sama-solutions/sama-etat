#!/bin/bash

# Test de syntaxe rapide pour Sama Jokoo
# ======================================

echo "🔍 Test de syntaxe Sama Jokoo"
echo "=============================="

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

errors=0

echo -e "${BLUE}1. Test de syntaxe Python...${NC}"
find . -name "*.py" -type f | while read file; do
    if ! python3 -m py_compile "$file" 2>/dev/null; then
        echo -e "${RED}❌ Erreur dans: $file${NC}"
        errors=$((errors + 1))
    fi
done

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Syntaxe Python OK${NC}"
else
    echo -e "${RED}❌ Erreurs de syntaxe Python${NC}"
fi

echo -e "${BLUE}2. Test de syntaxe XML...${NC}"
find . -name "*.xml" -type f | while read file; do
    if ! xmllint --noout "$file" 2>/dev/null; then
        echo -e "${RED}❌ Erreur XML dans: $file${NC}"
        errors=$((errors + 1))
    fi
done

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Syntaxe XML OK${NC}"
else
    echo -e "${RED}❌ Erreurs de syntaxe XML${NC}"
fi

echo -e "${BLUE}3. Test du manifest...${NC}"
if python3 -c "exec(open('__manifest__.py').read())" 2>/dev/null; then
    echo -e "${GREEN}✅ Manifest OK${NC}"
else
    echo -e "${RED}❌ Erreur dans le manifest${NC}"
    errors=$((errors + 1))
fi

echo -e "${BLUE}4. Vérification des dépendances interdites...${NC}"
if grep -q "account" __manifest__.py; then
    echo -e "${RED}❌ Dépendance interdite 'account' trouvée${NC}"
    errors=$((errors + 1))
else
    echo -e "${GREEN}✅ Pas de dépendances interdites${NC}"
fi

echo -e "${BLUE}5. Vérification de la structure...${NC}"
required_files=(
    "models/__init__.py"
    "models/social_post.py"
    "controllers/__init__.py"
    "controllers/api_auth.py"
    "security/social_security.xml"
    "security/ir.model.access.csv"
    "views/social_post_views.xml"
)

missing=0
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}❌ Fichier manquant: $file${NC}"
        missing=$((missing + 1))
    fi
done

if [ $missing -eq 0 ]; then
    echo -e "${GREEN}✅ Structure complète${NC}"
else
    echo -e "${RED}❌ $missing fichiers manquants${NC}"
    errors=$((errors + missing))
fi

echo ""
if [ $errors -eq 0 ]; then
    echo -e "${GREEN}🎉 TOUS LES TESTS PASSÉS !${NC}"
    echo -e "${GREEN}Le module Sama Jokoo est prêt pour l'installation.${NC}"
    exit 0
else
    echo -e "${RED}❌ $errors erreurs détectées${NC}"
    echo -e "${RED}Corrigez les erreurs avant de continuer.${NC}"
    exit 1
fi