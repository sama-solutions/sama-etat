#!/usr/bin/env python3
"""
Diagnostic d'accès aux paramètres Odoo
"""

import subprocess
import time
import sys
import requests
import xmlrpc.client

def start_odoo_for_diagnosis():
    """Démarrer Odoo pour diagnostic"""
    print("🔍 DIAGNOSTIC D'ACCÈS AUX PARAMÈTRES")
    print("=" * 50)
    
    # Configuration
    PORT = 8074
    DATABASE = "sama_syndicat_final_1756812346"
    ODOO_BIN = "/var/odoo/odoo18/odoo-bin"
    ADDONS_PATH = "/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat"
    
    # Arrêter les processus existants
    print("🛑 Arrêt des processus existants...")
    subprocess.run(['pkill', '-f', 'odoo-bin'], capture_output=True)
    time.sleep(3)
    
    # Démarrer Odoo
    cmd = [
        'python3', ODOO_BIN,
        f'--addons-path={ADDONS_PATH}',
        f'--database={DATABASE}',
        f'--xmlrpc-port={PORT}',
        '--log-level=info'
    ]
    
    print("🚀 Démarrage d'Odoo pour diagnostic...")
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Attendre que Odoo soit prêt
    max_wait = 60
    wait_time = 0
    
    while wait_time < max_wait:
        try:
            response = requests.get(f'http://localhost:{PORT}/web', timeout=5)
            if response.status_code == 200:
                print(f"✅ Odoo démarré sur le port {PORT}")
                return process, PORT, DATABASE
        except:
            pass
        
        time.sleep(2)
        wait_time += 2
        
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print("❌ Odoo s'est arrêté de manière inattendue")
            print(f"Erreur: {stderr.decode()[-500:]}")
            return None, None, None
    
    print("❌ Timeout - Odoo n'a pas démarré à temps")
    process.terminate()
    return None, None, None

def test_xmlrpc_access(port, database):
    """Tester l'accès XML-RPC et les modèles"""
    print("\n🔌 Test d'accès XML-RPC...")
    
    try:
        # Connexion XML-RPC
        common = xmlrpc.client.ServerProxy(f'http://localhost:{port}/xmlrpc/2/common')
        uid = common.authenticate(database, 'admin', 'admin', {})
        
        if not uid:
            print("❌ Impossible de s'authentifier")
            return False
        
        print(f"✅ Authentification réussie (UID: {uid})")
        
        models = xmlrpc.client.ServerProxy(f'http://localhost:{port}/xmlrpc/2/object')
        
        # Tester l'accès au modèle res.config.settings
        print("\n📋 Test du modèle res.config.settings...")
        try:
            # Chercher les enregistrements de configuration
            config_ids = models.execute_kw(database, uid, 'admin', 'res.config.settings', 'search', [[]])
            print(f"✅ Modèle res.config.settings accessible ({len(config_ids)} enregistrements)")
            
            # Tester la création d'un enregistrement temporaire
            try:
                temp_config = models.execute_kw(database, uid, 'admin', 'res.config.settings', 'create', [{}])
                print(f"✅ Création d'enregistrement possible (ID: {temp_config})")
                
                # Supprimer l'enregistrement temporaire
                models.execute_kw(database, uid, 'admin', 'res.config.settings', 'unlink', [[temp_config]])
                print("✅ Suppression d'enregistrement possible")
                
            except Exception as e:
                print(f"⚠️ Problème avec la création/suppression: {e}")
            
        except Exception as e:
            print(f"❌ Erreur avec res.config.settings: {e}")
            return False
        
        # Tester l'accès aux champs du modèle
        print("\n🔍 Test des champs du modèle...")
        try:
            fields = models.execute_kw(database, uid, 'admin', 'res.config.settings', 'fields_get', [])
            print(f"✅ Champs du modèle accessibles ({len(fields)} champs)")
            
            # Vérifier s'il y a des champs problématiques
            problematic_fields = []
            for field_name, field_info in fields.items():
                if 'default_value' in field_name or 'help' in field_name:
                    problematic_fields.append(field_name)
            
            if problematic_fields:
                print(f"⚠️ Champs potentiellement problématiques: {problematic_fields}")
            else:
                print("✅ Aucun champ problématique détecté")
                
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des champs: {e}")
            return False
        
        # Tester l'accès au modèle ir.model.fields
        print("\n🔧 Test du modèle ir.model.fields...")
        try:
            field_ids = models.execute_kw(database, uid, 'admin', 'ir.model.fields', 'search', 
                                        [[['model', '=', 'res.config.settings']], {'limit': 5}])
            print(f"✅ Modèle ir.model.fields accessible ({len(field_ids)} champs trouvés)")
            
            if field_ids:
                field_data = models.execute_kw(database, uid, 'admin', 'ir.model.fields', 'read', 
                                             [field_ids], {'fields': ['name', 'ttype', 'model']})
                print("✅ Lecture des champs réussie")
                for field in field_data[:3]:  # Afficher les 3 premiers
                    print(f"   - {field['name']} ({field['ttype']})")
            
        except Exception as e:
            print(f"❌ Erreur avec ir.model.fields: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur XML-RPC générale: {e}")
        return False

