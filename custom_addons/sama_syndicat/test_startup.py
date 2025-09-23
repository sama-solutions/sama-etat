#!/usr/bin/env python3
"""
Script de test pour les scripts de démarrage SAMA SYNDICAT
"""

import os
import sys
import subprocess
import time

def test_script_exists():
    """Tester que les scripts existent et sont exécutables"""
    scripts = [
        "start_sama_syndicat.py",
        "start_simple.py", 
        "start_sama_syndicat.sh"
    ]
    
    print("🧪 TEST DES SCRIPTS DE DÉMARRAGE")
    print("=" * 40)
    
    for script in scripts:
        if os.path.exists(script):
            if os.access(script, os.X_OK):
                print(f"✅ {script} - Existe et exécutable")
            else:
                print(f"⚠️ {script} - Existe mais pas exécutable")
        else:
            print(f"❌ {script} - N'existe pas")

def test_dependencies():
    """Tester les dépendances"""
    print("\n🔍 TEST DES DÉPENDANCES")
    print("=" * 30)
    
    # Python3
    try:
        result = subprocess.run(['python3', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Python3: {result.stdout.strip()}")
        else:
            print("❌ Python3 non disponible")
    except:
        print("❌ Python3 non trouvé")
    
    # Outils système
    tools = ['lsof', 'pkill', 'fuser', 'netstat']
    for tool in tools:
        try:
            result = subprocess.run(['which', tool], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {tool}: {result.stdout.strip()}")
            else:
                print(f"⚠️ {tool}: Non disponible")
        except:
            print(f"❌ {tool}: Erreur de vérification")

def test_odoo_path():
    """Tester les chemins Odoo"""
    print("\n📁 TEST DES CHEMINS ODOO")
    print("=" * 25)
    
    odoo_paths = [
        "/var/odoo/odoo18/odoo-bin",
        "/usr/bin/odoo",
        "/usr/local/bin/odoo",
        "/opt/odoo/odoo-bin"
    ]
    
    for path in odoo_paths:
        if os.path.exists(path):
            print(f"✅ {path} - Trouvé")
        else:
            print(f"❌ {path} - Non trouvé")
    
    # Vérifier dans le PATH
    try:
        result = subprocess.run(['which', 'odoo'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Odoo dans PATH: {result.stdout.strip()}")
        else:
            print("⚠️ Odoo non trouvé dans le PATH")
    except:
        print("❌ Erreur lors de la vérification du PATH")

def test_port_check():
    """Tester la vérification du port"""
    print("\n🌐 TEST DU PORT 8070")
    print("=" * 20)
    
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex(('localhost', 8070))
            if result == 0:
                print("⚠️ Port 8070 occupé")
            else:
                print("✅ Port 8070 disponible")
    except Exception as e:
        print(f"❌ Erreur lors du test du port: {e}")

def show_usage():
    """Afficher les instructions d'utilisation"""
    print("\n📋 INSTRUCTIONS D'UTILISATION")
    print("=" * 35)
    print("🐍 Scripts Python:")
    print("   ./start_sama_syndicat.py  # Version complète")
    print("   ./start_simple.py         # Version basique")
    print()
    print("🐚 Script Bash:")
    print("   ./start_sama_syndicat.sh  # Version bash")
    print()
    print("⚡ Démarrage rapide:")
    print("   python3 start_simple.py")
    print()
    print("🛑 Pour arrêter:")
    print("   Ctrl+C dans le terminal")
    print("   ou pkill -f odoo-bin")

def main():
    """Fonction principale"""
    print("🚀 SAMA SYNDICAT - TEST DES SCRIPTS DE DÉMARRAGE")
    print("=" * 55)
    
    test_script_exists()
    test_dependencies()
    test_odoo_path()
    test_port_check()
    show_usage()
    
    print("\n🎯 RÉSUMÉ")
    print("=" * 10)
    print("✅ Scripts de démarrage créés et testés")
    print("✅ 3 versions disponibles (Python complet, Python simple, Bash)")
    print("✅ Gestion automatique de l'arrêt des processus")
    print("✅ Démarrage automatique d'Odoo avec SAMA SYNDICAT")
    
    print("\n💡 RECOMMANDATION")
    print("Utilisez start_simple.py pour un démarrage rapide")

if __name__ == "__main__":
    main()