#!/usr/bin/env python3
"""
Création d'une nouvelle base de données propre pour tester web_studio_community
"""

import subprocess
import time
import sys
import requests
import xmlrpc.client

def create_fresh_database():
    """Créer une nouvelle base de données propre"""
    print("🆕 CRÉATION D'UNE NOUVELLE BASE DE DONNÉES PROPRE")
    print("=" * 60)
    
    # Configuration
    NEW_DATABASE = "test_web_studio_fresh"
    ODOO_BIN = "/var/odoo/odoo18/odoo-bin"
    ADDONS_PATH = "/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat"
    PORT = 8080
    
    # Arrêter tous les processus Odoo
    print("🛑 Arrêt de tous les processus Odoo...")
    subprocess.run(['pkill', '-f', 'odoo-bin'], capture_output=True)
    time.sleep(3)
    
    # Supprimer la base de données si elle existe
    print("🗑️ Suppression de l'ancienne base de données de test...")
    try:
        subprocess.run(['dropdb', NEW_DATABASE], capture_output=True)
        print("✅ Ancienne base supprimée")
    except:
        print("ℹ️ Aucune ancienne base à supprimer")
    
    # Créer une nouvelle base de données avec les modules de base
    print("🆕 Création d'une nouvelle base de données...")
    
    create_cmd = [
        'python3', ODOO_BIN,
        f'--addons-path={ADDONS_PATH}',
        f'--database={NEW_DATABASE}',
        f'--xmlrpc-port={PORT}',
        '--init=base',
        '--stop-after-init',
        '--log-level=warn',
        '--without-demo=all'
    ]
    
    try:
        result = subprocess.run(create_cmd, capture_output=True, text=True, timeout=180)
        if result.returncode == 0:
            print("✅ Nouvelle base de données créée avec succès")
        else:
            print("❌ Erreur lors de la création de la base")
            print(result.stderr[-500:])
            return False
    except subprocess.TimeoutExpired:
        print("⏰ Timeout lors de la création de la base")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    # Installer web_studio_community sur la nouvelle base
    print("\n📦 Installation de web_studio_community...")
    
    install_cmd = [
        'python3', ODOO_BIN,
        f'--addons-path={ADDONS_PATH}',
        f'--database={NEW_DATABASE}',
        f'--xmlrpc-port={PORT}',
        '-i', 'web_studio_community',
        '--stop-after-init',
        '--log-level=info'
    ]
    
    try:
        result = subprocess.run(install_cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print("✅ Module web_studio_community installé avec succès")
        else:
            print("❌ Erreur lors de l'installation du module")
            print(result.stderr[-500:])
            return False
    except Exception as e:
        print(f"❌ Erreur lors de l'installation: {e}")
        return False
    
    return NEW_DATABASE

def test_fresh_database(database):
    """Tester la nouvelle base de données"""
    print(f"\n🧪 TEST DE LA NOUVELLE BASE DE DONNÉES: {database}")
    print("=" * 60)
    
    ODOO_BIN = "/var/odoo/odoo18/odoo-bin"
    ADDONS_PATH = "/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat"
    PORT = 8081
    
    # Démarrer Odoo avec la nouvelle base
    cmd = [
        'python3', ODOO_BIN,
        f'--addons-path={ADDONS_PATH}',
        f'--database={database}',
        f'--xmlrpc-port={PORT}',
        '--log-level=warn'
    ]
    
    print("🚀 Démarrage d'Odoo avec la nouvelle base...")
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Attendre que Odoo soit prêt
    max_wait = 60
    wait_time = 0
    
    while wait_time < max_wait:
        try:
            response = requests.get(f'http://localhost:{PORT}/web', timeout=5)
            if response.status_code == 200:
                print(f"✅ Odoo démarré sur le port {PORT}")
                break
        except:
            pass
        
        time.sleep(2)
        wait_time += 2
        
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print("❌ Odoo s'est arrêté de manière inattendue")
            print(f"Erreur: {stderr.decode()[-500:]}")
            return False
    
    if wait_time >= max_wait:
        print("❌ Timeout - Odoo n'a pas démarré à temps")
        process.terminate()
        return False
    
    try:
        # Attendre stabilisation
        print("⏳ Attente de la stabilisation...")
        time.sleep(10)
        
        # Test XML-RPC
        print("🔌 Test XML-RPC...")
        common = xmlrpc.client.ServerProxy(f'http://localhost:{PORT}/xmlrpc/2/common')
        uid = common.authenticate(database, 'admin', 'admin', {})
        
        if not uid:
            print("❌ Impossible de s'authentifier")
            return False
        
        print(f"✅ Authentification réussie (UID: {uid})")
        
        models = xmlrpc.client.ServerProxy(f'http://localhost:{PORT}/xmlrpc/2/object')
        
        # Test res.config.settings
        print("\n📋 Test res.config.settings...")
        try:
            config_ids = models.execute_kw(database, uid, 'admin', 'res.config.settings', 'search', [[]])
            print(f"✅ res.config.settings accessible ({len(config_ids)} enregistrements)")
            
            # Test fields_get
            fields = models.execute_kw(database, uid, 'admin', 'res.config.settings', 'fields_get', [])
            print(f"✅ Champs accessibles ({len(fields)} champs)")
            
        except Exception as e:
            print(f"❌ Erreur avec res.config.settings: {e}")
            return False
        
        # Test ir.model.fields
        print("\n🔧 Test ir.model.fields...")
        try:
            field_ids = models.execute_kw(database, uid, 'admin', 'ir.model.fields', 'search', 
                                        [[['model', '=', 'res.config.settings']], {'limit': 5}])
            print(f"✅ ir.model.fields accessible ({len(field_ids)} champs)")
            
            if field_ids:
                field_data = models.execute_kw(database, uid, 'admin', 'ir.model.fields', 'read', 
                                             [field_ids], {'fields': ['name', 'ttype']})
                print("✅ Lecture des champs réussie")
                for field in field_data[:3]:
                    print(f"   - {field['name']} ({field['ttype']})")
            
        except Exception as e:
            print(f"❌ Erreur avec ir.model.fields: {e}")
            return False
        
        # Test du module web_studio_community
        print("\n📦 Test du module web_studio_community...")
        try:
            module_ids = models.execute_kw(database, uid, 'admin', 'ir.module.module', 'search', 
                                         [[['name', '=', 'web_studio_community']]])
            
            if module_ids:
                module_data = models.execute_kw(database, uid, 'admin', 'ir.module.module', 'read', 
                                              [module_ids], {'fields': ['name', 'state']})
                module = module_data[0]
                print(f"✅ Module trouvé: {module['name']} (état: {module['state']})")
            else:
                print("❌ Module web_studio_community non trouvé")
                return False
            
        except Exception as e:
            print(f"❌ Erreur avec le module: {e}")
            return False
        
        # Test accès web
        print("\n🌐 Test accès web...")
        try:
            response = requests.get(f'http://localhost:{PORT}/web#action=base.action_res_config_settings', timeout=10)
            if response.status_code == 200:
                print("✅ Page des paramètres accessible")
            else:
                print(f"❌ Page des paramètres inaccessible: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erreur accès web: {e}")
            return False
        
        print("\n🎉 TOUS LES TESTS RÉUSSIS SUR LA NOUVELLE BASE!")
        print(f"La base de données {database} fonctionne parfaitement.")
        return True
        
    except Exception as e:
        print(f"❌ Erreur générale lors du test: {e}")
        return False
    
    finally:
        # Arrêter Odoo
        print("\n🛑 Arrêt d'Odoo...")
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()

def main():
    """Fonction principale"""
    print("🎯 CRÉATION ET TEST D'UNE BASE DE DONNÉES PROPRE")
    print("=" * 70)
    
    # Étape 1: Créer une nouvelle base de données
    new_database = create_fresh_database()
    if not new_database:
        print("❌ Échec de la création de la nouvelle base")
        return False
    
    # Étape 2: Tester la nouvelle base
    if not test_fresh_database(new_database):
        print("❌ Échec du test de la nouvelle base")
        return False
    
    print("\n🎉 SUCCÈS COMPLET!")
    print(f"La nouvelle base de données '{new_database}' fonctionne parfaitement.")
    print("Le module web_studio_community est opérationnel.")
    print("\n📋 Pour utiliser cette base:")
    print(f"   python3 start_odoo_final_optimized.py")
    print(f"   (Modifiez DATABASE = '{new_database}' dans le script)")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)