def test_web_access(port):
    """Tester l'accès web aux paramètres"""
    print("\n🌐 Test d'accès web aux paramètres...")
    
    try:
        # Test de la page principale
        response = requests.get(f'http://localhost:{port}/web', timeout=10)
        if response.status_code == 200:
            print("✅ Page principale accessible")
        else:
            print(f"❌ Page principale inaccessible: {response.status_code}")
            return False
        
        # Test de la page de paramètres (sans authentification)
        settings_urls = [
            f'http://localhost:{port}/web#action=base.action_res_config_settings',
            f'http://localhost:{port}/web/settings',
            f'http://localhost:{port}/web#menu_id=base.menu_administration'
        ]
        
        for url in settings_urls:
            try:
                response = requests.get(url, timeout=10)
                print(f"✅ URL accessible: {url} (Status: {response.status_code})")
            except Exception as e:
                print(f"⚠️ URL problématique: {url} - {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test web: {e}")
        return False

def check_module_status(port, database):
    """Vérifier le statut du module web_studio_community"""
    print("\n📦 Vérification du statut du module...")
    
    try:
        common = xmlrpc.client.ServerProxy(f'http://localhost:{port}/xmlrpc/2/common')
        uid = common.authenticate(database, 'admin', 'admin', {})
        
        if not uid:
            print("❌ Impossible de s'authentifier")
            return False
        
        models = xmlrpc.client.ServerProxy(f'http://localhost:{port}/xmlrpc/2/object')
        
        # Chercher le module web_studio_community
        module_ids = models.execute_kw(database, uid, 'admin', 'ir.module.module', 'search', 
                                     [[['name', '=', 'web_studio_community']]])
        
        if module_ids:
            module_data = models.execute_kw(database, uid, 'admin', 'ir.module.module', 'read', 
                                          [module_ids], {'fields': ['name', 'state', 'installed_version']})
            
            module = module_data[0]
            print(f"✅ Module trouvé: {module['name']}")
            print(f"   État: {module['state']}")
            print(f"   Version: {module.get('installed_version', 'N/A')}")
            
            if module['state'] != 'installed':
                print(f"⚠️ Le module n'est pas installé (état: {module['state']})")
                return False
            
        else:
            print("❌ Module web_studio_community non trouvé")
            return False
        
        # Vérifier les menus créés par le module
        menu_ids = models.execute_kw(database, uid, 'admin', 'ir.ui.menu', 'search', 
                                   [[['name', '=', 'Studio']]])
        
        if menu_ids:
            print("✅ Menu Studio trouvé")
        else:
            print("⚠️ Menu Studio non trouvé")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification du module: {e}")
        return False

def main():
    """Fonction principale de diagnostic"""
    # Démarrer Odoo
    process, port, database = start_odoo_for_diagnosis()
    
    if not process:
        print("❌ Impossible de démarrer Odoo pour le diagnostic")
        return False
    
    try:
        # Attendre que Odoo soit complètement prêt
        print("⏳ Attente de la stabilisation d'Odoo...")
        time.sleep(10)
        
        # Tests de diagnostic
        tests = [
            ("Accès XML-RPC", lambda: test_xmlrpc_access(port, database)),
            ("Statut du module", lambda: check_module_status(port, database)),
            ("Accès web", lambda: test_web_access(port))
        ]
        
        results = []
        
        for test_name, test_func in tests:
            print(f"\n{'='*50}")
            print(f"🔍 {test_name}")
            print(f"{'='*50}")
            
            try:
                result = test_func()
                results.append((test_name, result))
                if result:
                    print(f"\n✅ {test_name}: RÉUSSI")
                else:
                    print(f"\n❌ {test_name}: ÉCHEC")
            except Exception as e:
                print(f"\n❌ {test_name}: ERREUR - {e}")
                results.append((test_name, False))
        
        # Résumé
        print(f"\n{'='*50}")
        print("📊 RÉSUMÉ DU DIAGNOSTIC")
        print(f"{'='*50}")
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ RÉUSSI" if result else "❌ ÉCHEC"
            print(f"{test_name:.<30} {status}")
        
        print(f"\nRésultat global: {passed}/{total} tests réussis")
        
        if passed == total:
            print("\n🎉 DIAGNOSTIC RÉUSSI!")
            print("Le problème ne semble pas venir du module.")
            print("Vérifiez les permissions utilisateur et l'accès aux menus.")
        else:
            print("\n⚠️ PROBLÈMES DÉTECTÉS")
            print("Des corrections sont nécessaires.")
        
        return passed == total
    
    finally:
        # Arrêter Odoo
        print(f"\n🛑 Arrêt d'Odoo...")
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)