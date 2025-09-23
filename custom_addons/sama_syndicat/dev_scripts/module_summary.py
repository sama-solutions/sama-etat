#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Résumé du module sama_syndicat
"""

import os
import glob

def count_lines_in_file(filepath):
    """Compte les lignes dans un fichier"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except:
        return 0

def get_file_stats():
    """Statistiques des fichiers"""
    stats = {
        'python': {'count': 0, 'lines': 0},
        'xml': {'count': 0, 'lines': 0},
        'csv': {'count': 0, 'lines': 0},
        'md': {'count': 0, 'lines': 0},
        'sh': {'count': 0, 'lines': 0},
    }
    
    for root, dirs, files in os.walk('sama_syndicat'):
        for file in files:
            filepath = os.path.join(root, file)
            lines = count_lines_in_file(filepath)
            
            if file.endswith('.py'):
                stats['python']['count'] += 1
                stats['python']['lines'] += lines
            elif file.endswith('.xml'):
                stats['xml']['count'] += 1
                stats['xml']['lines'] += lines
            elif file.endswith('.csv'):
                stats['csv']['count'] += 1
                stats['csv']['lines'] += lines
            elif file.endswith('.md'):
                stats['md']['count'] += 1
                stats['md']['lines'] += lines
            elif file.endswith('.sh'):
                stats['sh']['count'] += 1
                stats['sh']['lines'] += lines
    
    return stats

def main():
    """Fonction principale"""
    print("🏛️  SAMA SYNDICAT - Résumé du Module")
    print("=" * 60)
    
    # Informations générales
    print("\n📋 INFORMATIONS GÉNÉRALES")
    print("-" * 30)
    print("Nom du module    : SAMA SYNDICAT")
    print("Version          : 1.0.0")
    print("Auteur           : POLITECH SÉNÉGAL")
    print("Licence          : LGPL-3")
    print("Type             : Application Odoo 18 CE")
    
    # Statistiques des fichiers
    print("\n📊 STATISTIQUES DES FICHIERS")
    print("-" * 30)
    stats = get_file_stats()
    total_files = sum(s['count'] for s in stats.values())
    total_lines = sum(s['lines'] for s in stats.values())
    
    for file_type, data in stats.items():
        if data['count'] > 0:
            print(f"{file_type.upper():10} : {data['count']:2} fichiers, {data['lines']:4} lignes")
    
    print(f"{'TOTAL':10} : {total_files:2} fichiers, {total_lines:4} lignes")
    
    # Modèles
    print("\n🗃️  MODÈLES DE DONNÉES")
    print("-" * 30)
    models = [
        "syndicat.adherent      - Gestion des adhérents et cotisations",
        "syndicat.assemblee     - Assemblées et système de vote",
        "syndicat.revendication - Revendications et négociations",
        "syndicat.action        - Actions syndicales (grèves, manifestations)",
        "syndicat.communication - Communications multi-canaux",
        "syndicat.formation     - Formations avec certifications",
        "syndicat.convention    - Conventions collectives",
        "syndicat.mediation     - Gestion des conflits et médiations",
        "syndicat.dashboard     - Tableau de bord analytique",
        "res.partner (étendu)   - Extension des contacts"
    ]
    
    for model in models:
        print(f"• {model}")
    
    # Fonctionnalités
    print("\n🚀 FONCTIONNALITÉS PRINCIPALES")
    print("-" * 30)
    features = [
        "✅ Gestion zéro papier complète",
        "✅ Interface web responsive",
        "✅ Portail adhérents",
        "✅ Tableau de bord analytique",
        "✅ Communications multi-canaux",
        "✅ Système de vote électronique",
        "✅ Gestion des formations",
        "✅ Suivi des conventions collectives",
        "✅ Médiation des conflits",
        "✅ Sécurité par rôles",
        "✅ API REST intégrée",
        "✅ Rapports et statistiques"
    ]
    
    for feature in features:
        print(feature)
    
    # Vues disponibles
    print("\n👁️  VUES DISPONIBLES")
    print("-" * 30)
    views = [
        "Kanban    - Vue par défaut avec cartes interactives",
        "Liste     - Tableaux avec édition en masse",
        "Formulaire- Formulaires détaillés avec workflow",
        "Graphique - Statistiques et analyses",
        "Pivot     - Analyses croisées",
        "Calendrier- Planning des événements"
    ]
    
    for view in views:
        print(f"• {view}")
    
    # Sécurité
    print("\n🔒 SÉCURITÉ")
    print("-" * 30)
    security = [
        "Adhérent    - Accès limité aux données personnelles",
        "Utilisateur - Accès lecture/écriture aux données courantes",
        "Secrétaire  - Gestion des communications et assemblées",
        "Trésorier   - Gestion des cotisations et finances",
        "Formateur   - Gestion des formations",
        "Responsable - Accès complet à toutes les données"
    ]
    
    for role in security:
        print(f"• {role}")
    
    # Scripts de développement
    print("\n🛠️  SCRIPTS DE DÉVELOPPEMENT")
    print("-" * 30)
    scripts = [
        "validate_syntax.py - Validation syntaxique",
        "quick_install.sh   - Installation rapide",
        "simple_test.py     - Test complet",
        "test_module.py     - Test avancé",
        "module_summary.py  - Ce résumé"
    ]
    
    for script in scripts:
        print(f"• {script}")
    
    # Instructions de démarrage
    print("\n🚀 DÉMARRAGE RAPIDE")
    print("-" * 30)
    print("1. Validation : python3 sama_syndicat/dev_scripts/validate_syntax.py")
    print("2. Installation: ./sama_syndicat/dev_scripts/quick_install.sh")
    print("3. Démarrage   : python3 sama_syndicat/start_syndicat.py")
    print("4. Accès web   : http://localhost:8070")
    
    print("\n" + "=" * 60)
    print("🎉 Module SAMA SYNDICAT prêt pour l'installation!")

if __name__ == "__main__":
    main()