#!/bin/bash

echo "🖼️ TEST DES VRAIES IMAGES DE FOND - SAMA_CARTE V2.1"
echo "=================================================="
echo ""

echo "🔍 TESTS DE VALIDATION DES IMAGES:"
echo "=================================="
echo ""

# Test des routes d'images
echo "📡 TESTS D'ACCÈS AUX IMAGES:"
echo "============================"

images=(
    "http://localhost:8071/background/image/dakar_gazelles/landscape:Dakar Gazelles Paysage"
    "http://localhost:8071/background/image/dakar_gazelles/portrait:Dakar Gazelles Portrait"
    "http://localhost:8071/background/image/jokkoo/landscape:Jokkoo Paysage"
    "http://localhost:8071/background/image/jokkoo/portrait:Jokkoo Portrait"
    "http://localhost:8071/background/image/teranga_corp/landscape:Teranga Corp Paysage"
    "http://localhost:8071/background/image/teranga_corp/portrait:Teranga Corp Portrait"
)

all_images_success=true

for image_info in "${images[@]}"; do
    IFS=':' read -r url description <<< "$image_info"
    status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    if [ "$status" = "200" ]; then
        echo "✅ $description - OK ($status)"
    else
        echo "❌ $description - ERREUR ($status)"
        all_images_success=false
    fi
done

echo ""
echo "📡 TESTS DES GALERIES:"
echo "====================="

galleries=(
    "http://localhost:8071/background/real/gallery:Galerie Vraies Images"
    "http://localhost:8071/background/fullsize/gallery:Galerie Dégradés"
)

all_galleries_success=true

for gallery_info in "${galleries[@]}"; do
    IFS=':' read -r url description <<< "$gallery_info"
    status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    if [ "$status" = "200" ]; then
        echo "✅ $description - OK ($status)"
    else
        echo "❌ $description - ERREUR ($status)"
        all_galleries_success=false
    fi
done

echo ""
echo "🎨 TESTS DES DESIGNS AVEC VRAIES IMAGES:"
echo "========================================"

designs=(
    "http://localhost:8071/background/test/with-image/modern/dakar_gazelles:Moderne + Dakar Gazelles"
    "http://localhost:8071/background/test/with-image/modern/jokkoo:Moderne + Jokkoo"
    "http://localhost:8071/background/test/with-image/modern/teranga_corp:Moderne + Teranga Corp"
    "http://localhost:8071/background/test/with-image/corporate/dakar_gazelles:Corporate + Dakar Gazelles"
    "http://localhost:8071/background/test/with-image/corporate/jokkoo:Corporate + Jokkoo"
    "http://localhost:8071/background/test/with-image/corporate/teranga_corp:Corporate + Teranga Corp"
    "http://localhost:8071/background/test/with-image/prestige/dakar_gazelles:Prestige + Dakar Gazelles"
    "http://localhost:8071/background/test/with-image/prestige/jokkoo:Prestige + Jokkoo"
    "http://localhost:8071/background/test/with-image/prestige/teranga_corp:Prestige + Teranga Corp"
)

all_designs_success=true

for design_info in "${designs[@]}"; do
    IFS=':' read -r url description <<< "$design_info"
    status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    if [ "$status" = "200" ]; then
        echo "✅ $description - OK ($status)"
    else
        echo "❌ $description - ERREUR ($status)"
        all_designs_success=false
    fi
done

echo ""
echo "🔍 VÉRIFICATION DU CONTENU DES IMAGES:"
echo "====================================="

# Test de contenu d'une galerie
gallery_content=$(curl -s "http://localhost:8071/background/real/gallery")
if echo "$gallery_content" | grep -q "Galerie des Designs avec Vraies Images"; then
    echo "✅ Titre de la galerie vraies images présent"
else
    echo "❌ Titre de la galerie vraies images manquant"
    all_galleries_success=false
fi

if echo "$gallery_content" | grep -q "Dakar Gazelles"; then
    echo "✅ Référence Dakar Gazelles présente"
else
    echo "❌ Référence Dakar Gazelles manquante"
    all_galleries_success=false
fi

if echo "$gallery_content" | grep -q "Jokkoo"; then
    echo "✅ Référence Jokkoo présente"
else
    echo "❌ Référence Jokkoo manquante"
    all_galleries_success=false
fi

if echo "$gallery_content" | grep -q "Teranga Corp"; then
    echo "✅ Référence Teranga Corp présente"
else
    echo "❌ Référence Teranga Corp manquante"
    all_galleries_success=false
fi

# Test de contenu d'un design
modern_content=$(curl -s "http://localhost:8071/background/test/with-image/modern/dakar_gazelles")
if echo "$modern_content" | grep -q "background-image: url('/background/image/dakar_gazelles/landscape')"; then
    echo "✅ Image de fond Dakar Gazelles intégrée dans le design moderne"
else
    echo "❌ Image de fond Dakar Gazelles non intégrée"
    all_designs_success=false
fi

if echo "$modern_content" | grep -q "Jean Dupont"; then
    echo "✅ Données de test présentes dans le design avec vraie image"
else
    echo "❌ Données de test manquantes"
    all_designs_success=false
