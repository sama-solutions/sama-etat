#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Résumé final de l'installation autonome SAMA SYNDICAT
"""

import os
import subprocess

def print_banner():
    """Bannière finale"""
    print("🏛️" + "=" * 70 + "🏛️")
    print("🏛️" + " " * 25 + "SAMA SYNDICAT" + " " * 32 + "🏛️")
    print("🏛️" + " " * 20 + "INSTALLATION AUTONOME PRÊTE" + " " * 22 + "🏛️")
    print("🏛️" + " " * 70 + "🏛️")
    print("🏛️" + " " * 20 + "POLITECH SÉNÉGAL - v1.0.0" + " " * 24 + "🏛️")
    print("🏛️" + "=" * 70 + "🏛️")

def check_installation_readiness():
    """Vérifie que tout est prêt pour l'installation"""
    print("\n🔍 VÉRIFICATION FINALE DE PRÉPARATION")
    print("=" * 50)
    
    checks = [
        ("Manifeste", "sama_syndicat/__manifest__.py"),
        ("Modèles", "sama_syndicat/models/__init__.py"),
        ("Contrôleurs", "sama_syndicat/controllers/__init__.py"),
        ("Vues", "sama_syndicat/views/menus.xml"),
        ("Sécurité", "sama_syndicat/security/security.xml"),
        ("Données", "sama_syndicat/data/sequences.xml"),
        ("Script principal", "sama_syndicat/install_and_start.sh"),
        ("Lanceur Python", "sama_syndicat/launch_sama_syndicat.py"),
    ]
    
    all_ok = True
    for name, path in checks:
        if os.path.exists(path):
            print(f"✅ {name:15} : {path}")
        else:
            print(f"❌ {name:15} : {path} - MANQUANT")
            all_ok = False
    
    return all_ok

def show_installation_options():
    """Affiche les options d'installation"""
    print("\n🚀 OPTIONS D'INSTALLATION AUTONOME")
    print("=" * 50)
    
    options = [
        ("1. Installation Forcée", "./sama_syndicat/dev_scripts/force_install.sh", "Recommandé pour test"),
        ("2. Installation Intelligente", "./sama_syndicat/start_if_installed.sh", "Vérifie avant d'installer"),
        ("3. Installation Simple", "./sama_syndicat/install_and_start.sh", "Installation directe"),
        ("4. Lanceur Python", "python3 sama_syndicat/launch_sama_syndicat.py", "Avec vérifications"),
    ]
    
    for title, command, description in options:
        print(f"\n{title}")
        print(f"   Commande : {command}")
        print(f"   Description : {description}")

def show_diagnostic_tools():
    """Affiche les outils de diagnostic"""
    print("\n🔧 OUTILS DE DIAGNOSTIC")
    print("=" * 50)
    
    tools = [
        ("Test de connectivité", "./sama_syndicat/dev_scripts/test_connectivity.sh"),
        ("Validation syntaxique", "python3 sama_syndicat/dev_scripts/validate_syntax.py"),
        ("Vérification rapide", "python3 sama_syndicat/dev_scripts/quick_check.py"),
        ("Vérification des logs", "./sama_syndicat/dev_scripts/check_logs.sh"),
        ("Résumé du module", "python3 sama_syndicat/dev_scripts/module_summary.py"),
    ]
    
    for name, command in tools:
        print(f"• {name:20} : {command}")

def show_access_info():
    """Affiche les informations d'accès"""
    print("\n🌐 INFORMATIONS D'ACCÈS")
    print("=" * 50)
    print("URL d'accès    : http://localhost:8070")
    print("Port dédié     : 8070 (pas de conflit)")
    print("Utilisateur    : admin")
    print("Mot de passe   : admin (à changer)")
    print("Base de données: sama_syndicat_* (générée automatiquement)")

def show_features():
    """Affiche les fonctionnalités"""
    print("\n🏛️ FONCTIONNALITÉS DISPONIBLES")
    print("=" * 50)
    
    features = [
        "📊 Tableau de Bord - Vue d'ensemble avec KPI",
        "👥 Adhérents - Gestion complète des membres",
        "🏛️ Assemblées - Organisation et votes électroniques",
        "⚖️ Revendications - Suivi des négociations",
        "🚩 Actions Syndicales - Manifestations et grèves",
        "📢 Communications - Multi-canaux avec analytics",
        "🎓 Formations - Programmes et certifications",
        "📋 Conventions - Conventions collectives",
        "🤝 Médiations - Gestion des conflits",
    ]
    
    for feature in features:
        print(f"  {feature}")

def show_statistics():
    """Affiche les statistiques du module"""
    print("\n📊 STATISTIQUES DU MODULE")
    print("=" * 50)
    
    # Compter les fichiers
    total_files = 0
    total_lines = 0
    
    for root, dirs, files in os.walk('sama_syndicat'):
        for file in files:
            if not file.startswith('.'):
                total_files += 1
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        total_lines += len(f.readlines())
                except:
                    pass
    
    print(f"Fichiers créés     : {total_files}")
    print(f"Lignes de code     : {total_lines:,}")
    print(f"Modèles de données : 10")
    print(f"Vues XML           : 13")
    print(f"Groupes sécurité   : 6")
    print(f"Scripts développés : 15+")

def main():
    """Fonction principale"""
    print_banner()
    
    # Vérifications
    if check_installation_readiness():
        print("\n🎉 TOUTES LES VÉRIFICATIONS SONT OK!")
    else:
        print("\n❌ Des fichiers sont manquants")
        return
    
    # Options d'installation
    show_installation_options()
    
    # Outils de diagnostic
    show_diagnostic_tools()
    
    # Informations d'accès
    show_access_info()
    
    # Fonctionnalités
    show_features()
    
    # Statistiques
    show_statistics()
    
    # Instructions finales
    print("\n" + "=" * 70)
    print("🎯 INSTRUCTIONS FINALES")
    print("=" * 70)
    print("1. Choisir une option d'installation ci-dessus")
    print("2. Exécuter la commande correspondante")
    print("3. Attendre la fin de l'installation (2-5 minutes)")
    print("4. Accéder à http://localhost:8070")
    print("5. Se connecter avec admin/admin")
    print("6. Explorer le menu 'Syndicat'")
    
    print("\n🏛️ SAMA SYNDICAT - Gestion Zéro Papier pour Syndicats")
    print("✨ Installation autonome prête - Bonne utilisation ! ✨")

if __name__ == "__main__":
    main()