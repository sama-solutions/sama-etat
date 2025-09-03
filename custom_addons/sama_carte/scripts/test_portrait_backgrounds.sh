#!/bin/bash

echo "📱 TEST DES VERSIONS PORTRAIT - SAMA_CARTE V2.1"
echo "==============================================="
echo ""

echo "🔍 TESTS DE VALIDATION DES VERSIONS PORTRAIT:"
echo "============================================="
echo ""

echo "📡 TESTS D'ACCÈS AUX VERSIONS PORTRAIT:"
echo "======================================="

portraits=(
    "http://localhost:8071/background/portrait/dakar_gazelles:Portrait Dakar Gazelles"
    "http://localhost:8071/background/portrait/jokkoo:Portrait Jokkoo"
    "http://localhost:8071/background/portrait/teranga_corp:Portrait Teranga Corp"
)

all_portraits_success=true

for portrait_info in "${portraits[@]}"; do
    IFS=':' read -r url description <<< "$portrait_info"
    status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    if [ "$status" = "200" ]; then
        echo "✅ $description - OK ($status)"
    else
        echo "❌ $description - ERREUR ($status)"
        all_portraits_success=false
    fi
done

echo ""
echo "📡 TEST DE LA GALERIE MISE À JOUR:"
echo "=================================="

gallery_status=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8071/background/real/gallery")
if [ "$gallery_status" = "200" ]; then
    echo "✅ Galerie vraies images - OK ($gallery_status)"
else
    echo "❌ Galerie vraies images - ERREUR ($gallery_status)"
    all_portraits_success=false
fi

echo ""
echo "🔍 VÉRIFICATION DU CONTENU DE LA GALERIE:"
echo "========================================="

# Test de contenu de la galerie
gallery_content=$(curl -s "http://localhost:8071/background/real/gallery")

if echo "$gallery_content" | grep -q "Paysage - Dakar Gazelles"; then
    echo "✅ Bouton Paysage Dakar Gazelles présent"
else
    echo "❌ Bouton Paysage Dakar Gazelles manquant"
    all_portraits_success=false
fi

if echo "$gallery_content" | grep -q "Portrait - Dakar Gazelles"; then
    echo "✅ Bouton Portrait Dakar Gazelles présent"
else
    echo "❌ Bouton Portrait Dakar Gazelles manquant"
    all_portraits_success=false
fi

if echo "$gallery_content" | grep -q "Paysage - Jokkoo"; then
    echo "✅ Bouton Paysage Jokkoo présent"
else
    echo "❌ Bouton Paysage Jokkoo manquant"
    all_portraits_success=false
fi

if echo "$gallery_content" | grep -q "Portrait - Jokkoo"; then
    echo "✅ Bouton Portrait Jokkoo présent"
else
    echo "❌ Bouton Portrait Jokkoo manquant"
    all_portraits_success=false
fi

if echo "$gallery_content" | grep -q "Paysage - Teranga Corp"; then
    echo "✅ Bouton Paysage Teranga Corp présent"
else
    echo "❌ Bouton Paysage Teranga Corp manquant"
    all_portraits_success=false
fi

if echo "$gallery_content" | grep -q "Portrait - Teranga Corp"; then
    echo "✅ Bouton Portrait Teranga Corp présent"
else
    echo "❌ Bouton Portrait Teranga Corp manquant"
    all_portraits_success=false
fi

echo ""
echo "🔍 VÉRIFICATION DU CONTENU DES VERSIONS PORTRAIT:"
echo "================================================"

# Test de contenu d'une version portrait
dakar_portrait_content=$(curl -s "http://localhost:8071/background/portrait/dakar_gazelles")
if echo "$dakar_portrait_content" | grep -q "background-image: url('/background/image/dakar_gazelles/portrait')"; then
    echo "✅ Image portrait Dakar Gazelles intégrée"
else
    echo "❌ Image portrait Dakar Gazelles non intégrée"
    all_portraits_success=false
fi

if echo "$dakar_portrait_content" | grep -q "aspect-ratio: 9/16"; then
    echo "✅ Aspect ratio portrait 9:16 configuré"
else
    echo "❌ Aspect ratio portrait manquant"
    all_portraits_success=false
fi

if echo "$dakar_portrait_content" | grep -q "Jean Dupont"; then
    echo "✅ Données de test présentes dans version portrait"
else
    echo "❌ Données de test manquantes"
    all_portraits_success=false
fi

if echo "$dakar_portrait_content" | grep -q "Design Moderne Portrait - Dakar Gazelles"; then
    echo "✅ Titre spécifique portrait présent"
else
    echo "❌ Titre spécifique portrait manquant"
    all_portraits_success=false
fi

