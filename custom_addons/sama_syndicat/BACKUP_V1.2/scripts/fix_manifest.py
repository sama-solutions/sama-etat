#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de validation et correction du manifeste sama_syndicat
"""

import ast
import os
import sys

def validate_manifest(manifest_path):
    """Valide la syntaxe du manifeste"""
    print(f"🔍 Validation du manifeste: {manifest_path}")
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Test de parsing
        manifest_dict = ast.literal_eval(content)
        
        print("✅ Syntaxe du manifeste valide")
        
        # Vérifications de base
        required_keys = ['name', 'version', 'depends', 'installable']
        missing_keys = [key for key in required_keys if key not in manifest_dict]
        
        if missing_keys:
            print(f"⚠️  Clés manquantes: {missing_keys}")
        else:
            print("✅ Toutes les clés requises présentes")
        
        # Afficher les informations
        print(f"📋 Nom: {manifest_dict.get('name', 'N/A')}")
        print(f"📋 Version: {manifest_dict.get('version', 'N/A')}")
        print(f"📋 Dépendances: {len(manifest_dict.get('depends', []))}")
        print(f"📋 Fichiers de données: {len(manifest_dict.get('data', []))}")
        
        return True, manifest_dict
        
    except SyntaxError as e:
        print(f"❌ Erreur de syntaxe ligne {e.lineno}: {e.msg}")
        return False, None
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False, None

def create_clean_manifest():
    """Crée un manifeste propre"""
    clean_manifest = {
        'name': 'SAMA SYNDICAT - Gestion Zéro Papier',
        'version': '1.0.0',
        'category': 'Human Resources',
        'summary': 'Gestion complète et zéro papier d\'un syndicat ou groupement professionnel',
        'description': """
SAMA SYNDICAT - Gestion Zéro Papier d'un Syndicat
==================================================

Ce module permet la gestion complète et zéro papier d'un syndicat ou groupement professionnel.

Fonctionnalités principales :
-----------------------------
* Gestion des adhérents et cotisations
* Organisation des assemblées générales et réunions
* Gestion des revendications et négociations
* Suivi des actions syndicales et manifestations
* Communication avec les adhérents
* Gestion des formations professionnelles
* Suivi des conventions collectives
* Gestion des conflits et médiations
* Tableau de bord et statistiques
* Interface publique pour les adhérents

Auteur : POLITECH SÉNÉGAL
Licence : LGPL-3
        """,
        'author': 'POLITECH SÉNÉGAL',
        'website': 'https://www.politech.sn',
        'license': 'LGPL-3',
        'depends': [
            'base',
            'mail',
            'website',
            'portal',
            'hr',
            'calendar',
            'document',
            'survey',
        ],
        'data': [
            'security/security.xml',
            'security/ir.model.access.csv',
            'data/sequences.xml',
            'data/data.xml',
            'views/syndicat_adherent_views.xml',
            'views/syndicat_assemblee_views.xml',
            'views/syndicat_revendication_views.xml',
            'views/syndicat_action_views.xml',
            'views/syndicat_communication_views.xml',
            'views/syndicat_formation_views.xml',
            'views/syndicat_convention_views.xml',
            'views/syndicat_mediation_views.xml',
            'views/syndicat_dashboard_views.xml',
            'views/menus.xml',
        ],
        'demo': [],
        'installable': True,
        'auto_install': False,
        'application': True,
        'sequence': 10,
    }
    
    return clean_manifest

def write_manifest(manifest_path, manifest_dict):
    """Écrit le manifeste de façon propre"""
    print(f"✏️  Écriture du manifeste: {manifest_path}")
    
    # Créer une sauvegarde
    backup_path = manifest_path + '.backup'
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r') as src, open(backup_path, 'w') as dst:
            dst.write(src.read())
        print(f"💾 Sauvegarde créée: {backup_path}")
    
    # Écrire le nouveau manifeste
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write("{\n")
        
        for key, value in manifest_dict.items():
            if isinstance(value, str):
                # Échapper les apostrophes dans les chaînes
                escaped_value = value.replace("'", "\\'")
                if '\n' in value:
                    f.write(f"    '{key}': \"\"\"{value}\"\"\",\n")
                else:
                    f.write(f"    '{key}': '{escaped_value}',\n")
            elif isinstance(value, list):
                f.write(f"    '{key}': [\n")
                for item in value:
                    f.write(f"        '{item}',\n")
                f.write("    ],\n")
            elif isinstance(value, bool):
                f.write(f"    '{key}': {str(value)},\n")
            elif isinstance(value, (int, float)):
                f.write(f"    '{key}': {value},\n")
            else:
                f.write(f"    '{key}': {repr(value)},\n")
        
        f.write("}\n")
    
    print("✅ Manifeste écrit avec succès")

def main():
    """Fonction principale"""
    print("🏛️  SAMA SYNDICAT - VALIDATION ET CORRECTION DU MANIFESTE")
    print("=" * 60)
    
    # Toujours résoudre le chemin du manifeste relativement au script, pas au CWD
    module_dir = os.path.dirname(os.path.abspath(__file__))
    manifest_path = os.path.join(module_dir, "__manifest__.py")
    
    if not os.path.exists(manifest_path):
        print(f"❌ Manifeste non trouvé: {manifest_path}")
        sys.exit(1)
    
    # Validation
    is_valid, manifest_dict = validate_manifest(manifest_path)
    
    if not is_valid:
        print("\n🔧 CORRECTION AUTOMATIQUE")
        print("-" * 30)
        print("⚠️  Le manifeste contient des erreurs, création d'un manifeste propre...")
        
        clean_manifest = create_clean_manifest()
        write_manifest(manifest_path, clean_manifest)
        
        # Re-validation
        print("\n🔍 RE-VALIDATION")
        print("-" * 30)
        is_valid, _ = validate_manifest(manifest_path)
        
        if is_valid:
            print("✅ Manifeste corrigé avec succès!")
        else:
            print("❌ Impossible de corriger le manifeste")
            sys.exit(1)
    
    print("\n🎉 MANIFESTE VALIDE ET PRÊT POUR L'INSTALLATION")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)