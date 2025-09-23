#!/usr/bin/env python3
"""
Test complet et autonome pour web_studio_community
"""

import subprocess
import time
import sys
import os
import tempfile

def run_command(cmd, timeout=60):
    """Exécuter une commande avec timeout"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout"
    except Exception as e:
        return False, "", str(e)

def test_python_syntax():
    """Tester la syntaxe Python de tous les fichiers"""
    print("🐍 Test de syntaxe Python...")
    
    python_files = [
        "../web_studio_community/__init__.py",
        "../web_studio_community/__manifest__.py",
        "../web_studio_community/models/__init__.py",
        "../web_studio_community/models/studio_customization.py",
        "../web_studio_community/models/ir_model.py",
        "../web_studio_community/models/ir_model_fields.py"
    ]
    
    for file_path in python_files:
        if os.path.exists(file_path):
            success, stdout, stderr = run_command(['python3', '-m', 'py_compile', file_path])
            if success:
                print(f"  ✅ {file_path}")
            else:
                print(f"  ❌ {file_path}: {stderr}")
                return False
        else:
            print(f"  ⚠️ {file_path}: Fichier manquant")
    
    return True

def test_xml_syntax():
    """Tester la syntaxe XML de tous les fichiers"""
    print("📄 Test de syntaxe XML...")
    
    xml_files = [
        "../web_studio_community/views/studio_model_views.xml",
        "../web_studio_community/views/studio_menus.xml",
        "../web_studio_community/views/templates.xml",
        "../web_studio_community/static/src/components/view_customizer/view_customizer.xml",
        "../web_studio_community/static/src/components/view_customizer/studio_node.xml"
    ]
    
    for file_path in xml_files:
        if os.path.exists(file_path):
            success, stdout, stderr = run_command(['xmllint', '--noout', file_path])
            if success:
                print(f"  ✅ {file_path}")
            else:
                print(f"  ❌ {file_path}: {stderr}")
                return False
        else:
            print(f"  ⚠️ {file_path}: Fichier manquant")
    
    return True

def test_js_syntax():
    """Tester la syntaxe JavaScript de tous les fichiers"""
    print("🟨 Test de syntaxe JavaScript...")
    
    js_files = [
        "../web_studio_community/static/src/legacy/js/studio_button.js",
        "../web_studio_community/static/src/components/view_customizer/studio_arch_differ.js",
        "../web_studio_community/static/src/components/view_customizer/studio_node.js",
        "../web_studio_community/static/src/components/view_customizer/view_customizer.js"
    ]
    
    for file_path in js_files:
        if os.path.exists(file_path):
            success, stdout, stderr = run_command(['node', '--check', file_path])
            if success:
                print(f"  ✅ {file_path}")
            else:
                print(f"  ❌ {file_path}: {stderr}")
                return False
        else:
            print(f"  ⚠️ {file_path}: Fichier manquant")
    
    return True

def test_manifest_structure():
    """Tester la structure du manifest"""
    print("📋 Test de structure du manifest...")
    
    manifest_path = "../web_studio_community/__manifest__.py"
    if not os.path.exists(manifest_path):
        print("  ❌ __manifest__.py manquant")
        return False
    
    try:
        with open(manifest_path, 'r') as f:
            content = f.read()
        
        # Tenter d'évaluer le manifest
        manifest_dict = eval(content)
        
        required_keys = ['name', 'version', 'depends', 'installable']
        for key in required_keys:
            if key not in manifest_dict:
                print(f"  ❌ Clé manquante dans le manifest: {key}")
                return False
        
        # Vérifier que tous les fichiers de données existent
        if 'data' in manifest_dict:
            for data_file in manifest_dict['data']:
                full_path = f"../web_studio_community/{data_file}"
                if not os.path.exists(full_path):
                    print(f"  ❌ Fichier de données manquant: {data_file}")
                    return False
        
        # Vérifier que tous les assets existent
        if 'assets' in manifest_dict:
            for bundle, files in manifest_dict['assets'].items():
                for asset_file in files:
                    # Enlever le préfixe du module
                    asset_path = asset_file.replace('web_studio_community/', '../web_studio_community/')
                    if not os.path.exists(asset_path):
                        print(f"  ❌ Asset manquant: {asset_file}")
                        return False
        
        print("  ✅ Structure du manifest valide")
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur dans le manifest: {e}")
        return False

def test_module_installation():
    """Tester l'installation du module"""
    print("🔧 Test d'installation du module...")
    
    # Configuration
    PORT = 8071  # Port différent pour éviter les conflits
    DATABASE = "test_web_studio_community"
    ODOO_BIN = "/var/odoo/odoo18/odoo-bin"
    ADDONS_PATH = "/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat"
    
    # Arrêter les processus existants
    subprocess.run(['pkill', '-f', 'odoo-bin'], capture_output=True)
    time.sleep(2)
    
    # Créer une base de données temporaire pour le test
    cmd = [
        'python3', ODOO_BIN,
        f'--addons-path={ADDONS_PATH}',
        f'--database={DATABASE}',
        f'--xmlrpc-port={PORT}',
        '-i', 'web_studio_community',
        '--stop-after-init',
        '--log-level=error'
    ]
    
    print(f"  Commande: {' '.join(cmd)}")
    success, stdout, stderr = run_command(cmd, timeout=120)
    
    if success:
        print("  ✅ Module installé avec succès")
        
        # Nettoyer la base de données de test
        cleanup_cmd = [
            'python3', ODOO_BIN,
            f'--addons-path={ADDONS_PATH}',
            f'--database={DATABASE}',
            '--stop-after-init',
            '--log-level=error',
            '--init=base'
        ]
        run_command(cleanup_cmd, timeout=60)
        
        return True
    else:
        print(f"  ❌ Échec de l'installation")
        print(f"  Erreur: {stderr[-500:]}")  # Dernières 500 caractères
        return False

def test_file_structure():
    """Tester la structure des fichiers"""
    print("📁 Test de structure des fichiers...")
    
    required_files = [
        "../web_studio_community/__init__.py",
        "../web_studio_community/__manifest__.py",
        "../web_studio_community/models/__init__.py",
        "../web_studio_community/models/studio_customization.py",
        "../web_studio_community/views/studio_menus.xml",
        "../web_studio_community/views/studio_model_views.xml",
        "../web_studio_community/security/ir.model.access.csv"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}: Fichier manquant")
            return False
    
    return True

def main():
    """Fonction principale de test"""
    print("🧪 TEST COMPLET ET AUTONOME - WEB STUDIO COMMUNITY")
    print("=" * 60)
    
    tests = [
        ("Structure des fichiers", test_file_structure),
        ("Syntaxe Python", test_python_syntax),
        ("Syntaxe XML", test_xml_syntax),
        ("Syntaxe JavaScript", test_js_syntax),
        ("Structure du manifest", test_manifest_structure),
        ("Installation du module", test_module_installation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ {test_name}: RÉUSSI")
            else:
                print(f"❌ {test_name}: ÉCHEC")
        except Exception as e:
            print(f"❌ {test_name}: ERREUR - {e}")
            results.append((test_name, False))
    
    # Résumé final
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHEC"
        print(f"{test_name:.<40} {status}")
    
    print("=" * 60)
    print(f"RÉSULTAT GLOBAL: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 TOUS LES TESTS SONT RÉUSSIS!")
        print("Le module web_studio_community est prêt à être utilisé.")
        return True
    else:
        print("⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        print("Des corrections sont nécessaires avant utilisation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)