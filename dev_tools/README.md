# Dev Tools - Outils de Développement

Ce dossier contient tous les outils et fichiers de développement qui ne sont pas nécessaires pour l'installation de production de SAMA ÉTAT.

## Structure

### 📁 scripts/
Contient tous les scripts de développement et d'utilitaires :
- `check_xml_syntax.sh` - Vérification de la syntaxe XML
- `create_backup.sh` - Script de création de sauvegardes
- `fix_odoo_views.py` - Correction des vues Odoo
- `odoo18_startup.sh` - Script de démarrage Odoo 18
- `publish_github.sh` - Script de publication GitHub
- `regenerate_assets.sh` - Régénération des assets
- `release_v1.3.sh` - Script de release v1.3
- `start_odoo_detached.sh` - Démarrage Odoo en arrière-plan
- `test_oauth.py` - Tests OAuth
- `validate_map_data.py` - Validation des données cartographiques

### 📁 config/
Fichiers de configuration de développement :
- `odoo.conf` - Configuration Odoo de développement
- `client_secret_*.json` - Secrets OAuth (ne pas committer en production)

### 📁 logs/
Fichiers de logs de développement :
- `odoo.log` - Logs Odoo
- `odoo_tasks_update.log` - Logs de mise à jour des tâches

### 📁 backup_files/
Archives et fichiers de sauvegarde :
- `project_public_sn_tabs_security.zip` - Archive de sécurité

## Usage

Ces fichiers sont utiles pour :
- Le développement local
- Les tests et le débogage
- La maintenance et les sauvegardes
- Les scripts d'automatisation

## Note Importante

⚠️ **Ces fichiers ne doivent PAS être inclus dans les déploiements de production.**

Ils sont exclus du repository principal via `.gitignore` pour maintenir un code propre et sécurisé.