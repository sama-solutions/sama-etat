#!/usr/bin/env python3
"""
Script rapide pour vérifier l'état des menus dashboards
"""

import subprocess
import sys

def check_menus_status():
    """Vérifier l'état des menus"""
    
    print("🔍 VÉRIFICATION RAPIDE DES MENUS")
    print("=" * 40)
    
    # Vérifier si Odoo est démarré
    try:
        result = subprocess.run(['lsof', '-i', ':8070'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout:
            print("✅ Odoo semble démarré sur le port 8070")
            odoo_running = True
        else:
            print("❌ Odoo ne semble pas démarré sur le port 8070")
            odoo_running = False
    except:
        print("⚠️ Impossible de vérifier l'état du port 8070")
        odoo_running = False
    
    # Vérifier les fichiers de menu
    print("\n📁 Vérification des fichiers...")
    
    files_to_check = [
        'views/dashboard_test_menus.xml',
        'views/dashboard_actions.xml',
        'views/dashboard_v1_native_odoo.xml',
        'views/dashboard_v2_compact.xml',
        'views/dashboard_v3_graphiques.xml',
        'views/dashboard_v4_minimal.xml'
    ]
    
    for file in files_to_check:
        try:
            with open(file, 'r') as f:
                content = f.read()
                if 'action_syndicat_dashboard_v' in content:
                    print(f"✅ {file} - Contient les actions dashboard")
                else:
                    print(f"⚠️ {file} - Pas d'actions dashboard trouvées")
        except FileNotFoundError:
            print(f"❌ {file} - Fichier non trouvé")
        except Exception as e:
            print(f"❌ {file} - Erreur: {e}")
    
    # Vérifier le manifeste
    print("\n📋 Vérification du manifeste...")
    try:
        with open('__manifest__.py', 'r') as f:
            manifest = f.read()
            if 'dashboard_test_menus.xml' in manifest:
                print("✅ dashboard_test_menus.xml dans le manifeste")
            else:
                print("❌ dashboard_test_menus.xml manquant dans le manifeste")
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du manifeste: {e}")
    
    # Recommandations
    print("\n💡 RECOMMANDATIONS")
    print("=" * 20)
    
    if not odoo_running:
        print("🚀 Démarrer Odoo avec correction automatique:")
        print("   python3 start_and_fix_menus.py")
    else:
        print("🔧 Corriger les menus (Odoo déjà démarré):")
        print("   python3 fix_menus_simple.py")
    
    print("\n📍 Accès aux dashboards:")
    print("   Menu Syndicat → 🧪 Test Dashboards")
    
    print("\n🔗 Accès direct (si menus absents):")
    print("   http://localhost:8070/web#action=action_syndicat_dashboard_v1")
    print("   http://localhost:8070/web#action=action_syndicat_dashboard_v2")
    print("   http://localhost:8070/web#action=action_syndicat_dashboard_v3")
    print("   http://localhost:8070/web#action=action_syndicat_dashboard_v4")

if __name__ == "__main__":
    check_menus_status()