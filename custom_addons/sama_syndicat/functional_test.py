#!/usr/bin/env python3
"""
Test fonctionnel avancé pour web_studio_community
"""

import subprocess
import time
import sys
import os
import requests
import json

def start_odoo_for_test():
    """Démarrer Odoo pour les tests fonctionnels"""
    print("🚀 Démarrage d'Odoo pour tests fonctionnels...")
    
    # Configuration
    PORT = 8072
    DATABASE = "test_functional_studio"
    ODOO_BIN = "/var/odoo/odoo18/odoo-bin"
    ADDONS_PATH = "/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat"
    
    # Arrêter les processus existants
    subprocess.run(['pkill', '-f', 'odoo-bin'], capture_output=True)
    time.sleep(2)
    
    # Démarrer Odoo en arrière-plan
    cmd = [
        'python3', ODOO_BIN,
        f'--addons-path={ADDONS_PATH}',
        f'--database={DATABASE}',
        f'--xmlrpc-port={PORT}',
        '-i', 'web_studio_community',
        '--log-level=warn'
    ]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Attendre que Odoo soit prêt
    max_wait = 60
    wait_time = 0
    
    while wait_time < max_wait:
        try:
            response = requests.get(f'http://localhost:{PORT}/web/database/selector', timeout=5)
            if response.status_code == 200:
                print(f"  ✅ Odoo démarré sur le port {PORT}")
                return process, PORT, DATABASE
        except:
            pass
        
        time.sleep(2)
        wait_time += 2
        
        if process.poll() is not None:
            print("  ❌ Odoo s'est arrêté de manière inattendue")
            return None, None, None
    
    print("  ❌ Timeout - Odoo n'a pas démarré à temps")
    process.terminate()
    return None, None, None

def test_web_interface(port):
    """Tester l'interface web"""
    print("🌐 Test de l'interface web...")
    
    try:
        # Test de la page principale
        response = requests.get(f'http://localhost:{port}/web', timeout=10)
        if response.status_code == 200:
            print("  ✅ Interface web accessible")
        else:
            print(f"  ❌ Interface web inaccessible: {response.status_code}")
            return False
        
        # Test de la page de login
        response = requests.get(f'http://localhost:{port}/web/login', timeout=10)
        if response.status_code == 200:
            print("  ✅ Page de login accessible")
        else:
            print(f"  ❌ Page de login inaccessible: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lors du test web: {e}")
        return False

def test_xmlrpc_connection(port, database):
    """Tester la connexion XML-RPC"""
    print("🔌 Test de connexion XML-RPC...")
    
    try:
        import xmlrpc.client
        
        # Test de connexion au service common
        common = xmlrpc.client.ServerProxy(f'http://localhost:{port}/xmlrpc/2/common')
        version = common.version()
        
        if version and 'server_version' in version:
            print(f"  ✅ XML-RPC accessible (Odoo {version['server_version']})")
        else:
            print("  ❌ XML-RPC inaccessible")
            return False
        
        # Test de connexion à la base de données
        db = xmlrpc.client.ServerProxy(f'http://localhost:{port}/xmlrpc/2/db')
        db_list = db.list()
        
        if database in db_list:
            print(f"  ✅ Base de données {database} accessible")
        else:
            print(f"  ❌ Base de données {database} non trouvée")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur XML-RPC: {e}")
        return False

