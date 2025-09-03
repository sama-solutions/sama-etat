#!/bin/bash

# Script de test des membres de démonstration
echo "=== Test des membres de démonstration ==="

# Configuration
export PGPASSWORD=odoo
PORT=8071

echo "🔍 Vérification des membres en base..."

# Récupérer les tokens d'accès des membres
echo "Récupération des tokens d'accès..."
TOKENS=$(psql -U odoo -d sama_carte_demo -t -c "SELECT name, access_token, expiration_date FROM membership_member ORDER BY membership_number LIMIT 5;")

echo "Membres trouvés:"
echo "$TOKENS"

echo ""
echo "🌐 Test des pages publiques..."

# Test de quelques pages publiques
echo "1. Test page membre non trouvé..."
RESPONSE=$(curl -s -w "%{http_code}" http://localhost:$PORT/member/token-inexistant -o /tmp/test_404.html)
if echo "$RESPONSE" | grep -q "200"; then
    if grep -q "Carte non trouvée" /tmp/test_404.html; then
        echo "   ✅ Page 'Membre non trouvé' fonctionne"
    else
        echo "   ❌ Contenu incorrect"
    fi
else
    echo "   ❌ Page non accessible (code: $RESPONSE)"
fi

# Test avec un vrai token
echo "2. Test avec un token valide..."
FIRST_TOKEN=$(psql -U odoo -d sama_carte_demo -t -c "SELECT access_token FROM membership_member LIMIT 1;" | tr -d ' ')
if [ ! -z "$FIRST_TOKEN" ]; then
    RESPONSE=$(curl -s -w "%{http_code}" http://localhost:$PORT/member/$FIRST_TOKEN -o /tmp/test_member.html)
    if echo "$RESPONSE" | grep -q "200"; then
        if grep -q "member-name\|Membre N°" /tmp/test_member.html; then
            echo "   ✅ Page membre valide fonctionne"
        else
            echo "   ⚠️  Page accessible mais contenu à vérifier"
        fi
    else
        echo "   ❌ Page membre non accessible (code: $RESPONSE)"
    fi
else
    echo "   ⚠️  Aucun token trouvé"
fi

echo ""
echo "📊 Statistiques des membres:"
echo "   Total membres: $(psql -U odoo -d sama_carte_demo -t -c "SELECT COUNT(*) FROM membership_member;" | tr -d ' ')"
echo "   Cartes valides: $(psql -U odoo -d sama_carte_demo -t -c "SELECT COUNT(*) FROM membership_member WHERE expiration_date >= CURRENT_DATE;" | tr -d ' ')"
echo "   Cartes expirées: $(psql -U odoo -d sama_carte_demo -t -c "SELECT COUNT(*) FROM membership_member WHERE expiration_date < CURRENT_DATE;" | tr -d ' ')"

echo ""
echo "🎯 Accès interface:"
echo "   URL: http://localhost:$PORT"
echo "   Login: admin / admin"
echo "   Menu: Gestion des Membres > Membres"

echo ""
echo "🔗 URLs de test des pages publiques:"
# Afficher quelques URLs de test
psql -U odoo -d sama_carte_demo -t -c "SELECT 'http://localhost:$PORT/member/' || access_token AS url FROM membership_member LIMIT 3;" | sed 's/^ */   /'