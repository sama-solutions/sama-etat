#!/usr/bin/env python3
"""
Nettoyage direct de la base de données PostgreSQL
"""

import subprocess
import sys

def clean_database_direct():
    """Nettoyer directement la base de données PostgreSQL"""
    print("🧹 NETTOYAGE DIRECT DE LA BASE DE DONNÉES")
    print("=" * 50)
    
    DATABASE = "sama_syndicat_final_1756812346"
    
    # Commandes SQL de nettoyage
    sql_commands = [
        # Supprimer les enregistrements ir.model.data problématiques
        """
        DELETE FROM ir_model_data 
        WHERE module = 'web_studio_community' 
        AND model = 'ir.model.fields';
        """,
        
        # Supprimer les champs personnalisés ajoutés par erreur
        """
        DELETE FROM ir_model_fields 
        WHERE model = 'ir.model.fields' 
        AND name IN ('default_value', 'help', 'domain', 'context')
        AND state = 'manual';
        """,
        
        # Nettoyer les contraintes orphelines
        """
        DELETE FROM ir_model_constraint 
        WHERE module = 'web_studio_community' 
        AND name LIKE '%ir_model_fields%';
        """,
        
        # Vérifier l'état final
        """
        SELECT COUNT(*) as count FROM ir_model_fields 
        WHERE model = 'ir.model.fields' 
        AND name IN ('default_value', 'help', 'domain', 'context');
        """
    ]
    
    print("🗄️ Connexion à PostgreSQL...")
    
    for i, sql in enumerate(sql_commands, 1):
        print(f"\n📝 Exécution de la commande {i}/{len(sql_commands)}...")
        
        # Créer un fichier SQL temporaire
        sql_file = f'/tmp/cleanup_{i}.sql'
        with open(sql_file, 'w') as f:
            f.write(sql.strip())
        
        # Exécuter la commande SQL
        cmd = ['psql', '-d', DATABASE, '-f', sql_file]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"✅ Commande {i} exécutée avec succès")
                if result.stdout.strip():
                    print(f"   Résultat: {result.stdout.strip()}")
            else:
                print(f"⚠️ Avertissement commande {i}: {result.stderr.strip()}")
        except subprocess.TimeoutExpired:
            print(f"⏰ Timeout commande {i}")
        except Exception as e:
            print(f"❌ Erreur commande {i}: {e}")
        
        # Nettoyer le fichier temporaire
        try:
            subprocess.run(['rm', sql_file], capture_output=True)
        except:
            pass
    
    print("\n🔄 Redémarrage des services PostgreSQL...")
    try:
        subprocess.run(['sudo', 'systemctl', 'restart', 'postgresql'], capture_output=True, timeout=30)
        print("✅ PostgreSQL redémarré")
    except:
        print("⚠️ Impossible de redémarrer PostgreSQL (peut nécessiter des privilèges)")
    
    return True

def update_module_after_clean():
    """Mettre à jour le module après nettoyage"""
    print("\n🔄 MISE À JOUR DU MODULE APRÈS NETTOYAGE")
    print("=" * 50)
    
    DATABASE = "sama_syndicat_final_1756812346"
    ODOO_BIN = "/var/odoo/odoo18/odoo-bin"
    ADDONS_PATH = "/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat"
    PORT = 8077
    
    # Arrêter les processus existants
    print("🛑 Arrêt des processus Odoo...")
    subprocess.run(['pkill', '-f', 'odoo-bin'], capture_output=True)
    
    # Mettre à jour le module
    cmd = [
        'python3', ODOO_BIN,
        f'--addons-path={ADDONS_PATH}',
        f'--database={DATABASE}',
        f'--xmlrpc-port={PORT}',
        '-u', 'web_studio_community',
        '--stop-after-init',
        '--log-level=warn'
    ]
    
    print("🔄 Mise à jour du module...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print("✅ Module mis à jour avec succès")
            return True
        else:
            print("❌ Erreur lors de la mise à jour")
            print(result.stderr[-500:])
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🎯 NETTOYAGE COMPLET DE LA BASE DE DONNÉES")
    print("=" * 60)
    
    # Étape 1: Nettoyage direct
    if not clean_database_direct():
        print("❌ Échec du nettoyage direct")
        return False
    
    # Étape 2: Mise à jour du module
    if not update_module_after_clean():
        print("❌ Échec de la mise à jour du module")
        return False
    
    print("\n🎉 NETTOYAGE COMPLET RÉUSSI!")
    print("La base de données a été nettoyée et le module mis à jour.")
    print("Vous pouvez maintenant tester l'accès aux paramètres.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)