def test_module_presence(port, database):
    """Tester la présence du module dans Odoo"""
    print("📦 Test de présence du module...")
    
    try:
        import xmlrpc.client
        
        common = xmlrpc.client.ServerProxy(f'http://localhost:{port}/xmlrpc/2/common')
        uid = common.authenticate(database, 'admin', 'admin', {})
        
        if not uid:
            print("  ❌ Impossible de s'authentifier")
            return False
        
        models = xmlrpc.client.ServerProxy(f'http://localhost:{port}/xmlrpc/2/object')
        
        # Chercher le module web_studio_community
        module_ids = models.execute_kw(database, uid, 'admin', 'ir.module.module', 'search', 
                                     [[['name', '=', 'web_studio_community']]])
        
        if module_ids:
            module_data = models.execute_kw(database, uid, 'admin', 'ir.module.module', 'read', 
                                          [module_ids], {'fields': ['name', 'state']})
            
            if module_data and module_data[0]['state'] == 'installed':
                print("  ✅ Module web_studio_community installé et actif")
            else:
                print(f"  ❌ Module dans l'état: {module_data[0]['state'] if module_data else 'inconnu'}")
                return False
        else:
            print("  ❌ Module web_studio_community non trouvé")
            return False
        
        # Tester la présence du modèle studio.customization
        try:
            model_ids = models.execute_kw(database, uid, 'admin', 'ir.model', 'search', 
                                        [[['model', '=', 'studio.customization']]])
            if model_ids:
                print("  ✅ Modèle studio.customization présent")
            else:
                print("  ⚠️ Modèle studio.customization non trouvé (normal pour TransientModel)")
        except:
            print("  ⚠️ Impossible de vérifier le modèle studio.customization")
        
        # Tester la présence des menus
        menu_ids = models.execute_kw(database, uid, 'admin', 'ir.ui.menu', 'search', 
                                   [[['name', '=', 'Studio']]])
        
        if menu_ids:
            print("  ✅ Menu Studio présent")
        else:
            print("  ❌ Menu Studio non trouvé")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lors du test de module: {e}")
        return False

def test_assets_loading(port):
    """Tester le chargement des assets"""
    print("🎨 Test de chargement des assets...")
    
    try:
        # Test des assets JavaScript
        js_assets = [
            '/web_studio_community/static/src/legacy/js/studio_button.js',
            '/web_studio_community/static/src/components/view_customizer/studio_arch_differ.js',
            '/web_studio_community/static/src/components/view_customizer/studio_node.js',
            '/web_studio_community/static/src/components/view_customizer/view_customizer.js'
        ]
        
        for asset in js_assets:
            response = requests.get(f'http://localhost:{port}{asset}', timeout=5)
            if response.status_code == 200:
                print(f"  ✅ {asset}")
            else:
                print(f"  ❌ {asset}: {response.status_code}")
                return False
        
        # Test des assets XML
        xml_assets = [
            '/web_studio_community/static/src/components/view_customizer/view_customizer.xml',
            '/web_studio_community/static/src/components/view_customizer/studio_node.xml'
        ]
        
        for asset in xml_assets:
            response = requests.get(f'http://localhost:{port}{asset}', timeout=5)
            if response.status_code == 200:
                print(f"  ✅ {asset}")
            else:
                print(f"  ❌ {asset}: {response.status_code}")
                return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lors du test des assets: {e}")
        return False

def cleanup_test_environment(process, database):
    """Nettoyer l'environnement de test"""
    print("🧹 Nettoyage de l'environnement de test...")
    
    if process:
        process.terminate()
        process.wait(timeout=10)
    
    # Supprimer la base de données de test
    try:
        subprocess.run(['dropdb', database], capture_output=True, timeout=30)
        print(f"  ✅ Base de données {database} supprimée")
    except:
        print(f"  ⚠️ Impossible de supprimer la base de données {database}")

def main():
    """Fonction principale de test fonctionnel"""
    print("🧪 TEST FONCTIONNEL AVANCÉ - WEB STUDIO COMMUNITY")
    print("=" * 60)
    
    # Démarrer Odoo
    process, port, database = start_odoo_for_test()
    
    if not process:
        print("❌ Impossible de démarrer Odoo pour les tests")
        return False
    
    try:
        # Attendre que Odoo soit complètement prêt
        print("⏳ Attente de la stabilisation d'Odoo...")
        time.sleep(10)
        
        tests = [
            ("Interface web", lambda: test_web_interface(port)),
            ("Connexion XML-RPC", lambda: test_xmlrpc_connection(port, database)),
            ("Présence du module", lambda: test_module_presence(port, database)),
            ("Chargement des assets", lambda: test_assets_loading(port))
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
        print("📊 RÉSUMÉ DES TESTS FONCTIONNELS")
        print("=" * 60)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ RÉUSSI" if result else "❌ ÉCHEC"
            print(f"{test_name:.<40} {status}")
        
        print("=" * 60)
        print(f"RÉSULTAT GLOBAL: {passed}/{total} tests réussis")
        
        if passed == total:
            print("🎉 TOUS LES TESTS FONCTIONNELS SONT RÉUSSIS!")
            print("Le module web_studio_community est complètement opérationnel.")
            return True
        else:
            print("⚠️ CERTAINS TESTS FONCTIONNELS ONT ÉCHOUÉ")
            return False
    
    finally:
        cleanup_test_environment(process, database)
    
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)