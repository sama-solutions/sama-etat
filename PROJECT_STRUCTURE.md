# Structure du Projet SAMA ÉTAT

<div align="center">
  <img src="logo.png" alt="SAMA ÉTAT Logo" width="150"/>
  
  **Organisation et Architecture du Projet**
  
  *Project Organization and Architecture*
</div>

---

## 📁 Structure des Dossiers | Folder Structure

```
sama_etat/
├── 📄 README.md                    # Documentation principale (FR/EN)
├── 📄 README.fr.md                 # Documentation française
├── 📄 QUICK_START.md               # Guide de démarrage rapide
├── 📄 CONTRIBUTING.md              # Guide de contribution
├── 📄 CHANGELOG.md                 # Journal des modifications
├── 📄 SECURITY.md                  # Politique de sécurité
├── 📄 PROJECT_STRUCTURE.md         # Ce fichier
├── 📄 LICENSE                      # Licence LGPL-3.0
├── 📄 .gitignore                   # Fichiers à ignorer par Git
├── 📄 __init__.py                  # Module Python principal
├── 📄 __manifest__.py              # Manifeste Odoo
├── 🖼️ logo.png                     # Logo officiel SAMA ÉTAT
│
├── 📁 .github/                     # Configuration GitHub
│   ├── 📁 ISSUE_TEMPLATE/          # Templates d'issues
│   │   ├── 📄 bug_report.md        # Template rapport de bug
│   │   ├── 📄 feature_request.md   # Template demande de fonctionnalité
│   │   └── 📄 question.md          # Template question
│   ├── 📁 workflows/               # GitHub Actions
│   │   └── 📄 ci.yml               # Pipeline CI/CD
│   └── 📄 pull_request_template.md # Template Pull Request
│
├── 📁 config/                      # Configuration
│   ├── 📄 odoo.conf                # Configuration Odoo production
│   └── 📄 odoo.test.conf           # Configuration Odoo test
│
├── 📁 scripts/                     # Scripts utilitaires
│   ├── 📄 entrypoint.sh            # Script d'entrée Docker
│   ├── 📄 test_entrypoint.sh       # Script d'entrée tests
│   └── 📄 init_db.sql              # Initialisation base de données
│
├── 📁 tests/                       # Tests
│   ├── 📄 __init__.py              # Module tests
│   └── 📄 test_models.py           # Tests des modèles
│
├── 📁 archive_files/               # Fichiers archivés
│   ├── 📄 check_xml_syntax.sh      # Scripts de développement
│   ├── 📄 create_backup.sh         # Scripts de sauvegarde
│   ├── 📄 restore_backup.sh        # Scripts de restauration
│   ├── 📄 fix_odoo_views.py        # Scripts de correction
│   ├── 📄 fix_odoo_views_lxml.py   # Scripts de correction
│   ├── 📄 validate_map_data.py     # Scripts de validation
│   ├── 📄 odoo_tasks_update.log    # Logs de développement
│   ├── 📄 project_public_sn_tabs_security.zip # Archives
│   └── 📄 odoo.conf                # Ancienne configuration
│
├── 📁 controllers/                 # Contrôleurs Odoo
├── 📁 data/                        # Données de démonstration
├── 📁 models/                      # Modèles de données
├── 📁 security/                    # Sécurité et permissions
├── 📁 static/                      # Ressources statiques
│   ├── 📁 description/             # Description du module
│   │   └── 📁 screenshots/         # Captures d'écran
│   └── 📁 lib/                     # Bibliothèques externes
│       └── 📁 leaflet/             # Cartographie
├── 📁 views/                       # Vues et interfaces
├── 📁 websitecontent/              # Contenu web public
├── 📁 wizard/                      # Assistants
├── 📁 fiche_project_public_sn/     # Module intégré
│
├── 🐳 Dockerfile                   # Image Docker production
├── 🐳 Dockerfile.test              # Image Docker tests
├── 🐳 docker-compose.yml           # Orchestration Docker
├── 🐳 docker-compose.test.yml      # Tests Docker
├── 📄 requirements.txt             # Dépendances Python
├── 📄 pyproject.toml               # Configuration outils Python
├── 📄 pytest.ini                  # Configuration pytest
└── 📄 Makefile                     # Automatisation des tâches
```

---

## 🏗️ Architecture du Module | Module Architecture

### 📊 Modèles de Données | Data Models

