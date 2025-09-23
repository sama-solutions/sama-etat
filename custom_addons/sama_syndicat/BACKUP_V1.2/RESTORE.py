#!/usr/bin/env python3
"""
Script de restauration automatique pour SAMA SYNDICAT V1.2
Usage: python3 RESTORE.py [destination_path]
"""

import os
import shutil
import sys
import subprocess
from pathlib import Path

def restore_sama_syndicat(destination=None):
    """Restaurer SAMA SYNDICAT V1.2 depuis la sauvegarde"""
    
    print("🔄 RESTAURATION SAMA SYNDICAT V1.2")
    print("=" * 50)
    
    # Déterminer le chemin de destination
    if destination:
        dest_path = Path(destination)
    else:
        dest_path = Path.cwd().parent / "sama_syndicat_restored"
    
    print(f"📁 Destination: {dest_path}")
    
    # Créer le répertoire de destination
    if dest_path.exists():
        response = input(f"⚠️ Le répertoire {dest_path} existe déjà. Écraser ? (y/N): ")
        if response.lower() != 'y':
            print("❌ Restauration annulée")
            return False
        shutil.rmtree(dest_path)
    
    dest_path.mkdir(parents=True, exist_ok=True)
    
    # Copier les fichiers
    backup_path = Path(__file__).parent
    
    print("📋 Copie des fichiers...")
    
    # Fichiers racine
    for file in ['__manifest__.py', '__init__.py']:
        if (backup_path / file).exists():
            shutil.copy2(backup_path / file, dest_path / file)
            print(f"  ✅ {file}")
    
    # Répertoires
    directories = ['models', 'views', 'controllers', 'static', 'data', 'security']
    
    for directory in directories:
        src_dir = backup_path / directory
        dest_dir = dest_path / directory
        
        if src_dir.exists():
            shutil.copytree(src_dir, dest_dir)
            print(f"  ✅ {directory}/")
    
    # Copier la documentation
    doc_dir = dest_path / "documentation"
    doc_dir.mkdir(exist_ok=True)
    
    for doc_file in (backup_path / "documentation").glob("*.md"):
        shutil.copy2(doc_file, doc_dir / doc_file.name)
        print(f"  ✅ documentation/{doc_file.name}")
    
    # Copier les scripts utiles
    script_dir = dest_path / "scripts"
    script_dir.mkdir(exist_ok=True)
    
    useful_scripts = [
        'install_module.py',
        'update_module.py', 
        'restart_server.py',
        'validate_corrections.py'
    ]
    
    for script in useful_scripts:
        script_path = backup_path / "scripts" / script
        if script_path.exists():
            shutil.copy2(script_path, script_dir / script)
            print(f"  ✅ scripts/{script}")
    
    print("\n✅ Restauration terminée avec succès!")
    print(f"📁 Module restauré dans: {dest_path}")
    
    # Instructions post-restauration
    print("\n🚀 PROCHAINES ÉTAPES:")
    print("1. Copier le module dans custom_addons:")
    print(f"   cp -r {dest_path} /chemin/vers/custom_addons/sama_syndicat")
    print("\n2. Installer le module:")
    print("   python3 scripts/install_module.py")
    print("\n3. Redémarrer le serveur:")
    print("   python3 scripts/restart_server.py")
    print("\n4. Tester les routes:")
    print("   curl http://localhost:8070/syndicat/test")
    
    return True

def main():
    """Point d'entrée principal"""
    destination = sys.argv[1] if len(sys.argv) > 1 else None
    
    try:
        success = restore_sama_syndicat(destination)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Erreur lors de la restauration: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()