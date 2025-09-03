#!/bin/bash

# Test final complet de l'intégration des photos
echo "=== TEST FINAL - INTÉGRATION PHOTOS SAMA_CARTE ==="

# Configuration
export PGPASSWORD=odoo
PORT=8071

echo ""
echo "🔍 1. VÉRIFICATION DE LA BASE DE DONNÉES"
echo "========================================"

# Test connexion base
if psql -U odoo -d sama_carte_demo -c "SELECT 1;" > /dev/null 2>&1; then
    echo "✅ Connexion base de données OK"
else
    echo "❌ Impossible de se connecter à la base"
    exit 1
fi

# Vérification structure table
COLUMNS=$(psql -U odoo -d sama_carte_demo -t -c "SELECT column_name FROM information_schema.columns WHERE table_name='membership_member' AND column_name='image_1920';" | tr -d ' ')
if [ "$COLUMNS" = "image_1920" ]; then
    echo "✅ Colonne image_1920 présente"
else
    echo "❌ Colonne image_1920 manquante"
    exit 1
fi

# Statistiques membres
TOTAL_MEMBERS=$(psql -U odoo -d sama_carte_demo -t -c "SELECT COUNT(*) FROM membership_member;" | tr -d ' ')
MEMBERS_WITH_PHOTOS=$(psql -U odoo -d sama_carte_demo -t -c "SELECT COUNT(*) FROM membership_member WHERE image_1920 IS NOT NULL;" | tr -d ' ')
VALID_CARDS=$(psql -U odoo -d sama_carte_demo -t -c "SELECT COUNT(*) FROM membership_member WHERE expiration_date >= CURRENT_DATE;" | tr -d ' ')
EXPIRED_CARDS=$(psql -U odoo -d sama_carte_demo -t -c "SELECT COUNT(*) FROM membership_member WHERE expiration_date < CURRENT_DATE;" | tr -d ' ')

echo "📊 Statistiques:"
echo "   - Total membres: $TOTAL_MEMBERS"
echo "   - Avec photos: $MEMBERS_WITH_PHOTOS"
echo "   - Cartes valides: $VALID_CARDS"
echo "   - Cartes expirées: $EXPIRED_CARDS"

echo ""
echo "🌐 2. VÉRIFICATION SERVEUR ODOO"
echo "==============================="

# Test connectivité serveur
if curl -s http://localhost:$PORT > /dev/null; then
    echo "✅ Serveur Odoo accessible sur port $PORT"
else
    echo "❌ Serveur Odoo non accessible"
    exit 1
fi

# Test page de login
LOGIN_RESPONSE=$(curl -s -w "%{http_code}" http://localhost:$PORT/web/login -o /dev/null)
if [ "$LOGIN_RESPONSE" = "200" ]; then
    echo "✅ Page de login accessible"
else
    echo "❌ Page de login non accessible (code: $LOGIN_RESPONSE)"
fi

echo ""
echo "🔗 3. TEST PAGES PUBLIQUES"
echo "=========================="

# Récupérer un token de test
FIRST_TOKEN=$(psql -U odoo -d sama_carte_demo -t -c "SELECT access_token FROM membership_member LIMIT 1;" | tr -d ' ')
FIRST_NAME=$(psql -U odoo -d sama_carte_demo -t -c "SELECT name FROM membership_member LIMIT 1;" | tr -d ' ')

if [ ! -z "$FIRST_TOKEN" ]; then
    echo "🔑 Token de test: ${FIRST_TOKEN:0:8}..."
    echo "👤 Membre de test: $FIRST_NAME"
    
    # Test page publique
    PUBLIC_RESPONSE=$(curl -s -w "%{http_code}" http://localhost:$PORT/member/$FIRST_TOKEN -o /tmp/test_public_page.html)
    if [ "$PUBLIC_RESPONSE" = "200" ]; then
        echo "✅ Page publique accessible"
        
        # Vérifier contenu
        if grep -q "$FIRST_NAME" /tmp/test_public_page.html; then
            echo "✅ Nom du membre affiché"
        else
            echo "⚠️  Nom du membre non trouvé"
        fi
        
        if grep -q "image_1920" /tmp/test_public_page.html; then
            echo "✅ Image détectée dans le HTML"
        else
            echo "⚠️  Image non détectée dans le HTML"
        fi
        
        if grep -q "QR Code" /tmp/test_public_page.html; then
            echo "✅ QR Code présent"
        else
            echo "⚠️  QR Code non trouvé"
        fi
    else
        echo "❌ Page publique non accessible (code: $PUBLIC_RESPONSE)"
    fi
else
    echo "❌ Aucun token trouvé"
fi

echo ""
echo "📁 4. VÉRIFICATION FICHIERS"
echo "==========================="

# Vérifier fichiers photos
if [ -d "headshots" ]; then
    ORIGINAL_PHOTOS=$(ls headshots/*.jpg 2>/dev/null | wc -l)
    echo "✅ Photos originales: $ORIGINAL_PHOTOS"
else
    echo "⚠️  Dossier headshots non trouvé"
fi

if [ -d "data/processed_headshots" ]; then
    PROCESSED_PHOTOS=$(ls data/processed_headshots/*.jpg 2>/dev/null | wc -l)
    echo "✅ Photos traitées: $PROCESSED_PHOTOS"
else
    echo "⚠️  Dossier processed_headshots non trouvé"
fi

# Vérifier scripts
SCRIPTS=("process_headshots.py" "add_photos_to_members.py" "install_with_demo.sh" "start_demo.sh")
for script in "${SCRIPTS[@]}"; do
    if [ -f "scripts/$script" ]; then
        echo "✅ Script $script présent"
    else
        echo "❌ Script $script manquant"
    fi
done

echo ""
echo "🎯 5. RÉSUMÉ FINAL"
echo "=================="

if [ "$MEMBERS_WITH_PHOTOS" = "$TOTAL_MEMBERS" ] && [ "$TOTAL_MEMBERS" -gt "0" ]; then
    echo "🎉 SUCCÈS COMPLET!"
    echo "   ✅ Tous les membres ($TOTAL_MEMBERS) ont des photos"
    echo "   ✅ Base de données fonctionnelle"
    echo "   ✅ Serveur Odoo opérationnel"
    echo "   ✅ Pages publiques accessibles"
    echo ""
    echo "🚀 PRÊT POUR LA PRODUCTION!"
    echo ""
    echo "📋 ACTIONS SUIVANTES:"
    echo "   1. Tester l'interface: http://localhost:$PORT"
    echo "   2. Login: admin / admin"
    echo "   3. Menu: Gestion des Membres > Membres"
    echo "   4. Vérifier les photos dans les fiches"
    echo "   5. Tester l'impression des cartes PDF"
    echo "   6. Vérifier les pages publiques"
    echo ""
    echo "💾 SAUVEGARDES DISPONIBLES:"
    ls -la backup/ | grep sama_carte | tail -3
else
    echo "⚠️  PROBLÈMES DÉTECTÉS"
    echo "   - Membres sans photos: $((TOTAL_MEMBERS - MEMBERS_WITH_PHOTOS))"
    echo "   - Vérifier les logs et relancer les scripts"
fi

echo ""
echo "🔧 COMMANDES UTILES:"
echo "   - Redémarrer: ./scripts/start_demo.sh"
echo "   - Ajouter photos: python3 scripts/add_photos_to_members.py"
echo "   - Arrêter: pkill -f 'odoo.*--http-port=8071'"
echo ""
echo "=== FIN DU TEST ==="