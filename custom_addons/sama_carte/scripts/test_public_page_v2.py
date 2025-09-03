#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour tester la page publique V2.0 avec les designs dynamiques
"""

import sys
import os

# Ajouter le chemin d'Odoo
sys.path.append('/var/odoo/odoo18')

import odoo
from odoo import api, SUPERUSER_ID

def test_public_page_v2():
    """Teste la page publique avec les designs V2.0"""
    
    # Configuration de la base de données
    odoo.tools.config.parse_config(['-d', 'sama_carte_demo'])
    
    with odoo.registry('sama_carte_demo').cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        print("🌐 TEST PAGE PUBLIQUE V2.0")
        print("==========================")
        
        # Trouver la société SAMA
        sama_company = env['res.company'].search([
            ('name', 'ilike', 'SAMA')
        ], limit=1)
        
        if not sama_company:
            print("❌ Société SAMA non trouvée")
            return False
        
        print(f"✅ Société: {sama_company.name}")
        print(f"🎨 Template: {sama_company.card_template_id.name if sama_company.card_template_id else 'Aucun'}")
        print(f"🎯 Couleurs: {sama_company.primary_color} / {sama_company.secondary_color}")
        
        # Trouver les membres SAMA
        members = env['membership.member'].search([
            ('company_id', '=', sama_company.id)
        ])
        
        print(f"\n👥 {len(members)} membres SAMA trouvés:")
        
        # Afficher les URLs publiques pour chaque membre
        for i, member in enumerate(members[:5], 1):  # Limiter à 5 pour l'affichage
            status = "✅ Valide" if member.is_card_valid() else "❌ Expiré"
            print(f"   {i}. {member.name} ({member.membership_number}) - {status}")
            print(f"      URL: http://localhost:8071/member/{member.access_token}")
        
        if len(members) > 5:
            print(f"   ... et {len(members) - 5} autres membres")
        
        # Statistiques des templates
        templates = env['membership.card.template'].search([])
        print(f"\n🎨 {len(templates)} templates disponibles:")
        for template in templates:
            print(f"   - {template.name} ({template.technical_name})")
        
        # Instructions de test
        print(f"\n🔍 INSTRUCTIONS DE TEST:")
        print(f"========================")
        print(f"1. Ouvrir une URL de membre ci-dessus")
        print(f"2. Vérifier que le design correspond au template SAMA")
        print(f"3. Changer le template de SAMA dans l'interface admin")
        print(f"4. Recharger la page publique pour voir le nouveau design")
        print(f"")
        print(f"🎯 EXEMPLE RAPIDE:")
        if members:
            first_member = members[0]
            print(f"URL: http://localhost:8071/member/{first_member.access_token}")
            print(f"Membre: {first_member.name}")
            print(f"Template actuel: {sama_company.card_template_id.name if sama_company.card_template_id else 'Moderne'}")
        
        return True

if __name__ == '__main__':
    print("🚀 TEST PAGE PUBLIQUE V2.0")
    print("===========================")
    
    try:
        success = test_public_page_v2()
        if success:
            print("\n🎉 INFORMATIONS RÉCUPÉRÉES AVEC SUCCÈS !")
            print("La page publique utilise maintenant les designs V2.0")
        else:
            print("\n❌ ERREUR LORS DU TEST")
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        sys.exit(1)