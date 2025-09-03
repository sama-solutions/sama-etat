#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour associer tous les membres existants à la société SAMA
et configurer les templates par défaut
"""

import sys
import os

# Ajouter le chemin d'Odoo
sys.path.append('/var/odoo/odoo18')

import odoo
from odoo import api, SUPERUSER_ID

def update_members_to_sama():
    """Met à jour tous les membres pour les associer à SAMA"""
    
    # Configuration de la base de données
    odoo.tools.config.parse_config(['-d', 'sama_carte_demo'])
    
    with odoo.registry('sama_carte_demo').cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        print("🔄 Mise à jour des membres pour SAMA...")
        
        # Trouver ou créer la société SAMA
        sama_company = env['res.company'].search([
            ('name', 'ilike', 'SAMA')
        ], limit=1)
        
        if not sama_company:
            print("❌ Société SAMA non trouvée")
            return False
        
        print(f"✅ Société SAMA trouvée: {sama_company.name}")
        
        # Trouver tous les membres sans société ou avec une autre société
        members_to_update = env['membership.member'].search([
            '|',
            ('company_id', '=', False),
            ('company_id', '!=', sama_company.id)
        ])
        
        print(f"📋 {len(members_to_update)} membres à mettre à jour")
        
        # Mettre à jour les membres
        if members_to_update:
            members_to_update.write({'company_id': sama_company.id})
            print(f"✅ {len(members_to_update)} membres associés à SAMA")
            
            # Afficher la liste des membres mis à jour
            for member in members_to_update:
                print(f"   - {member.name} ({member.membership_number})")
        
        # Configurer le template par défaut pour SAMA
        template_modern = env['membership.card.template'].search([
            ('technical_name', '=', 'modern')
        ], limit=1)
        
        if template_modern and not sama_company.card_template_id:
            sama_company.write({'card_template_id': template_modern.id})
            print(f"✅ Template moderne assigné à SAMA")
        
        # Régénérer les QR codes pour tous les membres
        all_members = env['membership.member'].search([
            ('company_id', '=', sama_company.id)
        ])
        
        print(f"🔄 Régénération des QR codes pour {len(all_members)} membres...")
        for member in all_members:
            member._compute_qr_code()
        
        print("✅ QR codes régénérés")
        
        # Statistiques finales
        total_members = len(all_members)
        valid_members = len(all_members.filtered(lambda m: m.is_card_valid()))
        
        print(f"\n📊 STATISTIQUES SAMA:")
        print(f"   Total membres: {total_members}")
        print(f"   Membres actifs: {valid_members}")
        print(f"   Membres expirés: {total_members - valid_members}")
        print(f"   Template: {sama_company.card_template_id.name if sama_company.card_template_id else 'Aucun'}")
        print(f"   Couleurs: {sama_company.primary_color} / {sama_company.secondary_color}")
        
        cr.commit()
        return True

if __name__ == '__main__':
    print("🚀 MISE À JOUR MEMBRES SAMA")
    print("============================")
    
    try:
        success = update_members_to_sama()
        if success:
            print("\n🎉 MISE À JOUR TERMINÉE AVEC SUCCÈS !")
            print("Les membres sont maintenant associés à SAMA")
            print("Vous pouvez tester les designs avec des données réelles")
        else:
            print("\n❌ ERREUR LORS DE LA MISE À JOUR")
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        sys.exit(1)