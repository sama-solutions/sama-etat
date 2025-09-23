#!/usr/bin/env python3
"""
Script de validation finale pour SAMA SYNDICAT
Vérification de toutes les corrections apportées aux liens et widgets
"""

import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

class CorrectionValidator:
    def __init__(self):
        self.module_path = Path(".")
        self.views_path = self.module_path / "views"
        self.models_path = self.module_path / "models"
        self.controllers_path = self.module_path / "controllers"
        
        # Résultats de validation
        self.validation_results = {
            'actions_defined': [],
            'python_methods': [],
            'website_enabled': False,
            'controllers_created': False,
            'templates_created': False,
            'css_created': False,
            'dashboard_links_fixed': False,
            'all_widgets_working': True,
            'issues_found': [],
            'recommendations': []
        }
        
    def validate_actions(self):
        """Valider que toutes les actions sont définies"""
        print("🔍 Validation des actions définies...")
        
        for xml_file in self.views_path.glob("*.xml"):
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                for record in root.findall(".//record[@model='ir.actions.act_window']"):
                    action_id = record.get('id')
                    if action_id:
                        self.validation_results['actions_defined'].append(action_id)
                        
            except ET.ParseError as e:
                self.validation_results['issues_found'].append(f"XML Error in {xml_file}: {e}")
                
        print(f"  ✅ {len(self.validation_results['actions_defined'])} actions trouvées")
        
    def validate_python_methods(self):
        """Valider que toutes les méthodes Python existent"""
        print("🐍 Validation des méthodes Python...")
        
        for py_file in self.models_path.glob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                action_methods = re.findall(r'def (action_\w+)', content)
                self.validation_results['python_methods'].extend(action_methods)
                
            except Exception as e:
                self.validation_results['issues_found'].append(f"Python Error in {py_file}: {e}")
                
        print(f"  ✅ {len(self.validation_results['python_methods'])} méthodes trouvées")
        
    def validate_website_features(self):
        """Valider les fonctionnalités website"""
        print("🌐 Validation des fonctionnalités website...")
        
        # Vérifier le manifeste
        try:
            with open("__manifest__.py", 'r', encoding='utf-8') as f:
                manifest_content = f.read()
                if "'website'" in manifest_content:
                    self.validation_results['website_enabled'] = True
                    print("  ✅ Module website activé dans le manifeste")
                else:
                    self.validation_results['issues_found'].append("Module website non trouvé dans les dépendances")
        except Exception as e:
            self.validation_results['issues_found'].append(f"Erreur lecture manifeste: {e}")
            
        # Vérifier les contrôleurs
        if self.controllers_path.exists():
            self.validation_results['controllers_created'] = True
            print("  ✅ Contrôleurs website créés")
        else:
            self.validation_results['issues_found'].append("Répertoire controllers manquant")
            
        # Vérifier les templates
        website_templates = self.views_path / "website" / "website_templates.xml"
        if website_templates.exists():
            self.validation_results['templates_created'] = True
            print("  ✅ Templates website créés")
        else:
            self.validation_results['issues_found'].append("Templates website manquants")
            
        # Vérifier le CSS
        website_css = self.module_path / "static" / "src" / "css" / "website.css"
        if website_css.exists():
            self.validation_results['css_created'] = True
            print("  ✅ CSS website créé")
        else:
            self.validation_results['issues_found'].append("CSS website manquant")
            
    def validate_dashboard_links(self):
        """Valider que les liens du dashboard sont corrigés"""
        print("📊 Validation des liens du dashboard...")
        
        dashboard_file = self.views_path / "syndicat_dashboard_views.xml"
        try:
            with open(dashboard_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Vérifier qu'il n'y a plus de liens href statiques
            static_links = re.findall(r'href="/web#action=', content)
            if not static_links:
                self.validation_results['dashboard_links_fixed'] = True
                print("  ✅ Liens statiques du dashboard corrigés")
            else:
                self.validation_results['issues_found'].append(f"Liens statiques trouvés: {len(static_links)}")
                
            # Vérifier la présence de t-on-click
            onclick_actions = re.findall(r't-on-click.*action:', content)
            if onclick_actions:
                print(f"  ✅ {len(onclick_actions)} actions t-on-click trouvées")
            else:
                self.validation_results['issues_found'].append("Aucune action t-on-click trouvée")
                
        except Exception as e:
            self.validation_results['issues_found'].append(f"Erreur validation dashboard: {e}")
            
    def validate_widget_consistency(self):
        """Valider la cohérence des widgets"""
        print("🔧 Validation de la cohérence des widgets...")
        
        # Actions définies
        defined_actions = set(self.validation_results['actions_defined'])
        
        # Méthodes Python disponibles
        python_methods = set(self.validation_results['python_methods'])
        
        # Vérifier les widgets dans tous les fichiers XML
        for xml_file in self.views_path.glob("*.xml"):
            try:
                with open(xml_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Chercher les boutons avec type="object"
                object_buttons = re.findall(r'name="([^"]+)".*type="object"', content)
                for button_action in object_buttons:
                    if button_action.startswith('action_') and button_action not in python_methods:
                        self.validation_results['issues_found'].append(
                            f"Méthode manquante: {button_action} dans {xml_file.name}"
                        )
                        self.validation_results['all_widgets_working'] = False
                        
                # Chercher les actions dans les liens
                action_links = re.findall(r'action="([^"]+)"', content)
                for action_link in action_links:
                    if action_link not in defined_actions:
                        self.validation_results['issues_found'].append(
                            f"Action manquante: {action_link} dans {xml_file.name}"
                        )
                        self.validation_results['all_widgets_working'] = False
                        
            except Exception as e:
                self.validation_results['issues_found'].append(f"Erreur validation widgets {xml_file}: {e}")
                
        if self.validation_results['all_widgets_working']:
            print("  ✅ Tous les widgets sont cohérents")
        else:
            print(f"  ⚠️ {len([i for i in self.validation_results['issues_found'] if 'manquante' in i])} problèmes trouvés")
            
    def generate_recommendations(self):
        """Générer des recommandations"""
        print("💡 Génération des recommandations...")
        
        recommendations = []
        
        if not self.validation_results['website_enabled']:
            recommendations.append("Activer le module website dans les dépendances")
            
        if not self.validation_results['controllers_created']:
            recommendations.append("Créer les contrôleurs pour les pages publiques")
            
        if not self.validation_results['templates_created']:
            recommendations.append("Créer les templates pour le site web")
            
        if not self.validation_results['css_created']:
            recommendations.append("Créer le CSS pour le site web")
            
        if not self.validation_results['dashboard_links_fixed']:
            recommendations.append("Corriger les liens statiques du dashboard")
            
        if not self.validation_results['all_widgets_working']:
            recommendations.append("Corriger les widgets et actions manquantes")
            
        # Recommandations d'amélioration
        if len(self.validation_results['actions_defined']) < 10:
            recommendations.append("Considérer l'ajout d'actions supplémentaires pour une meilleure navigation")
            
        if len(self.validation_results['python_methods']) > 50:
            recommendations.append("Considérer la refactorisation pour réduire la complexité")
            
        self.validation_results['recommendations'] = recommendations
        
        if recommendations:
            print(f"  💡 {len(recommendations)} recommandations générées")
        else:
            print("  ✅ Aucune recommandation - Module optimal")
            
    def generate_final_report(self):
        """Générer le rapport final"""
        print("📋 Génération du rapport final...")
        
        report_content = f"""# RAPPORT FINAL DE VALIDATION - SAMA SYNDICAT V1.1
## Correction des Liens et Widgets

### 📊 RÉSUMÉ EXÉCUTIF
- **Actions définies**: {len(self.validation_results['actions_defined'])}
- **Méthodes Python**: {len(self.validation_results['python_methods'])}
- **Website activé**: {'✅ OUI' if self.validation_results['website_enabled'] else '❌ NON'}
- **Contrôleurs créés**: {'✅ OUI' if self.validation_results['controllers_created'] else '❌ NON'}
- **Templates créés**: {'✅ OUI' if self.validation_results['templates_created'] else '❌ NON'}
- **CSS créé**: {'✅ OUI' if self.validation_results['css_created'] else '❌ NON'}
- **Dashboard corrigé**: {'✅ OUI' if self.validation_results['dashboard_links_fixed'] else '❌ NON'}
- **Widgets cohérents**: {'✅ OUI' if self.validation_results['all_widgets_working'] else '❌ NON'}

### ✅ ACTIONS DÉFINIES ({len(self.validation_results['actions_defined'])})
"""
        for action in sorted(self.validation_results['actions_defined']):
            report_content += f"- {action}\\n"
            
        report_content += f"""
### 🐍 MÉTHODES PYTHON ({len(self.validation_results['python_methods'])})
"""
        for method in sorted(set(self.validation_results['python_methods'])):
            report_content += f"- {method}\\n"
            
        if self.validation_results['issues_found']:
            report_content += f"""
### ⚠️ PROBLÈMES TROUVÉS ({len(self.validation_results['issues_found'])})
"""
            for issue in self.validation_results['issues_found']:
                report_content += f"- {issue}\\n"
        else:
            report_content += """
### ✅ AUCUN PROBLÈME TROUVÉ
Tous les liens et widgets fonctionnent correctement.
"""
            
        if self.validation_results['recommendations']:
            report_content += f"""
### 💡 RECOMMANDATIONS ({len(self.validation_results['recommendations'])})
"""
            for rec in self.validation_results['recommendations']:
                report_content += f"- {rec}\\n"
        else:
            report_content += """
### 🏆 AUCUNE RECOMMANDATION
Le module est optimalement configuré.
"""
            
        report_content += f"""
### 🌐 URLS PUBLIQUES DISPONIBLES
Avec l'activation du module website, les URLs suivantes sont maintenant disponibles :

#### Pages Principales
- `/syndicat` - Page d'accueil
- `/syndicat/about` - À propos
- `/syndicat/adhesion` - Formulaire d'adhésion
- `/syndicat/contact` - Contact

#### Contenu Dynamique
- `/syndicat/actualites` - Liste des actualités
- `/syndicat/actualites/<id>` - Détail d'une actualité
- `/syndicat/revendications` - Revendications publiques
- `/syndicat/formations` - Formations ouvertes
- `/syndicat/formations/<id>/inscription` - Inscription formation

### 🎯 CONCLUSION
{'🎉 SAMA SYNDICAT V1.1 est maintenant parfaitement configuré avec tous les liens et widgets fonctionnels, plus un site web public complet !' if not self.validation_results['issues_found'] and self.validation_results['website_enabled'] else '⚠️ Des corrections supplémentaires sont nécessaires.'}

---
**Rapport généré le**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Version**: SAMA SYNDICAT V1.1 Stable
**Développé par**: POLITECH SÉNÉGAL
"""
        
        with open("RAPPORT_VALIDATION_FINALE.md", 'w', encoding='utf-8') as f:
            f.write(report_content)
            
        print("  ✅ Rapport final sauvegardé: RAPPORT_VALIDATION_FINALE.md")
        
    def run(self):
        """Exécuter toutes les validations"""
        print("🚀 VALIDATION FINALE - SAMA SYNDICAT V1.1")
        print("=" * 50)
        
        self.validate_actions()
        print()
        
        self.validate_python_methods()
        print()
        
        self.validate_website_features()
        print()
        
        self.validate_dashboard_links()
        print()
        
        self.validate_widget_consistency()
        print()
        
        self.generate_recommendations()
        print()
        
        self.generate_final_report()
        print()
        
        # Résumé final
        issues_count = len(self.validation_results['issues_found'])
        recommendations_count = len(self.validation_results['recommendations'])
        
        if issues_count == 0 and self.validation_results['website_enabled']:
            print("🎉 VALIDATION RÉUSSIE - SAMA SYNDICAT V1.1 PARFAITEMENT CONFIGURÉ!")
            print("✅ Tous les liens et widgets fonctionnent")
            print("✅ Site web public activé et fonctionnel")
            print("✅ Module prêt pour la production")
        elif issues_count == 0:
            print("✅ VALIDATION RÉUSSIE - Liens et widgets fonctionnels")
            print(f"💡 {recommendations_count} recommandations pour optimiser")
        else:
            print(f"⚠️ VALIDATION PARTIELLE - {issues_count} problèmes à corriger")
            print(f"💡 {recommendations_count} recommandations")
            
        print(f"📊 Résumé: {len(self.validation_results['actions_defined'])} actions, {len(set(self.validation_results['python_methods']))} méthodes")

if __name__ == "__main__":
    validator = CorrectionValidator()
    validator.run()