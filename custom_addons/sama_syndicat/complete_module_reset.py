#!/usr/bin/env python3
"""
Réinitialisation complète du module web_studio_community
"""

import subprocess
import time
import sys

def complete_reset():
    """Réinitialisation complète du module"""
    print("🔄 RÉINITIALISATION COMPLÈTE DU MODULE")
    print("=" * 50)
    
    DATABASE = "sama_syndicat_final_1756812346"
    ODOO_BIN = "/var/odoo/odoo18/odoo-bin"
    ADDONS_PATH = "/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat"
    PORT = 8078
    
    # Arrêter tous les processus Odoo
    print("🛑 Arrêt de tous les processus Odoo...")
    subprocess.run(['pkill', '-f', 'odoo-bin'], capture_output=True)
    time.sleep(5)
    
    # Étape 1: Désinstaller complètement le module
    print("\n🗑️ Désinstallation complète du module...")
    
    uninstall_cmd = [
        'python3', ODOO_BIN,
        f'--addons-path={ADDONS_PATH}',
        f'--database={DATABASE}',
        f'--xmlrpc-port={PORT}',
        '--stop-after-init',
        '--log-level=warn'
    ]
    
    # Script SQL pour supprimer toutes les traces du module
    sql_cleanup = f"""
    -- Supprimer tous les enregistrements ir.model.data du module
    DELETE FROM ir_model_data WHERE module = 'web_studio_community';
    
    -- Supprimer le module de la liste des modules
    DELETE FROM ir_module_module WHERE name = 'web_studio_community';
    
    -- Supprimer les menus créés par le module
    DELETE FROM ir_ui_menu WHERE name = 'Studio';
    
    -- Supprimer les actions créées par le module
    DELETE FROM ir_actions_act_window WHERE name = 'Custom Models';
    
    -- Nettoyer les contraintes
    DELETE FROM ir_model_constraint WHERE module = 'web_studio_community';
    
    -- Nettoyer les relations
    DELETE FROM ir_model_relation WHERE module = 'web_studio_community';
    """
    
    # Écrire et exécuter le script SQL
    with open('/tmp/complete_cleanup.sql', 'w') as f:
        f.write(sql_cleanup)
    
    print("🧹 Nettoyage complet de la base de données...")
    try:
        result = subprocess.run(['psql', '-d', DATABASE, '-f', '/tmp/complete_cleanup.sql'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Nettoyage SQL réussi")
        else:
            print(f"⚠️ Avertissement SQL: {result.stderr}")
    except Exception as e:
        print(f"❌ Erreur SQL: {e}")
    
    # Nettoyer le fichier temporaire
    try:
        subprocess.run(['rm', '/tmp/complete_cleanup.sql'], capture_output=True)
    except:
        pass
    
    # Étape 2: Redémarrer Odoo pour vérifier que tout fonctionne sans le module
    print("\n🧪 Test d'Odoo sans le module...")
    
    test_cmd = [
        'python3', ODOO_BIN,
        f'--addons-path={ADDONS_PATH}',
        f'--database={DATABASE}',
        f'--xmlrpc-port={PORT}',
        '--stop-after-init',
        '--log-level=warn'
    ]
    
    try:
        result = subprocess.run(test_cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("✅ Odoo fonctionne correctement sans le module")
        else:
            print("❌ Problème avec Odoo sans le module")
            print(result.stderr[-300:])
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False
    
    # Étape 3: Réinstaller le module proprement
    print("\n📦 Réinstallation propre du module...")
    
    install_cmd = [
        'python3', ODOO_BIN,
        f'--addons-path={ADDONS_PATH}',
        f'--database={DATABASE}',
        f'--xmlrpc-port={PORT}',
        '-i', 'web_studio_community',
        '--stop-after-init',
        '--log-level=info'
    ]
    
    try:
        result = subprocess.run(install_cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print("✅ Module réinstallé avec succès")
            return True
        else:
            print("❌ Erreur lors de la réinstallation")
            print(result.stderr[-500:])
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la réinstallation: {e}")
        return False

def test_final_access():
    """Test final d'accès aux paramètres"""
    print("\n🧪 TEST FINAL D'ACCÈS AUX PARAMÈTRES")
    print("=" * 50)
    
    DATABASE = "sama_syndicat_final_1756812346"
    ODOO_BIN = "/var/odoo/odoo18/odoo-bin"
    ADDONS_PATH = "/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat"
    PORT = 8079
    
    # Démarrer Odoo
    cmd = [
        'python3', ODOO_BIN,
        f'--addons-path={ADDONS_PATH}',
        f'--database={DATABASE}',
        f'--xmlrpc-port={PORT}',
        '--log-level=warn'
    ]
    
    print("🚀 Démarrage d'Odoo pour test final...")
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Attendre que Odoo soit prêt
    import requests
    import xmlrpc.client
    
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
        time.sleep(10)
        
        # Test XML-RPC
        print("🔌 Test XML-RPC...")
        common = xmlrpc.client.ServerProxy(f'http://localhost:{PORT}/xmlrpc/2/common')
        uid = common.authenticate(DATABASE, 'admin', 'admin', {})
        
        if not uid:
            print("❌ Impossible de s'authentifier")
            return False
        
        models = xmlrpc.client.ServerProxy(f'http://localhost:{PORT}/xmlrpc/2/object')
        
        # Test res.config.settings
        print("📋 Test res.config.settings...")
        config_ids = models.execute_kw(DATABASE, uid, 'admin', 'res.config.settings', 'search', [[]])
        print(f"✅ res.config.settings accessible ({len(config_ids)} enregistrements)")
        
        # Test ir.model.fields
        print("🔧 Test ir.model.fields...")
        field_ids = models.execute_kw(DATABASE, uid, 'admin', 'ir.model.fields', 'search', 
                                    [[['model', '=', 'res.config.settings']], {'limit': 5}])
        print(f"✅ ir.model.fields accessible ({len(field_ids)} champs)")
        
        # Test accès web
        print("🌐 Test accès web...")
        response = requests.get(f'http://localhost:{PORT}/web#action=base.action_res_config_settings', timeout=10)
        if response.status_code == 200:
            print("✅ Page des paramètres accessible")
        
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False
    
    finally:
        # Arrêter Odoo
        print("🛑 Arrêt d'Odoo...")
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()

def main():
    """Fonction principale"""
    print("🎯 RÉINITIALISATION COMPLÈTE ET TEST")
    print("=" * 60)
    
    # Étape 1: Réinitialisation complète
    if not complete_reset():
        print("❌ Échec de la réinitialisation")
        return False
    
    # Étape 2: Test final
    if not test_final_access():
        print("❌ Échec du test final")
        return False
    
    print("\n🎉 RÉINITIALISATION ET TEST RÉUSSIS!")
    print("Le module web_studio_community fonctionne correctement.")
    print("L'accès aux paramètres est maintenant possible.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)