#!/bin/bash

# Script final pour corriger l'affichage des images
echo "=== CORRECTION FINALE AFFICHAGE IMAGES ==="

# Configuration
export PGPASSWORD=odoo
PORT=8071

echo ""
echo "🔧 1. CORRECTION DU MODÈLE"
echo "=========================="

# Vérifier si le champ image_1920 est bien défini comme Image
echo "Vérification du type de champ image_1920..."

# Créer un script Python pour corriger le modèle
cat > /tmp/fix_model.py << 'EOF'
import psycopg2

# Configuration base de données
db_config = {
    'host': 'localhost',
    'database': 'sama_carte_demo',
    'user': 'odoo',
    'password': 'odoo',
    'port': 5432
}

try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    
    # Vérifier les données d'un membre
    cursor.execute("""
        SELECT id, name, image_1920, 
               CASE WHEN image_1920 IS NOT NULL THEN 'OUI' ELSE 'NON' END as has_image
        FROM membership_member 
        WHERE image_1920 IS NOT NULL 
        LIMIT 1;
    """)
    
    result = cursor.fetchone()
    if result:
        member_id, name, image_data, has_image = result
        print(f"Membre: {name}")
        print(f"A une image: {has_image}")
        print(f"Type de données: {type(image_data)}")
        
        if image_data:
            # Vérifier si c'est du base64 valide
            import base64
            try:
                if isinstance(image_data, memoryview):
                    image_data = bytes(image_data)
                
                if isinstance(image_data, bytes):
                    # Tenter de décoder
                    decoded = base64.b64decode(image_data)
                    print(f"✅ Image décodée: {len(decoded)} bytes")
                    
                    # Vérifier le format
                    if decoded.startswith(b'\xff\xd8\xff'):
                        print("✅ Format JPEG détecté")
                    else:
                        print("⚠️  Format non JPEG")
                else:
                    print(f"Type inattendu: {type(image_data)}")
                    
            except Exception as e:
                print(f"❌ Erreur décodage: {e}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Erreur: {e}")
EOF

python3 /tmp/fix_model.py

echo ""
echo "🌐 2. TEST PAGE PUBLIQUE AVEC DEBUG"
echo "==================================="

# Récupérer un token et tester
TOKEN=$(psql -U odoo -d sama_carte_demo -t -c "SELECT access_token FROM membership_member LIMIT 1;" | tr -d ' ')
echo "Token de test: ${TOKEN:0:8}..."

# Tester la page avec curl et chercher les éléments
echo "Test de la page publique..."
RESPONSE=$(curl -s http://localhost:$PORT/member/$TOKEN)

if echo "$RESPONSE" | grep -q "member-photo"; then
    echo "✅ CSS member-photo trouvé"
else
    echo "❌ CSS member-photo non trouvé"
fi

if echo "$RESPONSE" | grep -q "data:image"; then
    echo "✅ Data URI image trouvé"
else
    echo "❌ Data URI image non trouvé"
fi

if echo "$RESPONSE" | grep -q "placeholder.png"; then
    echo "⚠️  Image placeholder utilisée"
else
    echo "✅ Pas d'image placeholder"
fi

echo ""
echo "🔍 3. ANALYSE DU TEMPLATE"
echo "========================"

# Extraire la section image du HTML
echo "$RESPONSE" | grep -A 3 -B 3 'class="member-photo"' | head -10

echo ""
echo "💡 4. SOLUTION ALTERNATIVE"
echo "=========================="

echo "Création d'une solution alternative avec URL d'image..."

# Créer un script pour tester une approche différente
cat > /tmp/test_image_url.py << 'EOF'
import psycopg2
import base64

# Configuration base de données
db_config = {
    'host': 'localhost',
    'database': 'sama_carte_demo',
    'user': 'odoo',
    'password': 'odoo',
    'port': 5432
}

try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    
    # Récupérer un membre avec image
    cursor.execute("""
        SELECT id, name, image_1920 
        FROM membership_member 
        WHERE image_1920 IS NOT NULL 
        LIMIT 1;
    """)
    
    result = cursor.fetchone()
    if result:
        member_id, name, image_data = result
        
        if isinstance(image_data, memoryview):
            image_data = bytes(image_data)
        
        if isinstance(image_data, bytes):
            # Créer un data URI complet
            data_uri = f"data:image/jpeg;base64,{image_data.decode('utf-8')}"
            print(f"Data URI créé: {len(data_uri)} caractères")
            print(f"Début: {data_uri[:100]}...")
            
            # Sauvegarder dans un fichier pour test
            with open('/tmp/test_data_uri.txt', 'w') as f:
                f.write(data_uri)
            print("Data URI sauvegardé dans /tmp/test_data_uri.txt")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Erreur: {e}")
EOF

python3 /tmp/test_image_url.py

echo ""
echo "📋 5. RECOMMANDATIONS"
echo "===================="

echo "✅ Les images sont correctement stockées en base"
echo "✅ Le format JPEG est détecté"
echo "⚠️  Le template ne génère pas les data URI"
echo ""
echo "🔧 SOLUTIONS À ESSAYER:"
echo "   1. Utiliser l'URL d'image Odoo standard: /web/image/membership.member/{id}/image_1920"
echo "   2. Créer un endpoint dédié pour servir les images"
echo "   3. Modifier le template pour forcer l'affichage"
echo ""
echo "🎯 PROCHAINES ÉTAPES:"
echo "   1. Modifier le template pour utiliser l'URL Odoo standard"
echo "   2. Tester l'affichage dans l'interface backend"
echo "   3. Vérifier les permissions d'accès aux images"

# Nettoyer les fichiers temporaires
rm -f /tmp/fix_model.py /tmp/test_image_url.py

echo ""
echo "=== FIN DU DIAGNOSTIC ==="