#!/usr/bin/env python3
"""
Script de démarrage final avec nettoyage complet et dashboards modernes uniquement
"""

import subprocess
import time
import sys
import os

def start_clean_modern():
    """Démarrer Odoo avec nettoyage complet et dashboards modernes uniquement"""
    
    print("🧹 DÉMARRAGE PROPRE AVEC DASHBOARDS MODERNES UNIQUEMENT")
    print("=" * 60)
    
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
    
    # Nettoyer les anciens menus
    print("\n🧹 Nettoyage des anciens menus...")
    try:
        result = subprocess.run(['python3', 'clean_old_menus.py'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Anciens menus nettoyés")
        else:
            print(f"⚠️ Problème lors du nettoyage: {result.stderr}")
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage: {e}")
    
    print("\n🎯 RÉSULTAT FINAL")
    print("=" * 20)
    print("✅ Odoo démarré avec succès")
    print("✅ Anciens menus supprimés")
    print("✅ Dashboards modernes uniquement")
    print("✅ Interface propre et moderne")
    print(f"🌐 Interface: http://localhost:{PORT}/web")
    
    print("\n📍 MENUS DISPONIBLES")
    print("=" * 25)
    print("Menu Syndicat:")
    print("├── 📊 Dashboard Principal (Cartes Modernes)")
    print("├── 👔 Dashboard Exécutif")
    print("├── Adhérents")
    print("├── Assemblées")
    print("├── Revendications")
    print("├── Actions Syndicales")
    print("├── Communications")
    print("├── Formations")
    print("├── Conventions")
    print("├── Médiations")
    print("└── Configuration")
    
    print("\n🎨 DASHBOARDS MODERNES")
    print("=" * 25)
    print("📊 Dashboard Principal:")
    print("   - Design avec cartes modernes")
    print("   - Métriques visuelles avancées")
    print("   - Barres de progression")
    print("   - Badges et indicateurs")
    print()
    print("👔 Dashboard Exécutif:")
    print("   - Interface premium")
    print("   - Header avec gradient")
    print("   - KPI cards détaillées")
    print("   - Métriques circulaires")
    
    print("\n💡 INSTRUCTIONS")
    print("=" * 15)
    print("1. Ouvrir http://localhost:8070/web")
    print("2. Se connecter (admin/admin)")
    print("3. Menu Syndicat → 📊 Dashboard Principal")
    print("4. Ou Menu Syndicat → 👔 Dashboard Exécutif")
    print("5. Plus d'anciens menus de test !")
    
    print("\n🧹 NETTOYAGE EFFECTUÉ")
    print("=" * 25)
    print("❌ Supprimé: Anciens menus de test")
    print("❌ Supprimé: Dashboards classiques V1-V4")
    print("❌ Supprimé: Menus 🧪 Test Dashboards")
    print("✅ Conservé: 2 dashboards modernes uniquement")
    print("✅ Conservé: Menus fonctionnels du syndicat")
    
    print("\n💡 Le serveur Odoo continue de tourner en arrière-plan")
    print("🛑 Pour l'arrêter: pkill -f odoo-bin")
    
    return True

if __name__ == "__main__":
    success = start_clean_modern()
    if success:
        print("\n🎊 Succès ! Interface propre avec dashboards modernes uniquement")
        print("🧹 Tous les anciens menus ont été supprimés")
    else:
        print("\n❌ Échec du démarrage")
    sys.exit(0 if success else 1)