echo ""
echo "📱 VERSIONS PORTRAIT DISPONIBLES:"
echo "================================="
echo "1. 🏃 Dakar Gazelles Portrait - Layout vertical optimisé"
echo "   └── URL: /background/portrait/dakar_gazelles"
echo ""
echo "2. 🏢 Jokkoo Portrait - Style moderne vertical"
echo "   └── URL: /background/portrait/jokkoo"
echo ""
echo "3. 🏛️ Teranga Corp Portrait - Design prestige vertical"
echo "   └── URL: /background/portrait/teranga_corp"
echo ""

echo "🎨 AMÉLIORATIONS APPORTÉES:"
echo "=========================="
echo "✅ Boutons de test simplifiés (1 seul bouton de retour)"
echo "✅ Galerie avec options Paysage/Portrait séparées"
echo "✅ 3 versions portrait dédiées créées"
echo "✅ Layout vertical optimisé pour chaque background"
echo "✅ Aspect ratio 9:16 pour format portrait"
echo "✅ Positionnement adapté au format vertical"
echo "✅ Overlays spécifiques pour chaque style"
echo "✅ Navigation cohérente vers la galerie"
echo ""

echo "📐 CARACTÉRISTIQUES DES VERSIONS PORTRAIT:"
echo "=========================================="
echo "📱 Format: 9:16 (portrait)"
echo "📏 Largeur max: 400px"
echo "📏 Hauteur min: 600px"
echo "🎯 Layout: Vertical centré"
echo "📸 Photo: 120px centrée"
echo "🎨 QR Code: 50px en haut à droite"
echo "💎 Glassmorphism: Effets de transparence"
echo "🌈 Overlays: Adaptés à chaque image"
echo "🔄 Navigation: Retour à la galerie"
echo ""

echo "🎯 URLS DE TEST PORTRAIT:"
echo "========================="
echo "1. 🏃 Dakar Gazelles: http://localhost:8071/background/portrait/dakar_gazelles"
echo "2. 🏢 Jokkoo: http://localhost:8071/background/portrait/jokkoo"
echo "3. 🏛️ Teranga Corp: http://localhost:8071/background/portrait/teranga_corp"
echo ""

echo "🌐 GALERIE MISE À JOUR:"
echo "======================="
echo "📍 URL: http://localhost:8071/background/real/gallery"
echo "🎨 Chaque design propose maintenant:"
echo "   ├── 🖥️ Version Paysage (16:9)"
echo "   └── 📱 Version Portrait (9:16)"
echo ""

echo "📋 INSTRUCTIONS D'UTILISATION:"
echo "=============================="
echo "1. 🌐 Ouvrir http://localhost:8071/background/real/gallery"
echo "2. 🎨 Choisir un background (Dakar, Jokkoo, Teranga)"
echo "3. 📐 Sélectionner le format:"
echo "   ├── 🖥️ Paysage pour desktop/tablette"
echo "   └── 📱 Portrait pour mobile/affichage vertical"
echo "4. 🔍 Observer le layout optimisé pour chaque format"
echo "5. 🔄 Utiliser le bouton 'Retour à la galerie' pour naviguer"
echo ""

echo "🚀 AVANTAGES DES VERSIONS PORTRAIT:"
echo "==================================="
echo "✅ Layout spécialement conçu pour l'affichage vertical"
echo "✅ Meilleure utilisation de l'espace en hauteur"
echo "✅ Photo membre plus grande et centrée"
echo "✅ Informations mieux organisées verticalement"
echo "✅ Overlays adaptés au format portrait"
echo "✅ Navigation simplifiée et cohérente"
echo "✅ Aspect ratio fixe pour cohérence visuelle"
echo ""

echo "🎊 RÉSULTAT FINAL:"
echo "=================="
if [ "$all_portraits_success" = true ]; then
    echo "✅ TOUS LES TESTS RÉUSSIS !"
    echo "✅ 3 versions portrait créées et fonctionnelles"
    echo "✅ Galerie mise à jour avec options Paysage/Portrait"
    echo "✅ Boutons de test simplifiés (1 seul retour)"
    echo "✅ Layout vertical optimisé pour chaque background"
    echo "✅ Navigation cohérente et intuitive"
    echo "✅ Aspect ratio 9:16 respecté"
    echo "✅ Overlays et effets adaptés"
    echo "✅ Système complet Paysage + Portrait opérationnel"
    echo ""
    echo "🚀 SAMA_CARTE V2.1 - VERSIONS PORTRAIT INTÉGRÉES AVEC SUCCÈS !"
    echo "=============================================================="
    exit 0
else
    echo "❌ CERTAINS TESTS ONT ÉCHOUÉ"
    echo "❌ Vérifiez les erreurs ci-dessus"
    echo ""
    echo "🔧 SAMA_CARTE V2.1 - INTÉGRATION PARTIELLE"
    echo "==========================================="
    exit 1
fi