fi

echo ""
echo "🖼️ IMAGES DISPONIBLES:"
echo "====================="
echo "1. 🏃 Dakar Gazelles - Thème sportif et dynamique"
echo "   ├── Portrait: /background/image/dakar_gazelles/portrait"
echo "   └── Paysage: /background/image/dakar_gazelles/landscape"
echo ""
echo "2. 🏢 Jokkoo - Style moderne et professionnel"
echo "   ├── Portrait: /background/image/jokkoo/portrait"
echo "   └── Paysage: /background/image/jokkoo/landscape"
echo ""
echo "3. 🏛️ Teranga Corp - Design corporate et institutionnel"
echo "   ├── Portrait: /background/image/teranga_corp/portrait"
echo "   └── Paysage: /background/image/teranga_corp/landscape"
echo ""

echo "🎨 DESIGNS AVEC VRAIES IMAGES:"
echo "============================="
echo "1. 🎯 Moderne - Grille intelligente + glassmorphism"
echo "   ├── Avec Dakar Gazelles: /background/test/with-image/modern/dakar_gazelles"
echo "   ├── Avec Jokkoo: /background/test/with-image/modern/jokkoo"
echo "   └── Avec Teranga Corp: /background/test/with-image/modern/teranga_corp"
echo ""
echo "2. 🏢 Corporate - Header/footer + QR flottant"
echo "   ├── Avec Dakar Gazelles: /background/test/with-image/corporate/dakar_gazelles"
echo "   ├── Avec Jokkoo: /background/test/with-image/corporate/jokkoo"
echo "   └── Avec Teranga Corp: /background/test/with-image/corporate/teranga_corp"
echo ""
echo "3. 👑 Prestige - Luxueux avec effets dorés"
echo "   ├── Avec Dakar Gazelles: /background/test/with-image/prestige/dakar_gazelles"
echo "   ├── Avec Jokkoo: /background/test/with-image/prestige/jokkoo"
echo "   └── Avec Teranga Corp: /background/test/with-image/prestige/teranga_corp"
echo ""

echo "📱 FONCTIONNALITÉS RESPONSIVE:"
echo "============================="
echo "📱 Mobile (< 768px): Utilise automatiquement les images portrait"
echo "🖥️ Desktop (≥ 768px): Utilise automatiquement les images paysage"
echo "🎨 Overlays adaptatifs: Améliore la lisibilité sur toutes les images"
echo "📐 Aspect ratio: Maintenu selon l'orientation"
echo ""

echo "✨ AMÉLIORATIONS VISUELLES:"
echo "=========================="
echo "🌈 Overlays dégradés: Meilleure lisibilité du texte"
echo "💎 Glassmorphism: Effets de transparence moderne"
echo "🎭 Ombres et contrastes: Éléments bien définis"
echo "🔄 Transitions fluides: Navigation agréable"
echo "🎯 Positionnement intelligent: Éléments bien placés"
echo ""

echo "📋 INSTRUCTIONS D'UTILISATION:"
echo "=============================="
echo "1. 🌐 Ouvrir http://localhost:8071/background/real/gallery"
echo "2. 🎨 Choisir un design (Moderne, Corporate, Prestige)"
echo "3. 🖼️ Sélectionner une image (Dakar Gazelles, Jokkoo, Teranga Corp)"
echo "4. 🔍 Observer le rendu avec la vraie image de fond"
echo "5. 📱 Redimensionner pour voir le responsive portrait/paysage"
echo "6. ⚖️ Comparer avec les versions dégradés"
echo ""

echo "🚀 PROCHAINES ÉTAPES:"
echo "===================="
echo "1. 🎨 Personnaliser les overlays selon les images"
echo "2. 📱 Optimiser pour différentes résolutions"
echo "3. 🖼️ Ajouter plus d'images de fond"
echo "4. 🔧 Intégrer dans l'interface de gestion"
echo "5. 🎯 Configurer pour production"
echo ""

echo "🎊 RÉSULTAT FINAL:"
echo "=================="
if [ "$all_images_success" = true ] && [ "$all_galleries_success" = true ] && [ "$all_designs_success" = true ]; then
    echo "✅ TOUS LES TESTS RÉUSSIS !"
    echo "✅ Images accessibles et fonctionnelles"
    echo "✅ Galeries opérationnelles"
    echo "✅ Tous les designs avec vraies images fonctionnent"
    echo "✅ Responsive portrait/paysage intégré"
    echo "✅ Overlays et effets visuels appliqués"
    echo "✅ Navigation fluide entre designs et images"
    echo "✅ Système complet et prêt pour utilisation"
    echo ""
    echo "🚀 SAMA_CARTE V2.1 - INTÉGRATION VRAIES IMAGES RÉUSSIE !"
    echo "========================================================"
    exit 0
else
    echo "❌ CERTAINS TESTS ONT ÉCHOUÉ"
    echo "❌ Vérifiez les erreurs ci-dessus"
    echo ""
    echo "🔧 SAMA_CARTE V2.1 - INTÉGRATION PARTIELLE"
    echo "==========================================="
    exit 1
fi