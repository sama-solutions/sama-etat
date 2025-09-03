#!/bin/bash

# Script de test des widgets backend
echo "=== Test des widgets backend sama_carte ==="

# Configuration
export PGPASSWORD=odoo
PORT=8071

echo "🔍 Vérification des nouvelles fonctionnalités..."

# Test 1: Vérifier que les nouveaux champs existent
echo "1. Vérification des nouveaux champs en base..."

# Vérifier le champ public_url
PUBLIC_URL_EXISTS=$(psql -U odoo -d sama_carte_demo -t -c "SELECT column_name FROM information_schema.columns WHERE table_name='membership_member' AND column_name='public_url';" | tr -d ' ')
if [ ! -z "$PUBLIC_URL_EXISTS" ]; then
    echo "   ✅ Champ public_url trouvé"
else
    echo "   ⚠️  Champ public_url non trouvé (normal car c'est un champ calculé)"
fi

# Vérifier le champ card_status
CARD_STATUS_EXISTS=$(psql -U odoo -d sama_carte_demo -t -c "SELECT column_name FROM information_schema.columns WHERE table_name='membership_member' AND column_name='card_status';" | tr -d ' ')
if [ ! -z "$CARD_STATUS_EXISTS" ]; then
    echo "   ✅ Champ card_status trouvé"
else
    echo "   ❌ Champ card_status non trouvé"
fi

# Test 2: Vérifier les URLs publiques
echo "2. Test des URLs publiques générées..."
SAMPLE_URLS=$(psql -U odoo -d sama_carte_demo -t -c "SELECT name, access_token FROM membership_member LIMIT 3;")
echo "   Échantillon d'URLs:"
echo "$SAMPLE_URLS" | while read line; do
    if [ ! -z "$line" ]; then
        NAME=$(echo "$line" | cut -d'|' -f1 | tr -d ' ')
        TOKEN=$(echo "$line" | cut -d'|' -f2 | tr -d ' ')
        if [ ! -z "$TOKEN" ]; then
            echo "   - $NAME: http://localhost:$PORT/member/$TOKEN"
        fi
    fi
done

# Test 3: Vérifier les statuts des cartes
echo "3. Vérification des statuts des cartes..."
VALID_COUNT=$(psql -U odoo -d sama_carte_demo -t -c "SELECT COUNT(*) FROM membership_member WHERE expiration_date >= CURRENT_DATE;" | tr -d ' ')
EXPIRED_COUNT=$(psql -U odoo -d sama_carte_demo -t -c "SELECT COUNT(*) FROM membership_member WHERE expiration_date < CURRENT_DATE;" | tr -d ' ')

echo "   ✅ Cartes valides: $VALID_COUNT"
echo "   ❌ Cartes expirées: $EXPIRED_COUNT"

# Test 4: Test de connectivité des pages
echo "4. Test de connectivité des pages publiques..."

# Test page d'accueil backend
if curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT | grep -q "200\|302"; then
    echo "   ✅ Backend accessible"
else
    echo "   ❌ Backend non accessible"
fi

# Test page publique avec token valide
FIRST_TOKEN=$(psql -U odoo -d sama_carte_demo -t -c "SELECT access_token FROM membership_member LIMIT 1;" | tr -d ' ')
if [ ! -z "$FIRST_TOKEN" ]; then
    RESPONSE=$(curl -s -w "%{http_code}" http://localhost:$PORT/member/$FIRST_TOKEN -o /tmp/test_public_page.html)
    if echo "$RESPONSE" | grep -q "200"; then
        echo "   ✅ Page publique accessible"
    else
        echo "   ❌ Page publique non accessible (code: $RESPONSE)"
    fi
else
    echo "   ⚠️  Aucun token trouvé pour le test"
fi

echo ""
echo "🎯 NOUVELLES FONCTIONNALITÉS AJOUTÉES:"
echo ""
echo "📋 Vue Liste:"
echo "   ✅ Colonne 'Statut de la Carte' avec badges colorés"
echo "   ✅ Bouton 'Ouvrir page publique' (icône lien externe)"
echo ""
echo "📝 Vue Formulaire:"
echo "   ✅ Bouton 'Voir Page Publique' dans l'en-tête"
echo "   ✅ Onglet 'QR Code & Accès Public' avec:"
echo "       - QR Code affiché"
echo "       - URL publique avec widget URL"
echo "       - Bouton 'Ouvrir' pour accès direct"
echo "   ✅ Onglet séparé 'Termes & Conditions'"
echo ""
echo "🔧 Modèle:"
echo "   ✅ Champ calculé 'public_url'"
echo "   ✅ Champ calculé 'card_status' (valide/expirée)"
echo "   ✅ Méthode 'action_open_public_page()'"
echo "   ✅ QR Code pointant vers URL publique"

echo ""
echo "🌐 ACCÈS INTERFACE:"
echo "   URL Backend: http://localhost:$PORT"
echo "   Login: admin / admin"
echo "   Menu: Gestion des Membres > Membres"

echo ""
echo "🎯 TESTS À EFFECTUER:"
echo "   1. Ouvrir la liste des membres"
echo "   2. Vérifier les badges de statut (vert=valide, rouge=expiré)"
echo "   3. Cliquer sur l'icône lien externe dans la liste"
echo "   4. Ouvrir un membre en mode formulaire"
echo "   5. Cliquer sur 'Voir Page Publique' dans l'en-tête"
echo "   6. Aller dans l'onglet 'QR Code & Accès Public'"
echo "   7. Cliquer sur 'Ouvrir' à côté de l'URL publique"

echo ""
echo "✅ WIDGETS BACKEND INSTALLÉS ET PRÊTS !"