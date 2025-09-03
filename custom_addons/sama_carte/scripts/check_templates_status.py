#!/usr/bin/env python3
"""
Script pour vérifier et corriger l'état des templates de cartes
"""

import psycopg2
import sys

def check_templates():
    try:
        # Connexion à la base de données
        conn = psycopg2.connect(
            host="localhost",
            database="sama_carte_demo",
            user="odoo",
            password="odoo"
        )
        cur = conn.cursor()
        
        print("🔍 VÉRIFICATION DE L'ÉTAT DES TEMPLATES")
        print("=" * 50)
        
        # Vérifier tous les templates
        cur.execute("""
            SELECT id, name, technical_name, active, sequence 
            FROM membership_card_template 
            ORDER BY sequence, name
        """)
        
        templates = cur.fetchall()
        
        print(f"\n📊 TEMPLATES TROUVÉS: {len(templates)}")
        print("-" * 30)
        
        active_count = 0
        inactive_count = 0
        
        for template in templates:
            id_val, name, tech_name, active, sequence = template
            status = "✅ ACTIF" if active else "❌ INACTIF"
            print(f"{status} | {sequence:2d} | {name} ({tech_name})")
            
            if active:
                active_count += 1
            else:
                inactive_count += 1
        
        print(f"\n📈 RÉSUMÉ:")
        print(f"✅ Templates actifs: {active_count}")
        print(f"❌ Templates inactifs: {inactive_count}")
        
        # Corriger si nécessaire
        if active_count != 3:
            print(f"\n⚠️  PROBLÈME DÉTECTÉ: {active_count} templates actifs au lieu de 3")
            print("🔧 CORRECTION EN COURS...")
            
            # Désactiver tous d'abord
            cur.execute("UPDATE membership_card_template SET active = false")
            
            # Activer seulement les 3 souhaités
            templates_to_activate = ['modern', 'dynamic', 'unified']
            
            for i, tech_name in enumerate(templates_to_activate, 1):
                cur.execute("""
                    UPDATE membership_card_template 
                    SET active = true, sequence = %s 
                    WHERE technical_name = %s
                """, (i, tech_name))
                
                if cur.rowcount > 0:
                    print(f"✅ Activé: {tech_name} (séquence {i})")
                else:
                    print(f"❌ Échec: {tech_name} non trouvé")
            
            # Créer le template unifié s'il n'existe pas
            cur.execute("SELECT id FROM membership_card_template WHERE technical_name = 'unified'")
            if not cur.fetchone():
                print("➕ Création du template 'unified'...")
                cur.execute("""
                    INSERT INTO membership_card_template 
                    (name, technical_name, description, category, sequence, is_premium, active, 
                     default_primary_color, default_secondary_color, default_text_color, create_date, write_date)
                    VALUES 
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                """, (
                    'Unifié & Élégant',
                    'unified',
                    'Design unifié avec photo et QR code en haut, informations centrées. Background personnalisable dans un cadre élégant.',
                    'modern',
                    3,
                    False,
                    True,
                    '#004a99',
                    '#f7f32d',
                    '#ffffff'
                ))
                print("✅ Template 'unified' créé")
            
            conn.commit()
            print("✅ Corrections appliquées")
            
            # Vérifier à nouveau
            print("\n🔍 VÉRIFICATION POST-CORRECTION:")
            cur.execute("""
                SELECT name, technical_name, active, sequence 
                FROM membership_card_template 
                WHERE active = true
                ORDER BY sequence
            """)
            
            active_templates = cur.fetchall()
            for template in active_templates:
                name, tech_name, active, sequence = template
                print(f"✅ {sequence} | {name} ({tech_name})")
        
        else:
            print("✅ Configuration correcte: 3 templates actifs")
        
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = check_templates()
    sys.exit(0 if success else 1)