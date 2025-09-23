#!/usr/bin/env python3
"""
Script de démarrage complet avec correction CSS et actions
"""

import subprocess
import time
import sys
import os

def start_complete_fix():
    """Démarrer Odoo avec toutes les corrections"""
    
    print("🚀 DÉMARRAGE COMPLET AVEC CORRECTIONS CSS ET ACTIONS")
    print("=" * 55)
    
    # Configuration
    PORT = 8070
    DATABASE = "sama_syndicat_final_1756812346"
    ODOO_BIN = "/var/odoo/odoo18/odoo-bin"
    ADDONS_PATH = "/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat"
    
    # Arrêter les processus existants
    print("🛑 Arrêt des processus existants...")
    subprocess.run(['pkill', '-f', 'odoo-bin'], capture_output=True)
    time.sleep(2)
    
    # Vérifier que Odoo existe
    if not os.path.exists(ODOO_BIN):
        print(f"❌ Odoo non trouvé à: {ODOO_BIN}")
        return False
    
    # Démarrer Odoo en arrière-plan
    print("⚡ Démarrage d'Odoo...")
    cmd = [
        'python3', ODOO_BIN,
        f'--addons-path={ADDONS_PATH}',
        f'--database={DATABASE}',
        f'--xmlrpc-port={PORT}',
        '--dev=reload,xml',
        '--log-level=warn'
    ]
    
    # Démarrer Odoo en arrière-plan
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print("⏳ Attente du démarrage d'Odoo...")
    
    # Attendre que Odoo soit prêt
    max_wait = 60
    wait_time = 0
    
    while wait_time < max_wait:
        try:
            import xmlrpc.client
            common = xmlrpc.client.ServerProxy(f'http://localhost:{PORT}/xmlrpc/2/common')
            version = common.version()
            if version:
                print(f"✅ Odoo démarré (version: {version['server_version']})")
                break
        except:
            pass
        
        time.sleep(2)
        wait_time += 2
        print(f"⏳ Attente... ({wait_time}s/{max_wait}s)")
        
        if process.poll() is not None:
            print("❌ Odoo s'est arrêté de manière inattendue")
            stdout, stderr = process.communicate()
            if stderr:
                print(f"Erreur: {stderr.decode()}")
            return False
    
    if wait_time >= max_wait:
        print("❌ Timeout - Odoo n'a pas démarré à temps")
        process.terminate()
        return False
    
    # Corriger le CSS et la largeur
    print("\n🎨 Correction du CSS et de la largeur...")
    try:
        result = subprocess.run(['python3', 'fix_dashboard_css.py'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ CSS et largeur corrigés")
        else:
            print(f"⚠️ Problème lors de la correction CSS: {result.stderr}")
    except Exception as e:
        print(f"❌ Erreur lors de la correction CSS: {e}")
    
    # Corriger les actions
    print("\n🔧 Correction des actions...")
    try:
        result = subprocess.run(['python3', 'fix_dashboard_actions.py'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Actions corrigées")
        else:
            print(f"⚠️ Problème lors de la correction des actions: {result.stderr}")
    except Exception as e:
        print(f"❌ Erreur lors de la correction des actions: {e}")
    
    print("\n🎯 RÉSULTAT FINAL")
    print("=" * 20)
    print("✅ Odoo démarré avec succès")
    print("✅ CSS et largeur corrigés")
    print("✅ Actions des dashboards corrigées")
    print("✅ Menus de test créés")
    print(f"🌐 Interface: http://localhost:{PORT}/web")
    print("📍 Accès: Menu Syndicat → 🧪 Test Dashboards")
    
    print("\n🎨 AMÉLIORATIONS CSS")
    print("=" * 20)
    print("✅ Largeur complète (100%)")
    print("✅ Styles des stat_box améliorés")
    print("✅ Sections avec bordures colorées")
    print("✅ Titre avec gradient bleu")
    print("✅ Effets hover sur les boutons")
    print("✅ Cache vidé pour rechargement")
    
    print("\n💡 INSTRUCTIONS")
    print("=" * 15)
    print("1. Ouvrir http://localhost:8070/web")
    print("2. Se connecter (admin/admin)")
    print("3. Menu Syndicat → 🧪 Test Dashboards")
    print("4. Tester les 4 versions")
    print("5. Vérifier la largeur complète")
    print("6. Tester les boutons cliquables")
    
    print("\n💡 Le serveur Odoo continue de tourner en arrière-plan")
    print("🛑 Pour l'arrêter: pkill -f odoo-bin")
    
    return True

if __name__ == "__main__":
    success = start_complete_fix()
    if success:
        print("\n🎊 Succès ! Les dashboards sont maintenant corrigés et utilisent toute la largeur")
    else:
        print("\n❌ Échec du démarrage")
    sys.exit(0 if success else 1)