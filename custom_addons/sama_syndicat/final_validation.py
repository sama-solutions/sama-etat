#!/usr/bin/env python3
"""
Validation finale complète du module web_studio_community
Test de bout en bout pour confirmer que tout fonctionne parfaitement
"""

import subprocess
import time
import sys
import os

def run_all_tests():
    """Exécuter tous les tests de validation"""
    print("🎯 VALIDATION FINALE COMPLÈTE - WEB STUDIO COMMUNITY")
    print("=" * 70)
    
    tests = [
        {
            'name': 'Test de structure et syntaxe',
            'script': 'comprehensive_test.py',
            'description': 'Validation de tous les fichiers et de la structure'
        },
        {
            'name': 'Test fonctionnel complet',
            'script': 'functional_test.py', 
            'description': 'Test avec Odoo en cours d\'exécution'
        }
    ]
    
    results = []
    
    for test in tests:
        print(f"\n🔍 {test['name']}")
        print(f"📝 {test['description']}")
        print("-" * 50)
        
        if not os.path.exists(test['script']):
            print(f"❌ Script de test manquant: {test['script']}")
            results.append((test['name'], False))
            continue
        
        try:
            result = subprocess.run(['python3', test['script']], 
                                  capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"✅ {test['name']}: RÉUSSI")
                results.append((test['name'], True))
            else:
                print(f"❌ {test['name']}: ÉCHEC")
                print(f"Erreur: {result.stderr[-200:]}")
                results.append((test['name'], False))
                
        except subprocess.TimeoutExpired:
            print(f"⏰ {test['name']}: TIMEOUT")
            results.append((test['name'], False))
        except Exception as e:
            print(f"❌ {test['name']}: ERREUR - {e}")
            results.append((test['name'], False))
    
    return results

def validate_file_integrity():
    """Valider l'intégrité de tous les fichiers"""
    print("\n🔍 Validation de l'intégrité des fichiers")
    print("-" * 50)
    
    critical_files = [
        '../web_studio_community/__init__.py',
        '../web_studio_community/__manifest__.py',
        '../web_studio_community/models/__init__.py',
        '../web_studio_community/models/studio_customization.py',
        '../web_studio_community/models/ir_model.py',
        '../web_studio_community/models/ir_model_fields.py',
        '../web_studio_community/views/studio_menus.xml',
        '../web_studio_community/views/studio_model_views.xml',
        '../web_studio_community/security/ir.model.access.csv'
    ]
    
    all_good = True
    
    for file_path in critical_files:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}: Manquant ou vide")
            all_good = False
    
    return all_good

def check_addon_path():
    """Vérifier que le lien symbolique est correct"""
    print("\n🔍 Validation du lien symbolique")
    print("-" * 50)
    
    link_path = "/tmp/addons_sama_syndicat/web_studio_community"
    target_path = "/home/grand-as/psagsn/custom_addons/web_studio_community"
    
    if os.path.islink(link_path):
        actual_target = os.readlink(link_path)
        if actual_target == target_path:
            print(f"✅ Lien symbolique correct: {link_path} -> {target_path}")
            return True
        else:
            print(f"❌ Lien symbolique incorrect: {link_path} -> {actual_target}")
            return False
    else:
        print(f"❌ Lien symbolique manquant: {link_path}")
        return False

def validate_scripts():
    """Valider que tous les scripts de démarrage sont présents"""
    print("\n🔍 Validation des scripts de démarrage")
    print("-" * 50)
    
    scripts = [
        'start_odoo_final_optimized.py',
        'comprehensive_test.py',
        'functional_test.py'
    ]
    
    all_good = True
    
    for script in scripts:
        if os.path.exists(script) and os.access(script, os.X_OK):
            print(f"✅ {script}: Présent et exécutable")
        else:
            print(f"❌ {script}: Manquant ou non exécutable")
            all_good = False
    
    return all_good

def main():
    """Fonction principale de validation finale"""
    print("🎯 VALIDATION FINALE COMPLÈTE")
    print("Vérification que tous les problèmes ont été résolus")
    print("=" * 70)
    
    # Étapes de validation
    validations = [
        ("Intégrité des fichiers", validate_file_integrity),
        ("Lien symbolique", check_addon_path),
        ("Scripts de démarrage", validate_scripts)
    ]
    
    validation_results = []
    
    # Exécuter les validations préliminaires
    for name, func in validations:
        print(f"\n🔍 {name}")
        print("-" * 50)
        result = func()
        validation_results.append((name, result))
        if result:
            print(f"✅ {name}: VALIDÉ")
        else:
            print(f"❌ {name}: PROBLÈME DÉTECTÉ")
    
    # Exécuter les tests complets
    test_results = run_all_tests()
    
    # Résumé final
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DE LA VALIDATION FINALE")
    print("=" * 70)
    
    print("\n🔧 Validations préliminaires:")
    for name, result in validation_results:
        status = "✅ VALIDÉ" if result else "❌ PROBLÈME"
        print(f"  {name:.<40} {status}")
    
    print("\n🧪 Tests complets:")
    for name, result in test_results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHEC"
        print(f"  {name:.<40} {status}")
    
    # Calcul du score global
    all_validations = validation_results + test_results
    passed = sum(1 for _, result in all_validations if result)
    total = len(all_validations)
    
    print("\n" + "=" * 70)
    print(f"🎯 SCORE GLOBAL: {passed}/{total} validations réussies")
    
    if passed == total:
        print("\n🎉 VALIDATION FINALE RÉUSSIE!")
        print("🚀 Le module web_studio_community est COMPLÈTEMENT FONCTIONNEL")
        print("✅ Tous les problèmes ont été résolus")
        print("✅ Prêt pour utilisation en production")
        print("\n📋 Pour démarrer Odoo:")
        print("   python3 start_odoo_final_optimized.py")
        print("\n🌐 Interface web:")
        print("   http://localhost:8070/web")
        return True
    else:
        print("\n⚠️ VALIDATION FINALE ÉCHOUÉE")
        print(f"❌ {total - passed} problème(s) détecté(s)")
        print("🔧 Des corrections supplémentaires sont nécessaires")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)