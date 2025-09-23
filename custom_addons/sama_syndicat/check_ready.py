#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vérification rapide que SAMA SYNDICAT est prêt
"""

import os
import sys

def check_files():
    """Vérifie que tous les fichiers essentiels existent"""
    essential_files = [
        "sama_syndicat/__manifest__.py",
        "sama_syndicat/__init__.py",
        "sama_syndicat/models/__init__.py",
        "sama_syndicat/controllers/__init__.py",
        "sama_syndicat/views/menus.xml",
        "sama_syndicat/security/security.xml",
        "sama_syndicat/security/ir.model.access.csv",
        "sama_syndicat/data/sequences.xml",
        "sama_syndicat/data/data.xml",
        "sama_syndicat/install_and_start.sh",
        "sama_syndicat/launch_sama_syndicat.py"
    ]
    
    missing = []
    for file in essential_files:
        if not os.path.exists(file):
            missing.append(file)
    
    return missing

def check_permissions():
    """Vérifie les permissions des scripts"""
    scripts = [
        "sama_syndicat/install_and_start.sh",
        "sama_syndicat/launch_sama_syndicat.py",
        "sama_syndicat/dev_scripts/final_test.sh",
        "sama_syndicat/dev_scripts/validate_syntax.py"
    ]
    
    non_executable = []
    for script in scripts:
        if os.path.exists(script) and not os.access(script, os.X_OK):
            non_executable.append(script)
    
    return non_executable

def main():
    """Vérification principale"""
    print("🏛️  SAMA SYNDICAT - VÉRIFICATION DE PRÉPARATION")
    print("=" * 50)
    
    # Vérifier les fichiers
    missing_files = check_files()
    if missing_files:
        print("❌ Fichiers manquants:")
        for file in missing_files:
            print(f"  • {file}")
        return False
    else:
        print("✅ Tous les fichiers essentiels présents")
    
    # Vérifier les permissions
    non_exec = check_permissions()
    if non_exec:
        print("⚠️  Scripts non exécutables:")
        for script in non_exec:
            print(f"  • {script}")
        print("Exécutez: chmod +x <script>")
    else:
        print("✅ Permissions des scripts OK")
    
    # Vérifier la syntaxe
    print("🔍 Test de syntaxe rapide...")
    try:
        result = os.system("python3 sama_syndicat/dev_scripts/validate_syntax.py > /dev/null 2>&1")
        if result == 0:
            print("✅ Syntaxe validée")
        else:
            print("❌ Erreurs de syntaxe détectées")
            return False
    except:
        print("⚠️  Impossible de valider la syntaxe")
    
    print("\n" + "=" * 50)
    if not missing_files and not non_exec:
        print("🎉 SAMA SYNDICAT EST PRÊT POUR L'INSTALLATION!")
        print("\n🚀 Pour démarrer:")
        print("   ./sama_syndicat/install_and_start.sh")
        print("   ou")
        print("   python3 sama_syndicat/launch_sama_syndicat.py")
        print("\n🌐 Accès: http://localhost:8070")
        return True
    else:
        print("❌ Des problèmes ont été détectés")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)