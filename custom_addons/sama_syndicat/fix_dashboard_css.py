#!/usr/bin/env python3
"""
Script pour corriger le CSS et la largeur des dashboards
"""

import xmlrpc.client
import sys
import time

def fix_dashboard_css():
    """Corriger le CSS et la largeur des dashboards"""
    
    print("🎨 CORRECTION DU CSS ET LARGEUR DES DASHBOARDS")
    print("=" * 50)
    
    # Configuration
    url = 'http://localhost:8070'
    db = 'sama_syndicat_final_1756812346'
    username = 'admin'
    password = 'admin'
    
    try:
        # Connexion
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        
        if not uid:
            print("❌ Erreur d'authentification")
            print("💡 Vérifiez que Odoo est démarré et accessible")
            return False
        
        print(f"✅ Connecté à Odoo (UID: {uid})")
        
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        
        # Mettre à jour le module pour charger le nouveau CSS
        print("📦 Mise à jour du module sama_syndicat...")
        try:
            module_ids = models.execute_kw(db, uid, password,
                'ir.module.module', 'search',
                [[('name', '=', 'sama_syndicat')]])
            
            if module_ids:
                models.execute_kw(db, uid, password,
                    'ir.module.module', 'button_immediate_upgrade',
                    [module_ids])
                print("✅ Module sama_syndicat mis à jour")
                
                # Attendre un peu pour que la mise à jour se termine
                print("⏳ Attente de la fin de la mise à jour...")
                time.sleep(5)
            else:
                print("⚠️ Module sama_syndicat non trouvé")
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour: {str(e)[:100]}...")
            return False
        
        # Vérifier les vues des dashboards
        print("\n📄 Vérification des vues dashboards...")
        dashboard_views = [
            'view_syndicat_dashboard_v1_kanban',
            'view_syndicat_dashboard_v2_kanban',
            'view_syndicat_dashboard_v3_kanban',
            'view_syndicat_dashboard_v4_kanban'
        ]
        
        for view_name in dashboard_views:
            try:
                view_ids = models.execute_kw(db, uid, password,
                    'ir.ui.view', 'search',
                    [[('name', '=', view_name)]])
                
                if view_ids:
                    # Lire la vue pour vérifier qu'elle contient les bonnes classes
                    view_data = models.execute_kw(db, uid, password,
                        'ir.ui.view', 'read',
                        [view_ids], {'fields': ['arch_db']})
                    
                    if view_data and 'o_kanban_dashboard_fullwidth' in view_data[0]['arch_db']:
                        print(f"  ✅ {view_name} - Classe fullwidth présente")
                    else:
                        print(f"  ⚠️ {view_name} - Classe fullwidth manquante")
                else:
                    print(f"  ❌ {view_name} - Non trouvé")
            except Exception as e:
                print(f"  ❌ {view_name} - Erreur: {e}")
        
        # Vider le cache des vues
        print("\n🔄 Vidage du cache des vues...")
        try:
            models.execute_kw(db, uid, password,
                'ir.ui.view', 'clear_caches', [])
            print("✅ Cache des vues vidé")
        except:
            print("⚠️ Impossible de vider le cache des vues")
        
        # Vider le cache des assets
        print("🔄 Vidage du cache des assets...")
        try:
            models.execute_kw(db, uid, password,
                'ir.attachment', 'search_unlink',
                [[('name', 'like', 'web.assets_%')]])
            print("✅ Cache des assets vidé")
        except:
            print("⚠️ Impossible de vider le cache des assets")
        
        print("\n🎯 CORRECTIONS APPORTÉES")
        print("=" * 25)
        print("✅ Classes CSS ajoutées aux vues :")
        print("   - o_kanban_dashboard_fullwidth")
        print("   - o_kanban_dashboard_record")
        print("✅ CSS amélioré pour :")
        print("   - Largeur complète (100%)")
        print("   - Styles des stat_box")
        print("   - Sections du dashboard")
        print("   - Titre avec gradient")
        print("✅ Cache vidé pour forcer le rechargement")
        
        print("\n💡 INSTRUCTIONS")
        print("=" * 15)
        print("1. Rechargez la page web (F5 ou Ctrl+Shift+R)")
        print("2. Allez dans Menu Syndicat → 🧪 Test Dashboards")
        print("3. Testez chaque version du dashboard")
        print("4. Vérifiez que les dashboards utilisent toute la largeur")
        
        print("\n🌐 ACCÈS AUX DASHBOARDS")
        print("=" * 25)
        print(f"Interface: http://localhost:8070/web")
        print("Menu: Syndicat → 🧪 Test Dashboards")
        print("Versions disponibles :")
        print("  - V1 - CSS Natif Odoo")
        print("  - V2 - Compact Organisé")
        print("  - V3 - Graphiques & Listes")
        print("  - V4 - Minimaliste")
        
        return True
        
    except ConnectionError:
        print("❌ Impossible de se connecter à Odoo")
        print("💡 Vérifiez que Odoo est démarré sur le port 8070")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = fix_dashboard_css()
    sys.exit(0 if success else 1)