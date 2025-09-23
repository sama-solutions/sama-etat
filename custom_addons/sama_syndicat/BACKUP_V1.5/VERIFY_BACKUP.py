#!/usr/bin/env python3
"""
Script de vérification de l'intégrité du backup SAMA SYNDICAT V1.5
"""

import os
import sys
from pathlib import Path

def verify_backup():
    """Vérifie l'intégrité du backup V1.5"""
    
    print("🔍 VÉRIFICATION BACKUP SAMA SYNDICAT V1.5")
    print("=" * 45)
    
    backup_dir = Path(__file__).parent
    print(f"📁 Répertoire de backup: {backup_dir}")
    
    # Structure attendue
    expected_structure = {
        'models': {
            'type': 'dir',
            'files': [
                '__init__.py',
                'syndicat_adherent.py',
                'syndicat_assemblee.py',
                'syndicat_revendication.py',
                'syndicat_action.py',
                'syndicat_communication.py',
                'syndicat_formation.py',
                'syndicat_convention.py',
                'syndicat_mediation.py',
                'syndicat_dashboard.py',
                'res_partner.py'
            ]
        },
        'views': {
            'type': 'dir',
            'files': [
                'menus.xml',
                'dashboard_modern_cards.xml',
                'dashboard_executive.xml',
                'dashboard_modern_menus.xml',
                'dashboard_v1_native_odoo.xml',
                'dashboard_v2_compact.xml',
                'dashboard_v3_graphiques.xml',
                'dashboard_v4_minimal.xml',
                'dashboard_actions.xml',
                'syndicat_adherent_views.xml',
                'syndicat_assemblee_views.xml',
                'syndicat_revendication_views.xml',
                'syndicat_action_views.xml',
                'syndicat_communication_views.xml',
                'syndicat_formation_views.xml',
                'syndicat_convention_views.xml',
                'syndicat_mediation_views.xml',
                'syndicat_dashboard_views.xml'
            ],
            'subdirs': ['website']
        },
        'static': {
            'type': 'dir',
            'subdirs': ['src', 'description']
        },
        'scripts': {
            'type': 'dir',
            'files': [
                'start_modern_dashboards.py',
                'start_clean_modern.py',
                'restart_clean_final.py',
                'apply_final_corrections.py',
                'clean_old_menus.py',
                'force_menu_update.py'
            ]
        },
        'documentation': {
            'type': 'dir',
            'files': [
                'DASHBOARDS_MODERNES.md',
                'CORRECTIONS_FINALES.md',
                'NETTOYAGE_MENUS.md',
                'README.md'
            ]
        },
        'security': {'type': 'dir'},
        'data': {'type': 'dir'},
        'controllers': {'type': 'dir'}
    }
    
    # Fichiers racine attendus
    expected_root_files = [
        '__manifest__.py',
        '__init__.py',
        'VERSION_1.5_CHANGELOG.md',
        'README_V1.5.md',
        'RESTORE_V1.5.sh',
        'VERIFY_BACKUP.py'
    ]
    
    errors = []
    warnings = []
    success_count = 0
    total_checks = 0
    
    print("\n📋 VÉRIFICATION DE LA STRUCTURE")
    print("-" * 35)
    
    # Vérifier les fichiers racine
    for file_name in expected_root_files:
        total_checks += 1
        file_path = backup_dir / file_name
        if file_path.exists():
            print(f"✅ {file_name}")
            success_count += 1
        else:
            print(f"❌ {file_name} - MANQUANT")
            errors.append(f"Fichier manquant: {file_name}")
    
    # Vérifier la structure des dossiers
    for dir_name, config in expected_structure.items():
        total_checks += 1
        dir_path = backup_dir / dir_name
        
        if not dir_path.exists():
            print(f"❌ {dir_name}/ - DOSSIER MANQUANT")
            errors.append(f"Dossier manquant: {dir_name}")
            continue
        
        if not dir_path.is_dir():
            print(f"❌ {dir_name} - N'EST PAS UN DOSSIER")
            errors.append(f"N'est pas un dossier: {dir_name}")
            continue
        
        print(f"✅ {dir_name}/")
        success_count += 1
        
        # Vérifier les fichiers dans le dossier
        if 'files' in config:
            for file_name in config['files']:
                total_checks += 1
                file_path = dir_path / file_name
                if file_path.exists():
                    print(f"  ✅ {file_name}")
                    success_count += 1
                else:
                    print(f"  ❌ {file_name} - MANQUANT")
                    errors.append(f"Fichier manquant: {dir_name}/{file_name}")
        
        # Vérifier les sous-dossiers
        if 'subdirs' in config:
            for subdir_name in config['subdirs']:
                total_checks += 1
                subdir_path = dir_path / subdir_name
                if subdir_path.exists() and subdir_path.is_dir():
                    print(f"  ✅ {subdir_name}/")
                    success_count += 1
                else:
                    print(f"  ❌ {subdir_name}/ - MANQUANT")
                    errors.append(f"Sous-dossier manquant: {dir_name}/{subdir_name}")
    
    # Vérifications spéciales
    print("\n🔍 VÉRIFICATIONS SPÉCIALES")
    print("-" * 30)
    
    # Vérifier le CSS moderne
    css_modern = backup_dir / 'static' / 'src' / 'css' / 'dashboard_modern.css'
    total_checks += 1
    if css_modern.exists():
        size = css_modern.stat().st_size
        if size > 10000:  # Plus de 10KB
            print(f"✅ CSS moderne ({size} bytes)")
            success_count += 1
        else:
            print(f"⚠️ CSS moderne trop petit ({size} bytes)")
            warnings.append(f"CSS moderne petit: {size} bytes")
    else:
        print("❌ CSS moderne manquant")
        errors.append("CSS moderne manquant")
    
    # Vérifier les dashboards modernes
    dashboard_files = [
        'views/dashboard_modern_cards.xml',
        'views/dashboard_executive.xml'
    ]
    
    for dashboard_file in dashboard_files:
        total_checks += 1
        dashboard_path = backup_dir / dashboard_file
        if dashboard_path.exists():
            size = dashboard_path.stat().st_size
            if size > 5000:  # Plus de 5KB
                print(f"✅ {dashboard_file} ({size} bytes)")
                success_count += 1
            else:
                print(f"⚠️ {dashboard_file} trop petit ({size} bytes)")
                warnings.append(f"Dashboard petit: {dashboard_file}")
        else:
            print(f"❌ {dashboard_file} manquant")
            errors.append(f"Dashboard manquant: {dashboard_file}")
    
    # Vérifier les scripts exécutables
    script_files = [
        'RESTORE_V1.5.sh',
        'scripts/start_modern_dashboards.py',
        'scripts/clean_old_menus.py'
    ]
    
    for script_file in script_files:
        total_checks += 1
        script_path = backup_dir / script_file
        if script_path.exists():
            if os.access(script_path, os.X_OK) or script_file.endswith('.py'):
                print(f"✅ {script_file} (exécutable)")
                success_count += 1
            else:
                print(f"⚠️ {script_file} (non exécutable)")
                warnings.append(f"Script non exécutable: {script_file}")
        else:
            print(f"❌ {script_file} manquant")
            errors.append(f"Script manquant: {script_file}")
    
    # Résumé
    print("\n📊 RÉSUMÉ DE LA VÉRIFICATION")
    print("=" * 35)
    
    success_rate = (success_count / total_checks) * 100 if total_checks > 0 else 0
    
    print(f"✅ Succès: {success_count}/{total_checks} ({success_rate:.1f}%)")
    print(f"❌ Erreurs: {len(errors)}")
    print(f"⚠️ Avertissements: {len(warnings)}")
    
    if errors:
        print("\n❌ ERREURS DÉTECTÉES:")
        for error in errors:
            print(f"  - {error}")
    
    if warnings:
        print("\n⚠️ AVERTISSEMENTS:")
        for warning in warnings:
            print(f"  - {warning}")
    
    # Vérification de l'intégrité globale
    print("\n🎯 INTÉGRITÉ GLOBALE")
    print("-" * 25)
    
    if len(errors) == 0:
        if len(warnings) == 0:
            print("🎊 BACKUP PARFAIT - Aucun problème détecté")
            integrity_status = "PARFAIT"
        else:
            print("✅ BACKUP VALIDE - Quelques avertissements mineurs")
            integrity_status = "VALIDE"
    elif len(errors) <= 2:
        print("⚠️ BACKUP UTILISABLE - Quelques erreurs mineures")
        integrity_status = "UTILISABLE"
    else:
        print("❌ BACKUP CORROMPU - Trop d'erreurs")
        integrity_status = "CORROMPU"
    
    # Informations sur la version
    print("\n📋 INFORMATIONS VERSION")
    print("-" * 30)
    print("Version: SAMA SYNDICAT V1.5")
    print("Date: 02 Septembre 2025")
    print("Type: Dashboards Modernes")
    print(f"Intégrité: {integrity_status}")
    print(f"Taille totale: {get_directory_size(backup_dir)} MB")
    
    # Instructions de restauration
    if integrity_status in ["PARFAIT", "VALIDE", "UTILISABLE"]:
        print("\n🚀 INSTRUCTIONS DE RESTAURATION")
        print("-" * 40)
        print("1. Exécuter: ./RESTORE_V1.5.sh")
        print("2. Ou copier manuellement les fichiers")
        print("3. Démarrer avec: python3 scripts/start_modern_dashboards.py")
        print("4. Interface: http://localhost:8070/web")
        print("5. Connexion: admin/admin")
    
    return len(errors) == 0

def get_directory_size(path):
    """Calcule la taille d'un répertoire en MB"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                total_size += os.path.getsize(filepath)
            except OSError:
                pass
    return round(total_size / (1024 * 1024), 2)

if __name__ == "__main__":
    success = verify_backup()
    print(f"\n{'✅ VÉRIFICATION RÉUSSIE' if success else '❌ VÉRIFICATION ÉCHOUÉE'}")
    sys.exit(0 if success else 1)