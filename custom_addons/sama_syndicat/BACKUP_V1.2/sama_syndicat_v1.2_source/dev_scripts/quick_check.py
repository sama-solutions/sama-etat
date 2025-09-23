#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vérification rapide des erreurs potentielles
"""

import os
import sys
import ast
import subprocess

def check_manifest():
    """Vérifie le manifeste"""
    print("🔍 Vérification du manifeste...")
    
    try:
        with open('sama_syndicat/__manifest__.py', 'r') as f:
            content = f.read()
        
        # Parser le manifeste
        tree = ast.parse(content)
        
        # Extraire le dictionnaire
        for node in ast.walk(tree):
            if isinstance(node, ast.Dict):
                manifest = ast.literal_eval(node)
                break
        
        print("✅ Manifeste syntaxiquement correct")
        
        # Vérifier les dépendances
        depends = manifest.get('depends', [])
        print(f"📦 Dépendances: {', '.join(depends)}")
        
        # Vérifier les fichiers de données
        data_files = manifest.get('data', [])
        missing_files = []
        
        for file_path in data_files:
            full_path = f"sama_syndicat/{file_path}"
            if not os.path.exists(full_path):
                missing_files.append(file_path)
        
        if missing_files:
            print("❌ Fichiers manquants dans data:")
            for file in missing_files:
                print(f"  • {file}")
            return False
        else:
            print("✅ Tous les fichiers de données existent")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans le manifeste: {e}")
        return False

def check_python_imports():
    """Vérifie les imports Python"""
    print("\n🔍 Vérification des imports Python...")
    
    python_files = []
    for root, dirs, files in os.walk('sama_syndicat'):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    errors = []
    
    for file_path in python_files:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Vérifier la syntaxe
            ast.parse(content)
            
            # Vérifier les imports Odoo (basique)
            if 'from odoo import' in content or 'import odoo' in content:
                # C'est un fichier Odoo, vérifier les imports courants
                if 'models' in content and 'from odoo import models' not in content:
                    errors.append(f"{file_path}: Import 'models' manquant")
                
                if 'fields' in content and 'from odoo import' in content and 'fields' not in content.split('from odoo import')[1].split('\n')[0]:
                    errors.append(f"{file_path}: Import 'fields' manquant")
            
        except SyntaxError as e:
            errors.append(f"{file_path}: Erreur de syntaxe ligne {e.lineno}: {e.msg}")
        except Exception as e:
            errors.append(f"{file_path}: {e}")
    
    if errors:
        print("❌ Erreurs trouvées:")
        for error in errors[:10]:  # Limiter à 10 erreurs
            print(f"  • {error}")
        return False
    else:
        print("✅ Imports Python OK")
        return True

def check_xml_syntax():
    """Vérifie la syntaxe XML"""
    print("\n🔍 Vérification de la syntaxe XML...")
    
    try:
        import xml.etree.ElementTree as ET
        
        xml_files = []
        for root, dirs, files in os.walk('sama_syndicat'):
            for file in files:
                if file.endswith('.xml'):
                    xml_files.append(os.path.join(root, file))
        
        errors = []
        
        for file_path in xml_files:
            try:
                ET.parse(file_path)
            except ET.ParseError as e:
                errors.append(f"{file_path}: {e}")
            except Exception as e:
                errors.append(f"{file_path}: {e}")
        
        if errors:
            print("❌ Erreurs XML:")
            for error in errors:
                print(f"  • {error}")
            return False
        else:
            print("✅ Syntaxe XML OK")
            return True
            
    except ImportError:
        print("⚠️  Module xml non disponible")
        return True

def check_csv_files():
    """Vérifie les fichiers CSV"""
    print("\n🔍 Vérification des fichiers CSV...")
    
    csv_files = []
    for root, dirs, files in os.walk('sama_syndicat'):
        for file in files:
            if file.endswith('.csv'):
                csv_files.append(os.path.join(root, file))
    
    errors = []
    
    for file_path in csv_files:
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            if len(lines) < 2:
                errors.append(f"{file_path}: Fichier vide ou sans données")
                continue
            
            # Vérifier que toutes les lignes ont le même nombre de colonnes
            header_cols = len(lines[0].split(','))
            for i, line in enumerate(lines[1:], 2):
                if line.strip() and len(line.split(',')) != header_cols:
                    errors.append(f"{file_path}: Ligne {i} - nombre de colonnes incorrect")
                    break
            
        except Exception as e:
            errors.append(f"{file_path}: {e}")
    
    if errors:
        print("❌ Erreurs CSV:")
        for error in errors:
            print(f"  • {error}")
        return False
    else:
        print("✅ Fichiers CSV OK")
        return True

def run_odoo_syntax_check():
    """Test rapide avec Odoo"""
    print("\n🔍 Test rapide avec Odoo...")
    
    try:
        # Test très basique - juste voir si Odoo peut parser le module
        cmd = """
cd /var/odoo/odoo18 && timeout 30 python3 -c "
import sys
sys.path.insert(0, '/home/grand-as/psagsn/custom_addons')
try:
    import sama_syndicat
    print('✅ Module importable')
except ImportError as e:
    print(f'❌ Erreur import: {e}')
except Exception as e:
    print(f'⚠️  Autre erreur: {e}')
"
        """
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=45)
        
        if result.returncode == 0:
            print(result.stdout.strip())
            return True
        else:
            print(f"❌ Erreur: {result.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Timeout du test Odoo")
        return False
    except Exception as e:
        print(f"❌ Erreur test Odoo: {e}")
        return False

def main():
    """Fonction principale"""
    print("🏛️  SAMA SYNDICAT - VÉRIFICATION RAPIDE")
    print("=" * 50)
    
    all_ok = True
    
    # Tests
    if not check_manifest():
        all_ok = False
    
    if not check_python_imports():
        all_ok = False
    
    if not check_xml_syntax():
        all_ok = False
    
    if not check_csv_files():
        all_ok = False
    
    if not run_odoo_syntax_check():
        all_ok = False
    
    print("\n" + "=" * 50)
    if all_ok:
        print("🎉 Toutes les vérifications sont OK!")
        print("✅ Le module devrait s'installer sans erreur")
    else:
        print("❌ Des problèmes ont été détectés")
        print("🔧 Corrigez les erreurs avant l'installation")
    
    return all_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)