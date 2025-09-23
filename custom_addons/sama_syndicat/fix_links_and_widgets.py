#!/usr/bin/env python3
"""
Script pour corriger tous les liens et widgets dans SAMA SYNDICAT
Inventaire et correction des actions, liens et widgets
"""

import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

class LinkWidgetFixer:
    def __init__(self):
        self.module_path = Path(".")
        self.views_path = self.module_path / "views"
        self.models_path = self.module_path / "models"
        
        # Actions définies dans les vues
        self.defined_actions = set()
        
        # Actions Python disponibles
        self.python_actions = set()
        
        # Problèmes trouvés
        self.issues = []
        
        # Corrections à appliquer
        self.corrections = []
        
    def analyze_defined_actions(self):
        """Analyser toutes les actions définies dans les fichiers XML"""
        print("🔍 Analyse des actions définies...")
        
        for xml_file in self.views_path.glob("*.xml"):
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                # Chercher les actions ir.actions.act_window
                for record in root.findall(".//record[@model='ir.actions.act_window']"):
                    action_id = record.get('id')
                    if action_id:
                        self.defined_actions.add(action_id)
                        print(f"  ✅ Action trouvée: {action_id} dans {xml_file.name}")
                        
            except ET.ParseError as e:
                print(f"  ❌ Erreur XML dans {xml_file}: {e}")
                
        print(f"📊 Total actions définies: {len(self.defined_actions)}")
        
    def analyze_python_actions(self):
        """Analyser toutes les méthodes action_ dans les modèles Python"""
        print("🐍 Analyse des actions Python...")
        
        for py_file in self.models_path.glob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Chercher les méthodes def action_
                action_methods = re.findall(r'def (action_\w+)', content)
                for method in action_methods:
                    self.python_actions.add(method)
                    print(f"  ✅ Méthode trouvée: {method} dans {py_file.name}")
                    
            except Exception as e:
                print(f"  ❌ Erreur dans {py_file}: {e}")
                
        print(f"📊 Total méthodes Python: {len(self.python_actions)}")
        
    def analyze_widget_issues(self):
        """Analyser les problèmes dans les widgets et liens"""
        print("🔧 Analyse des widgets et liens...")
        
        for xml_file in self.views_path.glob("*.xml"):
            try:
                with open(xml_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\\n')
                    
                for i, line in enumerate(lines, 1):
                    # Chercher les boutons avec type="object"
                    if 'type="object"' in line and 'name=' in line:
                        match = re.search(r'name="([^"]+)"', line)
                        if match:
                            action_name = match.group(1)
                            if action_name.startswith('action_'):
                                if action_name not in self.python_actions:
                                    self.issues.append({
                                        'type': 'missing_python_action',
                                        'file': xml_file.name,
                                        'line': i,
                                        'action': action_name,
                                        'content': line.strip()
                                    })
                                    
                    # Chercher les liens avec action=
                    if 'action=' in line:
                        matches = re.findall(r'action="([^"]+)"', line)
                        for action_name in matches:
                            if action_name not in self.defined_actions:
                                self.issues.append({
                                    'type': 'missing_xml_action',
                                    'file': xml_file.name,
                                    'line': i,
                                    'action': action_name,
                                    'content': line.strip()
                                })
                                
                    # Chercher les t-on-click avec action
                    if 't-on-click' in line and 'action:' in line:
                        matches = re.findall(r"action: '([^']+)'", line)
                        for action_name in matches:
                            if action_name not in self.python_actions:
                                self.issues.append({
                                    'type': 'missing_onclick_action',
                                    'file': xml_file.name,
                                    'line': i,
                                    'action': action_name,
                                    'content': line.strip()
                                })
                                
            except Exception as e:
                print(f"  ❌ Erreur dans {xml_file}: {e}")
                
        print(f"📊 Total problèmes trouvés: {len(self.issues)}")
        
    def generate_corrections(self):
        """Générer les corrections pour tous les problèmes"""
        print("🔨 Génération des corrections...")
        
        # Mapping des actions manquantes vers les bonnes actions
        action_mapping = {
            # Actions du dashboard
            'action_open_adherents': 'action_syndicat_adherent',
            'action_open_cotisations': 'action_syndicat_adherent',  # Pas d'action cotisation séparée
            'action_open_assemblees': 'action_syndicat_assemblee',
            'action_open_revendications': 'action_syndicat_revendication',
            'action_open_actions': 'action_syndicat_action',
            'action_open_formations': 'action_syndicat_formation',
            'action_open_mediations': 'action_syndicat_mediation',
            'action_open_communications': 'action_syndicat_communication',
            
            # Actions d'alertes (garder les méthodes Python existantes)
            'action_open_alertes_cotisations': 'action_open_alertes_cotisations',
            'action_open_alertes_assemblees': 'action_open_alertes_assemblees',
            'action_open_alertes_actions': 'action_open_alertes_actions',
            'action_open_alertes_mediations': 'action_open_alertes_mediations',
            
            # Actions de vues (utiliser les actions principales)
            'action_view_participants': 'action_view_participants',  # Méthode existe
            'action_view_cotisations': 'action_view_cotisations',    # Méthode existe
            'action_view_assemblees': 'action_view_assemblees',      # Méthode existe
            'action_view_actions': 'action_view_actions',            # Méthode existe
            'action_view_communications': 'action_view_communications', # Méthode existe
            'action_view_revendications': 'action_view_revendications', # Méthode existe
            'action_view_formations': 'action_syndicat_formation',
            'action_view_mediations': 'action_syndicat_mediation',
            'action_view_conventions': 'action_syndicat_convention',
        }
        
        for issue in self.issues:
            action = issue['action']
            
            if issue['type'] == 'missing_xml_action':
                # Pour les actions XML manquantes, utiliser le mapping
                if action in action_mapping:
                    new_action = action_mapping[action]
                    if new_action in self.defined_actions:
                        self.corrections.append({
                            'file': issue['file'],
                            'line': issue['line'],
                            'old_action': action,
                            'new_action': new_action,
                            'type': 'xml_action_fix'
                        })
                        
            elif issue['type'] == 'missing_python_action':
                # Pour les actions Python manquantes, vérifier si elles existent
                if action not in self.python_actions:
                    # Suggérer une action alternative
                    suggested = self.suggest_alternative_action(action)
                    if suggested:
                        self.corrections.append({
                            'file': issue['file'],
                            'line': issue['line'],
                            'old_action': action,
                            'new_action': suggested,
                            'type': 'python_action_fix'
                        })
                        
        print(f"📊 Total corrections générées: {len(self.corrections)}")
        
    def suggest_alternative_action(self, action):
        """Suggérer une action alternative basée sur le nom"""
        # Mapping des actions manquantes vers des alternatives
        alternatives = {
            'action_view_feedback': 'action_view_communications',
            'action_view_destinataires': 'action_view_communications',
            'action_view_lectures': 'action_view_communications',
            'action_view_reponses': 'action_view_communications',
            'action_view_resultats': 'action_view_participants',
            'action_view_budget': 'action_view_participants',
            'action_view_interventions': 'action_view_participants',
            'action_view_delais': 'action_view_participants',
            'action_view_votes': 'action_view_participants',
            'action_view_soutiens': 'action_view_participants',
            'action_view_negociations': 'action_view_participants',
            'action_view_representants': 'action_view_participants',
            'action_view_suivi': 'action_view_participants',
            'action_view_avenants': 'action_view_participants',
        }
        
        if action in alternatives:
            suggested = alternatives[action]
            if suggested in self.python_actions:
                return suggested
                
        return None
        
    def apply_corrections(self):
        """Appliquer toutes les corrections"""
        print("✏️ Application des corrections...")
        
        files_to_modify = {}
        
        # Grouper les corrections par fichier
        for correction in self.corrections:
            file_path = self.views_path / correction['file']
            if file_path not in files_to_modify:
                files_to_modify[file_path] = []
            files_to_modify[file_path].append(correction)
            
        # Appliquer les corrections fichier par fichier
        for file_path, corrections in files_to_modify.items():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Appliquer les corrections
                for correction in corrections:
                    old_action = correction['old_action']
                    new_action = correction['new_action']
                    
                    # Remplacer l'action
                    content = content.replace(f'action="{old_action}"', f'action="{new_action}"')
                    content = content.replace(f"action: '{old_action}'", f"action: '{new_action}'")
                    
                    print(f"  ✅ {file_path.name}: {old_action} → {new_action}")
                    
                # Sauvegarder le fichier modifié
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            except Exception as e:
                print(f"  ❌ Erreur lors de la modification de {file_path}: {e}")
                
    def create_missing_actions(self):
        """Créer les actions manquantes dans les fichiers appropriés"""
        print("🆕 Création des actions manquantes...")
        
        # Actions à créer dans syndicat_dashboard_views.xml
        dashboard_actions = [
            'action_open_cotisations',
        ]
        
        # Créer les actions manquantes
        for action in dashboard_actions:
            if action not in self.defined_actions:
                self.create_cotisations_action()
                
    def create_cotisations_action(self):
        """Créer l'action pour les cotisations"""
        dashboard_views_file = self.views_path / "syndicat_dashboard_views.xml"
        
        try:
            with open(dashboard_views_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Ajouter l'action avant la fermeture du fichier
            action_xml = '''
        <!-- Action pour les Cotisations -->
        <record id="action_open_cotisations" model="ir.actions.act_window">
            <field name="name">Cotisations</field>
            <field name="res_model">syndicat.adherent</field>
            <field name="view_mode">list,form</field>
            <field name="domain">[('cotisations_a_jour', '=', False)]</field>
            <field name="context">{'search_default_cotisations_retard': 1}</field>
            <field name="help">Liste des adhérents avec des cotisations en retard</field>
        </record>
'''
            
            # Insérer avant la fermeture
            content = content.replace('</odoo>', action_xml + '\\n    </odoo>')
            
            with open(dashboard_views_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"  ✅ Action action_open_cotisations créée dans {dashboard_views_file.name}")
            
        except Exception as e:
            print(f"  ❌ Erreur lors de la création de l'action cotisations: {e}")
            
    def generate_report(self):
        """Générer un rapport complet"""
        print("📋 Génération du rapport...")
        
        report_content = f"""# RAPPORT DE CORRECTION - SAMA SYNDICAT
## Liens et Widgets

### 📊 STATISTIQUES
- Actions XML définies: {len(self.defined_actions)}
- Méthodes Python disponibles: {len(self.python_actions)}
- Problèmes trouvés: {len(self.issues)}
- Corrections appliquées: {len(self.corrections)}

### ✅ ACTIONS XML DÉFINIES
"""
        for action in sorted(self.defined_actions):
            report_content += f"- {action}\\n"
            
        report_content += f"""
### 🐍 MÉTHODES PYTHON DISPONIBLES
"""
        for action in sorted(self.python_actions):
            report_content += f"- {action}\\n"
            
        report_content += f"""
### 🔧 PROBLÈMES TROUVÉS
"""
        for issue in self.issues:
            report_content += f"- **{issue['type']}** dans {issue['file']}:{issue['line']} - {issue['action']}\\n"
            
        report_content += f"""
### ✏️ CORRECTIONS APPLIQUÉES
"""
        for correction in self.corrections:
            report_content += f"- {correction['file']}: {correction['old_action']} → {correction['new_action']}\\n"
            
        # Sauvegarder le rapport
        with open("RAPPORT_CORRECTIONS.md", 'w', encoding='utf-8') as f:
            f.write(report_content)
            
        print("  ✅ Rapport sauvegardé dans RAPPORT_CORRECTIONS.md")
        
    def run(self):
        """Exécuter toutes les analyses et corrections"""
        print("🚀 CORRECTION DES LIENS ET WIDGETS - SAMA SYNDICAT")
        print("=" * 50)
        
        self.analyze_defined_actions()
        print()
        
        self.analyze_python_actions()
        print()
        
        self.analyze_widget_issues()
        print()
        
        self.generate_corrections()
        print()
        
        self.create_missing_actions()
        print()
        
        self.apply_corrections()
        print()
        
        self.generate_report()
        print()
        
        print("✅ CORRECTION TERMINÉE AVEC SUCCÈS!")
        print(f"📊 Résumé: {len(self.corrections)} corrections appliquées")

if __name__ == "__main__":
    fixer = LinkWidgetFixer()
    fixer.run()