#!/usr/bin/env python3
"""
Script de vérification de l'intégrité de la sauvegarde SAMA SYNDICAT V1.2
"""

import os
from pathlib import Path

def verify_backup():
    """Vérifier l'intégrité de la sauvegarde"""
    
    print("🔍 VÉRIFICATION DE LA SAUVEGARDE SAMA SYNDICAT V1.2")
    print("=" * 60)
    
    backup_path = Path(__file__).parent
    errors = []
    warnings = []
    
    # Fichiers essentiels
    essential_files = [
        '__manifest__.py',
        '__init__.py',
        'BACKUP_INFO.md',
        'README.md',
        'RESTORE.py'
    ]
    
    print("📋 Vérification des fichiers essentiels...")
    for file in essential_files:
        file_path = backup_path / file
        if file_path.exists():
            print(f"  ✅ {file}")
        else:
            errors.append(f"Fichier manquant: {file}")
            print(f"  ❌ {file}")
    
    # Répertoires requis
    required_dirs = [
        'models',
        'views', 
        'controllers',
        'static/src/css',
        'data',
        'security',
        'scripts',
        'documentation'
    ]
    
    print("\n📁 Vérification des répertoires...")
    for directory in required_dirs:
        dir_path = backup_path / directory
        if dir_path.exists():
            print(f"  ✅ {directory}/")
        else:
            errors.append(f"Répertoire manquant: {directory}")
            print(f"  ❌ {directory}/")
    
    # Modèles Python
    model_files = [
        'models/__init__.py',
        'models/syndicat_adherent.py',
        'models/syndicat_assemblee.py',
        'models/syndicat_action.py',
        'models/syndicat_communication.py',
        'models/syndicat_convention.py',
        'models/syndicat_dashboard.py',
        'models/syndicat_formation.py',
        'models/syndicat_mediation.py',
        'models/syndicat_revendication.py',
        'models/res_partner.py'
    ]
    
    print("\n🐍 Vérification des modèles Python...")
    for model in model_files:
        model_path = backup_path / model
        if model_path.exists():
            print(f"  ✅ {model}")
        else:
            errors.append(f"Modèle manquant: {model}")
            print(f"  ❌ {model}")
    
    # Vues XML
    view_files = [
        'views/menus.xml',
        'views/syndicat_adherent_views.xml',
        'views/syndicat_assemblee_views.xml',
        'views/syndicat_action_views.xml',
        'views/syndicat_communication_views.xml',
        'views/syndicat_convention_views.xml',
        'views/syndicat_dashboard_views.xml',
        'views/syndicat_formation_views.xml',
        'views/syndicat_mediation_views.xml',
        'views/syndicat_revendication_views.xml',
        'views/website/website_templates.xml'
    ]
    
    print("\n📄 Vérification des vues XML...")
    for view in view_files:
        view_path = backup_path / view
        if view_path.exists():
            print(f"  ✅ {view}")
        else:
            warnings.append(f"Vue manquante: {view}")
            print(f"  ⚠️ {view}")
    
    # Contrôleurs
    controller_files = [
        'controllers/__init__.py',
        'controllers/main.py',
        'controllers/portal.py'
    ]
    
    print("\n🎮 Vérification des contrôleurs...")
    for controller in controller_files:
        controller_path = backup_path / controller
        if controller_path.exists():
            print(f"  ✅ {controller}")
        else:
            errors.append(f"Contrôleur manquant: {controller}")
            print(f"  ❌ {controller}")
    
    # CSS
    css_files = [
        'static/src/css/dashboard.css',
        'static/src/css/website.css'
    ]
    
    print("\n🎨 Vérification des fichiers CSS...")
    for css in css_files:
        css_path = backup_path / css
        if css_path.exists():
            print(f"  ✅ {css}")
        else:
            warnings.append(f"CSS manquant: {css}")
            print(f"  ⚠️ {css}")
    
    # Données et sécurité
    data_files = [
        'data/data.xml',
        'data/sequences.xml',
        'security/security.xml',
        'security/ir.model.access.csv'
    ]
    
    print("\n🔒 Vérification des données et sécurité...")
    for data_file in data_files:
        data_path = backup_path / data_file
        if data_path.exists():
            print(f"  ✅ {data_file}")
        else:
            warnings.append(f"Fichier de données manquant: {data_file}")
            print(f"  ⚠️ {data_file}")
    
    # Scripts utilitaires
    script_files = [
        'scripts/install_module.py',
        'scripts/update_module.py',
        'scripts/restart_server.py',
        'scripts/validate_corrections.py'
    ]
    
    print("\n🔧 Vérification des scripts...")
    for script in script_files:
        script_path = backup_path / script
        if script_path.exists():
            print(f"  ✅ {script}")
        else:
            warnings.append(f"Script manquant: {script}")
            print(f"  ⚠️ {script}")
    
    # Documentation
    doc_files = [
        'documentation/README.md',
        'documentation/INSTALLATION.md',
        'documentation/RAPPORT_FINAL_ROUTES.md',
        'documentation/DIAGNOSTIC_500_FINAL.md'
    ]
    
    print("\n📚 Vérification de la documentation...")
    for doc in doc_files:
        doc_path = backup_path / doc
        if doc_path.exists():
            print(f"  ✅ {doc}")
        else:
            warnings.append(f"Documentation manquante: {doc}")
            print(f"  ⚠️ {doc}")
    
    # Calcul des statistiques
    total_files = 0
    for root, dirs, files in os.walk(backup_path):
        total_files += len(files)
    
    print(f"\n📊 STATISTIQUES DE LA SAUVEGARDE")
    print(f"  📁 Fichiers totaux: {total_files}")
    print(f"  ✅ Erreurs: {len(errors)}")
    print(f"  ⚠️ Avertissements: {len(warnings)}")
    
    # Résumé final
    print(f"\n🎯 RÉSULTAT DE LA VÉRIFICATION")
    
    if not errors:
        print("✅ SAUVEGARDE INTÈGRE - Tous les fichiers essentiels sont présents")
        if warnings:
            print(f"⚠️ {len(warnings)} avertissements (fichiers optionnels manquants)")
        else:
            print("🏆 SAUVEGARDE PARFAITE - Aucun problème détecté")
        return True
    else:
        print(f"❌ SAUVEGARDE INCOMPLÈTE - {len(errors)} erreurs critiques")
        print("\nErreurs critiques:")
        for error in errors:
            print(f"  ❌ {error}")
        return False

if __name__ == "__main__":
    success = verify_backup()
    exit(0 if success else 1)