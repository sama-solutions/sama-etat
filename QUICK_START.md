# Guide de Démarrage Rapide | Quick Start Guide

<div align="center">
  <img src="logo.png" alt="SAMA ÉTAT Logo" width="150"/>
  
  **Démarrez avec SAMA ÉTAT en moins de 5 minutes !**
  
  *Get started with SAMA ÉTAT in less than 5 minutes!*
</div>

---

## 🚀 Démarrage Rapide | Quick Start

### 🐳 Option 1: Docker (Recommandée | Recommended)

```bash
# 1. Cloner le repository | Clone repository
git clone https://github.com/loi200812/sama-etat.git
cd sama-etat

# 2. Lancer avec Docker | Start with Docker
docker-compose up -d

# 3. Attendre le démarrage | Wait for startup
docker-compose logs -f odoo

# 4. Accéder à l'application | Access application
# http://localhost:8069
```

### 🔧 Option 2: Installation Locale | Local Installation

```bash
# 1. Prérequis | Prerequisites
sudo apt update
sudo apt install postgresql python3-pip git

# 2. Cloner Odoo 18.0 | Clone Odoo 18.0
git clone --depth 1 --branch 18.0 https://github.com/odoo/odoo.git

# 3. Installer SAMA ÉTAT | Install SAMA ÉTAT
git clone https://github.com/loi200812/sama-etat.git
cp -r sama-etat/sama_etat /path/to/odoo/addons/

# 4. Installer les dépendances | Install dependencies
pip3 install -r sama-etat/requirements.txt

# 5. Lancer Odoo | Start Odoo
cd odoo
./odoo-bin -d sama_etat_db -i sama_etat
```

---

## 🎯 Première Connexion | First Login

### 📋 Informations de Connexion | Login Information

| Champ | Valeur | Field | Value |
|-------|--------|-------|-------|
| **URL** | http://localhost:8069 | **URL** | http://localhost:8069 |
| **Base de données** | sama_etat | **Database** | sama_etat |
| **Email** | admin@sama-etat.sn | **Email** | admin@sama-etat.sn |
| **Mot de passe** | admin | **Password** | admin |

### 🔐 Première Configuration | Initial Setup

1. **Connexion** : Utilisez les identifiants ci-dessus
2. **Langue** : Choisissez Français ou English
3. **Société** : Configurez les informations de votre organisation
4. **Utilisateurs** : Créez des comptes pour votre équipe

---

## 🗺️ Navigation Rapide | Quick Navigation

### 🏛️ Modules Principaux | Main Modules

| Module | Description FR | Description EN |
|--------|----------------|----------------|
| **📊 Tableau de Bord** | Vue d'ensemble des projets et KPIs | Overview of projects and KPIs |
| **🏗️ Projets** | Gestion des projets gouvernementaux | Government project management |
| **📋 Décisions** | Suivi des décisions officielles | Official decision tracking |
| **📅 Événements** | Gestion des événements publics | Public event management |
| **💰 Budgets** | Suivi financier et budgétaire | Financial and budget tracking |
| **🗺️ Carte** | Visualisation géographique | Geographic visualization |

### 🔗 Liens Rapides | Quick Links

- **Tableau de Bord** : `/web#action=sama_etat.dashboard_action`
- **Projets** : `/web#action=sama_etat.government_project_action`
- **Carte Interactive** : `/web#action=sama_etat.public_map_action`
- **Site Public** : `/sama-etat`

---

## 📊 Données de Démonstration | Demo Data

SAMA ÉTAT inclut des données de démonstration pour vous aider à comprendre le système :

### 🏗️ Projets Exemples | Sample Projects
- **50+ projets** répartis dans les 14 régions du Sénégal
- **Différents statuts** : En cours, Terminé, En attente
- **Budgets variés** : De 10M à 500M FCFA
- **Géolocalisation** : Coordonnées GPS réalistes

### 🏛️ Structure Administrative | Administrative Structure
- **14 régions** du Sénégal avec coordonnées GPS
- **Ministères** et départements gouvernementaux
- **Utilisateurs types** : Ministres, Directeurs, Chefs de projet

