# SAMA SYNDICAT - Guide de Développement

## 🚀 Démarrage Rapide

### Prérequis
- Odoo 18 CE installé dans `/var/odoo/odoo18`
- Environnement virtuel dans `/home/grand-as/odoo18-venv`
- PostgreSQL avec utilisateur `odoo/odoo`

### Installation et Test

1. **Validation syntaxique** (recommandé avant installation)
   ```bash
   python3 sama_syndicat/dev_scripts/validate_syntax.py
   ```

2. **Installation rapide**
   ```bash
   ./sama_syndicat/dev_scripts/quick_install.sh
   ```

3. **Démarrage du serveur de développement**
   ```bash
   python3 sama_syndicat/start_syndicat.py
   ```

### Scripts Disponibles

#### Scripts de Développement (`dev_scripts/`)
- `validate_syntax.py` : Validation syntaxique de tous les fichiers
- `quick_install.sh` : Installation rapide du module
- `simple_test.py` : Test complet avec création de base et démarrage serveur
- `test_module.py` : Test avancé avec gestion des erreurs

#### Script de Production
- `start_syndicat.py` : Script de démarrage pour la production

## 📁 Structure du Module

```
sama_syndicat/
├── __init__.py                     # Initialisation du module
├── __manifest__.py                 # Manifeste du module
├── start_syndicat.py              # Script de démarrage
├── README.md                      # Documentation utilisateur
├── DEVELOPMENT.md                 # Ce fichier
├── models/                        # Modèles de données
│   ├── __init__.py
│   ├── syndicat_adherent.py       # Gestion des adhérents
│   ├── syndicat_assemblee.py      # Assemblées et réunions
│   ├── syndicat_revendication.py  # Revendications syndicales
│   ├── syndicat_action.py         # Actions syndicales
│   ├── syndicat_communication.py  # Communications
│   ├── syndicat_formation.py      # Formations
│   ├── syndicat_convention.py     # Conventions collectives
│   ├── syndicat_mediation.py      # Médiations et conflits
│   ├── syndicat_dashboard.py      # Tableau de bord
│   └── res_partner.py             # Extension des contacts
├── controllers/                   # Contrôleurs web
│   ├── __init__.py
│   ├── main.py                    # Contrôleur principal
│   └── portal.py                  # Portail adhérents
├── views/                         # Vues et interfaces
│   ├── syndicat_adherent_views.xml
│   ├── syndicat_assemblee_views.xml
│   ├── syndicat_revendication_views.xml
│   ├── syndicat_action_views.xml
│   ├── syndicat_communication_views.xml
│   ├── syndicat_formation_views.xml
│   ├── syndicat_convention_views.xml
│   ├── syndicat_mediation_views.xml
│   ├── syndicat_dashboard_views.xml
│   └── menus.xml                  # Structure des menus
├── security/                      # Sécurité et droits d'accès
│   ├── security.xml               # Groupes et règles
│   └── ir.model.access.csv        # Droits d'accès aux modèles
├── data/                          # Données de base
│   ├── sequences.xml              # Séquences automatiques
│   └── data.xml                   # Données de démonstration
├── static/description/            # Ressources statiques
│   ├── icon.png                   # Icône du module
│   └── index.html                 # Description pour le store
└── dev_scripts/                   # Scripts de développement
    ├── validate_syntax.py
    ├── quick_install.sh
    ├── simple_test.py
    └── test_module.py
```

## 🔧 Configuration

### Port de Développement
Le module utilise le port **8070** pour éviter les conflits avec d'autres instances Odoo.

### Base de Données
- Test : `sama_syndicat_test`
- Production : `sama_syndicat_prod`

### Environnement
- Odoo 18 CE
- Python 3.11+
- PostgreSQL 13+

## 🧪 Tests et Validation

### Validation Syntaxique
```bash
python3 sama_syndicat/dev_scripts/validate_syntax.py
```

### Test d'Installation
```bash
./sama_syndicat/dev_scripts/quick_install.sh
```

### Test Complet
```bash
python3 sama_syndicat/dev_scripts/simple_test.py
```

## 🏗️ Architecture

### Modèles Principaux
1. **syndicat.adherent** : Gestion des adhérents et cotisations
2. **syndicat.assemblee** : Assemblées avec système de vote
3. **syndicat.revendication** : Revendications et négociations
4. **syndicat.action** : Actions syndicales (grèves, manifestations)
5. **syndicat.communication** : Communications multi-canaux
6. **syndicat.formation** : Formations avec certifications
7. **syndicat.convention** : Conventions collectives
8. **syndicat.mediation** : Gestion des conflits
9. **syndicat.dashboard** : Tableau de bord analytique

### Sécurité
- **6 groupes d'utilisateurs** : Adhérent, Utilisateur, Responsable, Secrétaire, Trésorier, Formateur
- **Règles d'accès par enregistrement** selon les rôles
- **Niveaux de confidentialité** pour les informations sensibles

### Vues
- **Kanban** : Vue par défaut pour tous les modèles
- **Liste** : Avec édition en masse (`multi_edit="1"`)
- **Formulaire** : Avec workflow et boutons d'action
- **Graphique** : Statistiques et analyses
- **Pivot** : Analyses croisées
- **Calendrier** : Pour les événements (assemblées, actions, formations)

## 🔄 Workflow de Développement

1. **Modification du code**
2. **Validation syntaxique** : `python3 dev_scripts/validate_syntax.py`
3. **Test d'installation** : `./dev_scripts/quick_install.sh`
4. **Test fonctionnel** : Démarrage du serveur et test manuel
5. **Commit des changements**

## 📊 Fonctionnalités Avancées

### Tableau de Bord
- Vue d'ensemble en temps réel
- Indicateurs clés de performance
- Alertes automatiques
- Actions rapides

### Communications
- Multi-canaux (Email, SMS, Web)
- Ciblage précis des destinataires
- Suivi des performances
- Workflow de validation

### Formations
- Gestion complète des inscriptions
- Suivi pédagogique
- Certifications
- Évaluations

### Médiations
- Gestion des conflits individuels/collectifs
- Processus de médiation structuré
- Suivi temporel
- Mesures de prévention

## 🚀 Déploiement

### Production
```bash
python3 sama_syndicat/start_syndicat.py
```

### Mise à jour
1. Arrêter le serveur
2. Mettre à jour le code
3. Redémarrer avec `--update=sama_syndicat`

## 📞 Support

- **Auteur** : POLITECH SÉNÉGAL
- **Email** : contact@politech.sn
- **Site** : https://www.politech.sn

## 📄 Licence

LGPL-3 - Voir le fichier LICENSE pour plus de détails.