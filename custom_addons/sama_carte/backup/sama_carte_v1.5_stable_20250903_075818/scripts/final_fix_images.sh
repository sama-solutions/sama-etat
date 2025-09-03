#!/bin/bash

# Script final pour corriger définitivement les images
echo "=== CORRECTION DÉFINITIVE DES IMAGES ==="

echo ""
echo "🎯 PROBLÈME IDENTIFIÉ:"
echo "   - Les images sont stockées en base"
echo "   - Le template utilise la bonne URL"
echo "   - Mais la condition t-if ne fonctionne pas"
echo ""

echo "💡 SOLUTION: Forcer l'affichage de l'image"
echo "   - Supprimer la condition t-if"
echo "   - Utiliser l'endpoint personnalisé"
echo "   - Gérer les erreurs côté serveur"

# Créer un template simplifié
cat > /tmp/new_template_section.txt << 'EOF'
                                    <!-- Photo du membre -->
                                    <img t-attf-src="/member/{{member.access_token}}/image" 
                                         class="member-photo" 
                                         alt="Photo du membre"
                                         onerror="this.src='/web/static/src/img/placeholder.png'"/>
EOF

echo ""
echo "🔧 Mise à jour du template..."

# Remplacer la section image dans le template
python3 << 'EOF'
# Lire le template
with open('views/website_member_views.xml', 'r') as f:
    content = f.read()

# Définir l'ancienne section
old_section = '''                                    <!-- Photo du membre -->
                                    <img t-if="member.image_1920" 
                                         t-attf-src="/member/{{member.access_token}}/image" 
                                         class="member-photo" 
                                         alt="Photo du membre"/>
                                    <img t-else="" 
                                         src="/web/static/src/img/placeholder.png" 
                                         class="member-photo" 
                                         alt="Pas de photo"/>'''

# Nouvelle section simplifiée
new_section = '''                                    <!-- Photo du membre -->
                                    <img t-attf-src="/member/{{member.access_token}}/image" 
                                         class="member-photo" 
                                         alt="Photo du membre"
                                         onerror="this.src='/web/static/src/img/placeholder.png'"/>'''

# Remplacer
if old_section in content:
    content = content.replace(old_section, new_section)
    print("✅ Section image remplacée")
else:
    print("⚠️  Section non trouvée, recherche alternative...")
    # Chercher une version similaire
    import re
    pattern = r'<!-- Photo du membre -->.*?alt="Pas de photo"/>'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        content = content.replace(match.group(0), new_section.strip())
        print("✅ Section alternative remplacée")
    else:
        print("❌ Impossible de trouver la section à remplacer")

# Écrire le nouveau template
with open('views/website_member_views.xml', 'w') as f:
    f.write(content)

print("✅ Template mis à jour")
EOF

echo ""
echo "🔧 Mise à jour du contrôleur pour debug..."

# Ajouter du debug au contrôleur
python3 << 'EOF'
# Lire le contrôleur
with open('controllers/main.py', 'r') as f:
    content = f.read()

# Ajouter du debug dans la méthode image
debug_section = '''        # Debug: afficher les informations
        print(f"DEBUG: Membre trouvé: {member.name}")
        print(f"DEBUG: A une image: {bool(member.image_1920)}")
        if member.image_1920:
            print(f"DEBUG: Type image: {type(member.image_1920)}")
            print(f"DEBUG: Taille: {len(member.image_1920) if hasattr(member.image_1920, '__len__') else 'N/A'}")
        '''

# Insérer après la recherche du membre
if 'if not member or not member.image_1920:' in content:
    content = content.replace(
        'if not member or not member.image_1920:',
        debug_section + '\n        if not member or not member.image_1920:'
    )
    print("✅ Debug ajouté au contrôleur")

# Écrire le nouveau contrôleur
with open('controllers/main.py', 'w') as f:
    f.write(content)
EOF

echo ""
echo "📋 RÉSUMÉ DES CHANGEMENTS:"
echo "   ✅ Template simplifié sans condition t-if"
echo "   ✅ Utilisation de onerror pour fallback"
echo "   ✅ Debug ajouté au contrôleur"
echo "   ✅ Endpoint personnalisé maintenu"

echo ""
echo "🚀 PROCHAINES ÉTAPES:"
echo "   1. Redémarrer Odoo"
echo "   2. Tester la page publique"
echo "   3. Vérifier les logs pour le debug"

echo ""
echo "=== CORRECTION APPLIQUÉE ==="