### 📈 Indicateurs | Metrics
- **KPIs stratégiques** alignés sur le Plan Sénégal 2050
- **Rapports financiers** automatisés
- **Tableaux de bord** interactifs

---

## 🛠️ Configuration Avancée | Advanced Configuration

### 🔧 Variables d'Environnement | Environment Variables

```bash
# Configuration de base | Basic configuration
POSTGRES_DB=sama_etat
POSTGRES_USER=odoo
POSTGRES_PASSWORD=your_password

# Configuration avancée | Advanced configuration
ODOO_WORKERS=4
ODOO_MAX_CRON_THREADS=2
ODOO_LIMIT_MEMORY_HARD=2684354560

# Mode développement | Development mode
DEV_MODE=true
LOG_LEVEL=debug
```

### 📧 Configuration Email | Email Configuration

```ini
# Dans odoo.conf | In odoo.conf
[options]
email_from = noreply@sama-etat.sn
smtp_server = smtp.gmail.com
smtp_port = 587
smtp_ssl = True
smtp_user = your_email@gmail.com
smtp_password = your_app_password
```

### 🗺️ Configuration Cartographique | Map Configuration

```ini
# Coordonnées par défaut (Dakar) | Default coordinates (Dakar)
map_default_lat = 14.6928
map_default_lng = -17.4467
map_default_zoom = 7

# Fournisseur de tuiles | Tile provider
map_tile_provider = OpenStreetMap
```

---

## 🔍 Résolution de Problèmes | Troubleshooting

### ❌ Problèmes Courants | Common Issues

#### 🐳 Docker

```bash
# Problème : Port déjà utilisé | Issue: Port already in use
docker-compose down
sudo lsof -i :8069
sudo kill -9 <PID>

# Problème : Base de données | Issue: Database
docker-compose down -v
docker-compose up -d

# Logs détaillés | Detailed logs
docker-compose logs -f odoo
```

#### 🔧 Installation Locale | Local Installation

```bash
# Problème : Dépendances manquantes | Issue: Missing dependencies
pip3 install --upgrade -r requirements.txt

# Problème : PostgreSQL | Issue: PostgreSQL
sudo systemctl start postgresql
sudo -u postgres createdb sama_etat

# Problème : Permissions | Issue: Permissions
sudo chown -R $USER:$USER /path/to/odoo
```

### 📞 Support | Support

- **GitHub Issues** : [Signaler un problème](https://github.com/loi200812/sama-etat/issues)
- **Documentation** : [Wiki complet](https://github.com/loi200812/sama-etat/wiki)
- **Email** : contact@sama-etat.sn

---

## 🎓 Tutoriels | Tutorials

### 📹 Vidéos de Formation | Training Videos
- [Installation et Configuration](https://youtube.com/watch?v=example1)
- [Création de Projets](https://youtube.com/watch?v=example2)
- [Utilisation de la Carte](https://youtube.com/watch?v=example3)

### 📚 Guides Détaillés | Detailed Guides
- [Guide Administrateur](ADMIN_GUIDE.md)
- [Guide Utilisateur](USER_GUIDE.md)
- [Guide Développeur](DEVELOPER_GUIDE.md)

---

## 🚀 Prochaines Étapes | Next Steps

### 🎯 Après l'Installation | After Installation

1. **Explorez** le tableau de bord principal
2. **Créez** votre premier projet gouvernemental
3. **Configurez** les utilisateurs et permissions
4. **Personnalisez** selon vos besoins
5. **Intégrez** avec vos systèmes existants

### 🔄 Mise à Jour | Updates

```bash
# Mise à jour Docker | Docker update
docker-compose pull
docker-compose up -d

# Mise à jour locale | Local update
git pull origin main
./odoo-bin -d sama_etat_db -u sama_etat
```

---

<div align="center">
  
  **🇸🇳 Bienvenue dans SAMA ÉTAT ! | Welcome to SAMA ÉTAT! 🇸🇳**
  
  *Transformons ensemble la gouvernance publique au Sénégal*
  
  *Let's transform public governance in Senegal together*
  
  ⭐ **N'oubliez pas de donner une étoile !** | **Don't forget to star!** ⭐
  
</div>