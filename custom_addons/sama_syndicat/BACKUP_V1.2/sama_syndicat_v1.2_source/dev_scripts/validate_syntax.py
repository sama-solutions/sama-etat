#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de validation syntaxique pour sama_syndicat
"""

import os
import ast
import sys

def validate_python_file(filepath):
    """Valide la syntaxe d'un fichier Python"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Compilation pour vérifier la syntaxe
        ast.parse(content)
        print(f"✅ {filepath}")
        return True
    except SyntaxError as e:
        print(f"❌ {filepath}: Erreur de syntaxe ligne {e.lineno}: {e.msg}")
        return False
    except Exception as e:
        print(f"⚠️  {filepath}: {e}")
        return False

def validate_xml_file(filepath):
    """Valide la syntaxe d'un fichier XML"""
    try:
        import xml.etree.ElementTree as ET
        ET.parse(filepath)
        print(f"✅ {filepath}")
        return True
    except ET.ParseError as e:
        print(f"❌ {filepath}: Erreur XML: {e}")
        return False
    except Exception as e:
        print(f"⚠️  {filepath}: {e}")
        return False

def main():
    """Fonction principale"""
    print("🔍 VALIDATION SYNTAXIQUE - SAMA SYNDICAT")
    print("=" * 50)
    
    module_path = "sama_syndicat"
    errors = 0
    total = 0
    
    # Validation des fichiers Python
    print("\n📝 Fichiers Python:")
    for root, dirs, files in os.walk(module_path):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                total += 1
                if not validate_python_file(filepath):
                    errors += 1
    
    # Validation des fichiers XML
    print("\n📄 Fichiers XML:")
    for root, dirs, files in os.walk(module_path):
        for file in files:
            if file.endswith('.xml'):
                filepath = os.path.join(root, file)
                total += 1
                if not validate_xml_file(filepath):
                    errors += 1
    
    # Validation des fichiers CSV
    print("\n📊 Fichiers CSV:")
    for root, dirs, files in os.walk(module_path):
        for file in files:
            if file.endswith('.csv'):
                filepath = os.path.join(root, file)
                total += 1
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        if len(lines) > 0:
                            print(f"✅ {filepath} ({len(lines)} lignes)")
                        else:
                            print(f"⚠️  {filepath}: Fichier vide")
                except Exception as e:
                    print(f"❌ {filepath}: {e}")
                    errors += 1
    
    print("\n" + "=" * 50)
    print(f"📊 RÉSULTAT: {total - errors}/{total} fichiers valides")
    
    if errors == 0:
        print("🎉 Tous les fichiers sont syntaxiquement corrects!")
        return True
    else:
        print(f"❌ {errors} erreur(s) trouvée(s)")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)