| Modèle | Description | Fichier |
|--------|-------------|---------|
| `government.project` | Projets gouvernementaux | `models/government_project.py` |
| `government.decision` | Décisions officielles | `models/government_decision.py` |
| `government.event` | Événements publics | `models/government_event.py` |
| `government.budget` | Budgets et finances | `models/government_budget.py` |
| `government.ministry` | Ministères | `models/government_ministry.py` |
| `strategic.plan` | Plans stratégiques | `models/strategic_plan.py` |
| `strategic.pillar` | Piliers stratégiques | `models/strategic_pillar.py` |
| `strategic.axis` | Axes stratégiques | `models/strategic_axis.py` |
| `strategic.objective` | Objectifs stratégiques | `models/strategic_objective.py` |
| `strategic.kpi` | Indicateurs de performance | `models/strategic_kpi.py` |

### 🎨 Vues et Interfaces | Views & Interfaces

| Type | Description | Répertoire |
|------|-------------|------------|
| **Vues Backend** | Interface d'administration | `views/` |
| **Vues Frontend** | Interface publique | `websitecontent/` |
| **Templates Web** | Pages web publiques | `views/public_*.xml` |
| **Assistants** | Wizards et formulaires | `wizard/` |
| **Tableaux de Bord** | Dashboards et métriques | `views/dashboard_*.xml` |

### 🔐 Sécurité | Security

| Composant | Description | Fichier |
|-----------|-------------|---------|
| **Groupes** | Rôles utilisateurs | `security/security.xml` |
| **Permissions** | Droits d'accès | `security/ir.model.access.csv` |
| **Règles** | Règles de sécurité | `security/security.xml` |

### 📊 Données | Data

| Type | Description | Répertoire |
|------|-------------|------------|
| **Données de Base** | Configuration initiale | `data/` |
| **Données Démo** | Exemples et tests | `data/*_demo_data.xml` |
| **Traductions** | Fichiers de langue | `i18n/` |

---

## 🔧 Configuration et Déploiement | Configuration & Deployment

### 🐳 Docker

| Fichier | Usage | Description |
|---------|-------|-------------|
| `Dockerfile` | Production | Image optimisée pour la production |
| `Dockerfile.test` | Tests | Image avec outils de test |
| `docker-compose.yml` | Développement | Orchestration complète |
| `docker-compose.test.yml` | Tests | Environnement de test |

### ⚙️ Configuration

| Fichier | Usage | Description |
|---------|-------|-------------|
| `config/odoo.conf` | Production | Configuration Odoo optimisée |
| `config/odoo.test.conf` | Tests | Configuration pour tests |
| `pyproject.toml` | Développement | Configuration outils Python |
| `pytest.ini` | Tests | Configuration pytest |

### 🔨 Automatisation

| Fichier | Usage | Description |
|---------|-------|-------------|
| `Makefile` | Développement | Commandes automatisées |
| `.github/workflows/ci.yml` | CI/CD | Pipeline d'intégration continue |
| `scripts/entrypoint.sh` | Docker | Script de démarrage |
| `scripts/test_entrypoint.sh` | Tests | Script de test |

---

## 📋 Conventions de Nommage | Naming Conventions

### 📁 Fichiers et Dossiers | Files & Folders

| Type | Convention | Exemple |
|------|------------|---------|
| **Modèles** | `snake_case.py` | `government_project.py` |
| **Vues** | `model_name_views.xml` | `government_project_views.xml` |
| **Données** | `description_data.xml` | `ministries_demo_data.xml` |
| **Tests** | `test_*.py` | `test_models.py` |
| **Scripts** | `action_script.sh` | `entrypoint.sh` |

### 🏷️ Identifiants XML | XML IDs

| Type | Convention | Exemple |
|------|------------|---------|
| **Modèles** | `model_name` | `government_project` |
| **Vues** | `model_name_view_type` | `government_project_form` |
| **Actions** | `model_name_action` | `government_project_action` |
| **Menus** | `menu_description` | `menu_government_projects` |
| **Groupes** | `group_description` | `group_project_manager` |

### 🐍 Code Python | Python Code

| Type | Convention | Exemple |
|------|------------|---------|
| **Classes** | `PascalCase` | `GovernmentProject` |
| **Méthodes** | `snake_case` | `compute_progress` |
| **Variables** | `snake_case` | `project_budget` |
| **Constantes** | `UPPER_CASE` | `DEFAULT_CURRENCY` |

---

## 🧪 Tests et Qualité | Testing & Quality

