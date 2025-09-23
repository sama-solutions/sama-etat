# SAMA SYNDICAT - Guide d'Installation

## 🎯 Installation Autonome Complète

Le module **SAMA SYNDICAT** est maintenant prêt pour l'installation autonome avec tous les scripts nécessaires.

## 📋 Prérequis Vérifiés

✅ **Odoo 18 CE** installé dans `/var/odoo/odoo18`  
✅ **Environnement virtuel** dans `/home/grand-as/odoo18-venv`  
✅ **PostgreSQL** avec utilisateur `odoo/odoo`  
✅ **Custom addons** dans `/home/grand-as/psagsn/custom_addons`  
✅ **Port dédié** 8070 (pas de conflit)  
✅ **Syntaxe validée** pour tous les fichiers  

## 🚀 Installation et Démarrage

### Option 1: Script Bash Simple (Recommandé)
```bash
./sama_syndicat/install_and_start.sh
```

### Option 2: Script Python Complet
```bash
python3 sama_syndicat/launch_sama_syndicat.py
```

### Option 3: Installation Manuelle
```bash
# 1. Activer l'environnement
source /home/grand-as/odoo18-venv/bin/activate

# 2. Arrêter les processus sur le port 8070
pkill -f "xmlrpc-port=8070"

# 3. Créer la base
createdb -U odoo -O odoo sama_syndicat_prod

# 4. Installer le module
cd /var/odoo/odoo18
python3 odoo-bin \
    --addons-path=/home/grand-as/psagsn/custom_addons \
    --database=sama_syndicat_prod \
    --db_user=odoo \
    --db_password=odoo \
    --init=sama_syndicat \
    --stop-after-init \
    --log-level=info

# 5. Démarrer le serveur
python3 odoo-bin \
    --addons-path=/home/grand-as/psagsn/custom_addons \
    --database=sama_syndicat_prod \
    --db_user=odoo \
    --db_password=odoo \
    --xmlrpc-port=8070 \
    --log-level=info
```

## 🌐 Accès au Module

- **URL** : http://localhost:8070
- **Base de données** : sama_syndicat_prod
- **Utilisateur** : admin
- **Mot de passe** : admin (à changer lors de la première connexion)

## 📊 Fonctionnalités Disponibles

### 🏛️ Menu Principal : Syndicat
1. **Tableau de Bord** - Vue d'ensemble avec KPI
2. **Adhérents** - Gestion complète des membres
3. **Assemblées** - Organisation et votes
4. **Revendications** - Suivi des négociations
5. **Actions Syndicales** - Manifestations et grèves
6. **Communications** - Multi-canaux avec analytics
7. **Formations** - Programmes et certifications
8. **Conventions** - Conventions collectives
9. **Médiations** - Gestion des conflits

### 🎨 Vues Activées
- ✅ **Kanban** - Vue par défaut avec cartes
- ✅ **Liste** - Tableaux avec édition en masse
- ✅ **Formulaire** - Formulaires détaillés
- ✅ **Graphique** - Statistiques et analyses
- ✅ **Pivot** - Analyses croisées
- ✅ **Calendrier** - Planning des événements
- ✅ **Dashboard** - Tableaux de bord interactifs

## 🔧 Scripts de Développement

### Dans `dev_scripts/`
- `validate_syntax.py` - Validation syntaxique
- `final_test.sh` - Test complet d'installation
- `autonomous_install.py` - Installation autonome avancée
- `iterative_test.py` - Tests itératifs avec corrections
- `module_summary.py` - Résumé du module

### Scripts Principaux
- `install_and_start.sh` - Installation et démarrage simple
- `launch_sama_syndicat.py` - Lanceur complet avec vérifications

## 🔒 Sécurité Configurée

### Groupes d'Utilisateurs
1. **Adhérent** - Accès limité aux données personnelles
2. **Utilisateur** - Accès lecture/écriture aux données courantes
3. **Secrétaire** - Gestion des communications et assemblées
4. **Trésorier** - Gestion des cotisations et finances
5. **Formateur** - Gestion des formations
6. **Responsable** - Accès complet à toutes les données

### Règles d'Accès
- Règles par enregistrement selon les rôles
- Confidentialité des données sensibles
- Accès contrôlé aux fonctionnalités

## 🧪 Tests et Validation

### Validation Syntaxique
```bash
python3 sama_syndicat/dev_scripts/validate_syntax.py
```

### Test d'Installation
```bash
./sama_syndicat/dev_scripts/final_test.sh
```

### Résumé du Module
```bash
python3 sama_syndicat/dev_scripts/module_summary.py
```

## 📈 Statistiques du Module

- **38 fichiers** créés (11,694+ lignes de code)
- **10 modèles** de données complets
- **13 vues XML** avec toutes les fonctionnalités
- **6 groupes** de sécurité
- **9 scripts** de développement et test

## 🎉 Première Utilisation

1. **Démarrer le serveur** avec un des scripts
2. **Accéder à** http://localhost:8070
3. **Se connecter** avec admin/admin
4. **Aller dans Apps** > Rechercher "SAMA SYNDICAT"
5. **Commencer la configuration** des adhérents
6. **Explorer les fonctionnalités** via le menu Syndicat

## 🔄 Cycle de Développement

Pour les modifications futures :

1. **Modifier le code**
2. **Valider** : `python3 dev_scripts/validate_syntax.py`
3. **Tester** : `./dev_scripts/final_test.sh`
4. **Redémarrer** : `./install_and_start.sh`

## 📞 Support

- **Développeur** : POLITECH SÉNÉGAL
- **Email** : contact@politech.sn
- **Documentation** : README.md et DEVELOPMENT.md

---

🏛️ **SAMA SYNDICAT** - Gestion Zéro Papier pour Syndicats et Groupements Professionnels