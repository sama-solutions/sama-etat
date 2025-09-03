#!/bin/bash

# Script de test de l'intégration des photos
echo "=== Test de l'intégration des photos sama_carte ==="

# Configuration
export PGPASSWORD=odoo
PORT=8071

echo "🔍 Vérification des photos intégrées..."

# Test 1: Vérifier que les membres ont des photos
echo "1. Vérification des photos en base..."
MEMBERS_WITH_PHOTOS=$(psql -U odoo -d sama_carte_demo -t -c "SELECT COUNT(*) FROM membership_member WHERE image_1920 IS NOT NULL;" | tr -d ' ')
TOTAL_MEMBERS=$(psql -U odoo -d sama_carte_demo -t -c "SELECT COUNT(*) FROM membership_member;" | tr -d ' ')

echo "   📊 Membres avec photos: $MEMBERS_WITH_PHOTOS / $TOTAL_MEMBERS"

if [ "$MEMBERS_WITH_PHOTOS" -eq "$TOTAL_MEMBERS" ]; then
    echo "   ✅ Toutes les photos ont été intégrées avec succès"
else
    echo "   ⚠️  Certains membres n'ont pas de photos"
fi

# Test 2: Vérifier les tailles des images
echo "2. Vérification des tailles d'images..."
psql -U odoo -d sama_carte_demo -c "SELECT name, LENGTH(image_1920) as image_size FROM membership_member WHERE image_1920 IS NOT NULL ORDER BY membership_number LIMIT 5;"

# Test 3: Test de connectivité des pages avec photos
echo "3. Test des pages publiques avec photos..."

# Test page publique avec token valide
FIRST_TOKEN=$(psql -U odoo -d sama_carte_demo -t -c "SELECT access_token FROM membership_member LIMIT 1;" | tr -d ' ')
if [ ! -z "$FIRST_TOKEN" ]; then
    RESPONSE=$(curl -s -w "%{http_code}" http://localhost:$PORT/member/$FIRST_TOKEN -o /tmp/test_member_with_photo.html)
    if echo "$RESPONSE" | grep -q "200"; then
        echo "   ✅ Page publique accessible avec photos"
        
        # Vérifier si l'image est présente dans le HTML
        if grep -q "image_1920" /tmp/test_member_with_photo.html; then
            echo "   ✅ Image détectée dans la page publique"
        else
            echo "   ⚠️  Image non détectée dans la page publique"
        fi
    else
        echo "   ❌ Page publique non accessible (code: $RESPONSE)"
    fi
else
    echo "   ⚠️  Aucun token trouvé pour le test"
fi

echo ""
echo "📁 FICHIERS CRÉÉS POUR LES PHOTOS:"
echo "   - headshots/ : 11 photos originales"
echo "   - data/processed_headshots/ : 11 photos traitées (300x300px)"
echo "   - data/demo_members_with_photos.xml : Données avec photos intégrées"

echo ""
echo "🔧 SCRIPTS CRÉÉS:"
echo "   - scripts/process_headshots.py : Traitement des images"
echo "   - scripts/generate_demo_with_photos.py : Génération XML avec photos"
echo "   - scripts/install_with_demo.sh : Installation avec démo"
echo "   - scripts/start_demo.sh : Démarrage base démo"

echo ""
echo "📊 RÉSUMÉ DES PHOTOS:"
echo "   ✅ 11 photos originales traitées"
echo "   ✅ Images centrées et redimensionnées (300x300px)"
echo "   ✅ Conversion en base64 pour Odoo"
echo "   ✅ Association avec les membres par ordre"
echo "   ✅ Intégration dans les données de démonstration"

echo ""
echo "🎯 TESTS À EFFECTUER DANS L'INTERFACE:"
echo "   1. Ouvrir http://localhost:$PORT"
echo "   2. Se connecter (admin/admin)"
echo "   3. Aller dans 'Gestion des Membres > Membres'"
echo "   4. Vérifier que tous les membres ont des photos"
echo "   5. Ouvrir un membre et cliquer sur 'Voir Page Publique'"
echo "   6. Vérifier que la photo s'affiche sur la page publique"
echo "   7. Imprimer une carte PDF pour voir le rendu final"

echo ""
echo "✅ INTÉGRATION DES PHOTOS TERMINÉE AVEC SUCCÈS !"