### 🔍 Types de Tests | Test Types

| Type | Description | Commande |
|------|-------------|----------|
| **Unitaires** | Tests des modèles et méthodes | `make test-unit` |
| **Intégration** | Tests Odoo complets | `make test-integration` |
| **Fonctionnels** | Tests end-to-end | `make test-functional` |
| **Performance** | Tests de charge | `make test-performance` |
| **Sécurité** | Analyse de vulnérabilités | `make security` |

### 📊 Métriques de Qualité | Quality Metrics

| Métrique | Objectif | Outil |
|----------|----------|-------|
| **Couverture de tests** | > 80% | pytest-cov |
| **Conformité PEP 8** | 100% | flake8 |
| **Formatage** | 100% | black |
| **Tri des imports** | 100% | isort |
| **Typage** | > 90% | mypy |
| **Sécurité** | 0 vulnérabilité critique | bandit, safety |

---

## 📚 Documentation | Documentation

### 📖 Types de Documentation | Documentation Types

| Type | Audience | Fichiers |
|------|----------|----------|
| **Utilisateur** | Utilisateurs finaux | `README.md`, `QUICK_START.md` |
| **Développeur** | Contributeurs | `CONTRIBUTING.md`, `PROJECT_STRUCTURE.md` |
| **Administrateur** | Administrateurs système | `DEPLOYMENT_GUIDE.md`, `SECURITY.md` |
| **API** | Intégrateurs | `API_DOCS.md` |

### 🌍 Langues Supportées | Supported Languages

| Langue | Code | Statut |
|--------|------|--------|
| **Français** | `fr_FR` | ✅ Complet |
| **Anglais** | `en_US` | ✅ Complet |
| **Wolof** | `wo_SN` | 🔄 En cours |
| **Pulaar** | `ff_SN` | 📋 Planifié |

---

## 🚀 Déploiement | Deployment

### 🌍 Environnements | Environments

| Environnement | URL | Description |
|---------------|-----|-------------|
| **Développement** | `localhost:8069` | Environnement local |
| **Test** | `test.sama-etat.sn` | Tests automatisés |
| **Staging** | `staging.sama-etat.sn` | Pré-production |
| **Production** | `sama-etat.sn` | Production officielle |

### 📦 Versions | Versions

| Version | Statut | Date | Description |
|---------|--------|------|-------------|
| **1.0.0** | ✅ Stable | 2024-01-15 | Version initiale |
| **1.1.0** | 🔄 Développement | TBD | Améliorations UX |
| **2.0.0** | 📋 Planifié | TBD | Nouvelles fonctionnalités |

---

## 🤝 Contribution | Contributing

### 👥 Équipe | Team

| Rôle | Nom | Email |
|------|-----|-------|
| **Architecte Principal** | Mamadou Mbagnick DOGUE | mamadou@sama-etat.sn |
| **Développeur Senior** | Rassol DOGUE | rassol@sama-etat.sn |

### 🔄 Workflow de Contribution | Contribution Workflow

1. **Fork** du repository
2. **Création** d'une branche feature
3. **Développement** avec tests
4. **Tests** et validation qualité
5. **Pull Request** avec description
6. **Review** par l'équipe
7. **Merge** après approbation

### 📋 Standards | Standards

- **Code** : PEP 8, Black formatting
- **Commits** : Conventional Commits
- **Branches** : GitFlow
- **Tests** : Couverture > 80%
- **Documentation** : Bilingue FR/EN

---

## 📞 Support | Support

### 🆘 Canaux de Support | Support Channels

| Canal | Usage | Réponse |
|-------|-------|---------|
| **GitHub Issues** | Bugs et fonctionnalités | 24-48h |
| **GitHub Discussions** | Questions générales | 48-72h |
| **Email** | Support professionnel | 24h |
| **Slack** | Communication équipe | Temps réel |

### 📧 Contacts | Contacts

- **Support technique** : support@sama-etat.sn
- **Sécurité** : security@sama-etat.sn
- **Partenariats** : partnerships@sama-etat.sn
- **Presse** : press@sama-etat.sn

---

<div align="center">
  
  **🇸🇳 SAMA ÉTAT - Structure et Organisation 🇸🇳**
  
  *Un projet structuré pour la transparence gouvernementale*
  
  *A structured project for government transparency*
  
  📧 **contact@sama-etat.sn** | 🌐 **https://sama-etat.sn**
  
</div>