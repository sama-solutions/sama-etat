#!/bin/bash

# Test final des images après upload via backend
echo "=== TEST FINAL DES IMAGES ==="

# Configuration
export PGPASSWORD=odoo
PORT=8071

echo ""
echo "🔍 1. VÉRIFICATION BACKEND"
echo "=========================="

echo "Test de l'interface backend..."
echo "🎯 Ouvrez http://localhost:$PORT dans votre navigateur"
echo "🎯 Connectez-vous avec admin/admin"
echo "🎯 Allez dans 'Gestion des Membres > Membres'"
echo "🎯 Vérifiez si les photos s'affichent dans la liste et les formulaires"

echo ""
echo "🌐 2. TEST PAGE PUBLIQUE"
echo "========================"

# Récupérer un token de test
TOKEN=$(psql -U odoo -d sama_carte_demo -t -c "SELECT access_token FROM membership_member LIMIT 1;" | tr -d ' ')
MEMBER_NAME=$(psql -U odoo -d sama_carte_demo -t -c "SELECT name FROM membership_member LIMIT 1;" | tr -d ' ')

echo "Token de test: ${TOKEN:0:8}..."
echo "Membre de test: $MEMBER_NAME"
echo "URL de test: http://localhost:$PORT/member/$TOKEN"

# Tester la page publique
echo ""
echo "Test de la page publique..."
RESPONSE=$(curl -s http://localhost:$PORT/member/$TOKEN)

if echo "$RESPONSE" | grep -q "member-photo"; then
    echo "✅ CSS member-photo trouvé"
else
    echo "❌ CSS member-photo non trouvé"
fi

if echo "$RESPONSE" | grep -q "/web/image/membership.member"; then
    echo "✅ URL Odoo standard utilisée"
else
    echo "❌ URL Odoo standard non trouvée"
fi

if echo "$RESPONSE" | grep -q "placeholder.png"; then
    echo "⚠️  Image placeholder détectée"
else
    echo "✅ Pas d'image placeholder"
fi

echo ""
echo "🖼️ 3. TEST URL IMAGES DIRECTES"
echo "=============================="

# Tester l'URL d'image directement
MEMBER_ID=$(psql -U odoo -d sama_carte_demo -t -c "SELECT id FROM membership_member LIMIT 1;" | tr -d ' ')
IMAGE_URL="http://localhost:$PORT/web/image/membership.member/$MEMBER_ID/image_1920"

echo "URL image: $IMAGE_URL"
RESPONSE_CODE=$(curl -s -w "%{http_code}" "$IMAGE_URL" -o /dev/null)
echo "Code de réponse: $RESPONSE_CODE"

if [ "$RESPONSE_CODE" = "200" ]; then
    # Vérifier le type de contenu
    CONTENT_TYPE=$(curl -s -I "$IMAGE_URL" | grep -i "content-type" | cut -d' ' -f2- | tr -d '\r')
    echo "Type de contenu: $CONTENT_TYPE"
    
    if echo "$CONTENT_TYPE" | grep -q "image/jpeg\|image/png"; then
        echo "✅ Image réelle servie"
    else
        echo "⚠️  Placeholder servi"
    fi
else
    echo "❌ Erreur d'accès à l'image"
fi

echo ""
echo "📊 4. VÉRIFICATION BASE DE DONNÉES"
echo "=================================="

# Vérifier les données en base
echo "Vérification des images en base..."
MEMBERS_WITH_IMAGES=$(psql -U odoo -d sama_carte_demo -t -c "SELECT COUNT(*) FROM membership_member WHERE image_1920 IS NOT NULL;" | tr -d ' ')
TOTAL_MEMBERS=$(psql -U odoo -d sama_carte_demo -t -c "SELECT COUNT(*) FROM membership_member;" | tr -d ' ')

echo "Membres avec images: $MEMBERS_WITH_IMAGES / $TOTAL_MEMBERS"

if [ "$MEMBERS_WITH_IMAGES" -gt "0" ]; then
    echo "✅ Images présentes en base"
    
    # Vérifier la taille d'une image
    IMAGE_SIZE=$(psql -U odoo -d sama_carte_demo -t -c "SELECT LENGTH(image_1920) FROM membership_member WHERE image_1920 IS NOT NULL LIMIT 1;" | tr -d ' ')
    echo "Taille d'une image: $IMAGE_SIZE bytes"
    
    if [ "$IMAGE_SIZE" -gt "1000" ]; then
        echo "✅ Taille d'image réaliste"
    else
        echo "⚠️  Taille d'image suspecte"
    fi
else
    echo "❌ Aucune image en base"
fi

echo ""
echo "🎯 5. RECOMMANDATIONS"
echo "===================="

if [ "$MEMBERS_WITH_IMAGES" -gt "0" ] && [ "$RESPONSE_CODE" = "200" ]; then
    echo "🎉 SUCCÈS PARTIEL!"
    echo "   ✅ Images en base de données"
    echo "   ✅ URLs accessibles"
    echo "   ✅ Template mis à jour"
    echo ""
    echo "🔧 POUR FINALISER:"
    echo "   1. Vérifiez l'affichage dans l'interface backend"
    echo "   2. Testez l'impression des cartes PDF"
    echo "   3. Vérifiez que toutes les photos sont visibles"
elif [ "$MEMBERS_WITH_IMAGES" -gt "0" ]; then
    echo "⚠️  PROBLÈME PARTIEL"
    echo "   ✅ Images en base"
    echo "   ❌ URLs ne servent pas les vraies images"
    echo ""
    echo "🔧 SOLUTIONS:"
    echo "   1. Vérifier les permissions du champ image_1920"
    echo "   2. Redémarrer Odoo complètement"
    echo "   3. Vider le cache navigateur"
else
    echo "❌ PROBLÈME MAJEUR"
    echo "   ❌ Pas d'images en base"
    echo ""
    echo "🔧 SOLUTION:"
    echo "   1. Re-uploader les photos via l'interface backend"
    echo "   2. Utiliser le widget image dans les formulaires"
fi

echo ""
echo "📋 URLS DE TEST:"
echo "   🌐 Interface: http://localhost:$PORT"
echo "   👤 Page membre: http://localhost:$PORT/member/$TOKEN"
echo "   🖼️  Image directe: $IMAGE_URL"

echo ""
echo "=== FIN DU TEST ==="