# SAMA ÉTAT

<div align="center">
  <img src="logo.png" alt="SAMA ÉTAT Logo" width="200"/>
  
  **Plateforme citoyenne de gouvernance stratégique, opérationnelle et transparente**
  
  *Citizen platform for strategic, operational, and transparent governance*
  
  [![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
  [![Odoo Version](https://img.shields.io/badge/Odoo-18.0-purple.svg)](https://www.odoo.com/)
  [![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
</div>

---

## 🌍 À propos | About

**SAMA ÉTAT** est une plateforme numérique open source révolutionnaire conçue pour digitaliser intégralement la gouvernance publique vers le zéro-papier. Elle vise à structurer, piloter et rendre visible toute action publique, au service d'une République transparente, performante et inclusive.

**SAMA ÉTAT** is a revolutionary open-source digital platform designed to fully digitize public governance towards zero-paper. It aims to structure, manage, and make visible all public actions, serving a transparent, efficient, and inclusive Republic.

---

## 🎯 Vision et Mission | Vision & Mission

### 🇫🇷 Français

**Vision :** Transformer l'État sénégalais en une administration 100% numérique, transparente et redevable devant ses citoyens.

**Mission :** Fournir une plateforme technologique qui centralise, structure et rend accessible toute l'information gouvernementale, permettant un pilotage efficace des politiques publiques et une participation citoyenne éclairée.

### 🇬🇧 English

**Vision:** Transform the Senegalese State into a 100% digital, transparent, and accountable administration to its citizens.

**Mission:** Provide a technological platform that centralizes, structures, and makes accessible all government information, enabling effective management of public policies and informed citizen participation.

---

## ✨ Fonctionnalités Principales | Key Features

### 🏛️ Gestion Gouvernementale | Government Management
- **Projets Publics** : Centralisation et suivi de tous les projets gouvernementaux
- **Décisions Officielles** : Traçabilité des décisions présidentielles et ministérielles
- **Événements Publics** : Gestion des événements et communications officielles
- **Budgets Transparents** : Suivi en temps réel des allocations et dépenses

### 🗺️ Cartographie Interactive | Interactive Mapping
- **Géolocalisation GPS** : Coordonnées réalistes de tous les projets et initiatives
- **Visualisation Territoriale** : Carte interactive des 14 régions du Sénégal
- **Suivi Géographique** : Répartition spatiale des investissements publics

### 📊 Tableau de Bord Stratégique | Strategic Dashboard
- **Plan Sénégal 2050** : Alignement avec les objectifs stratégiques nationaux
- **Indicateurs Clés** : KPIs de performance et de suivi
- **Rapports Automatisés** : Génération de rapports de transparence

### 👥 Participation Citoyenne | Citizen Participation
- **Accès Public** : Interface citoyenne pour consulter les projets
- **Transparence Totale** : Visibilité sur l'exécution et les budgets
- **Responsabilité** : Mécanismes de reddition de comptes

---

## 🚀 Avantages par Acteur | Benefits by Stakeholder

### 🏛️ Pour le Gouvernement | For Government
- ✅ Tableau de bord centralisé du Plan Sénégal 2050
- ✅ Coordination optimisée des politiques publiques
- ✅ Réduction des coûts opérationnels (zéro licence)
- ✅ Institutionnalisation de la reddition de comptes
- ✅ Alignement avec les Objectifs de Développement Durable (ODD)

### 👨‍👩‍👧‍👦 Pour les Citoyens | For Citizens
- ✅ Accès libre à tous les projets publics en cours
- ✅ Visualisation géographique des initiatives gouvernementales
- ✅ Suivi en temps réel de l'exécution et des budgets
- ✅ Participation active à la vie publique
- ✅ République redevable, projet par projet

### 🏢 Pour les Entreprises et ONG | For Businesses & NGOs
- ✅ Alignement sur les feuilles de route gouvernementales
- ✅ Réduction des doublons et meilleure coordination
- ✅ Outil de reporting et de transparence
- ✅ Plateforme adaptable à tout portefeuille de projets

---

## 🛠️ Technologies | Technologies

<div align="center">

| Technologie | Version | Description |
|-------------|---------|-------------|
| **Odoo** | 18.0 | Framework ERP open source |
| **Python** | 3.8+ | Langage de programmation principal |
| **PostgreSQL** | 13+ | Base de données relationnelle |
| **JavaScript** | ES6+ | Interface utilisateur dynamique |
| **Leaflet** | 1.9+ | Cartographie interactive |
| **Bootstrap** | 5.0+ | Framework CSS responsive |

</div>

---

## 📦 Installation | Installation

### 🐳 Installation Docker (Recommandée | Recommended)

```bash
# Cloner le dépôt | Clone repository
git clone https://github.com/loi200812/sama-etat.git
cd sama-etat

# Lancer avec Docker Compose | Run with Docker Compose
docker-compose up -d

# Accéder à l'application | Access application
# http://localhost:8069
```

### 🔧 Installation Manuelle | Manual Installation

#### Prérequis | Prerequisites
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql python3 python3-pip git

# Dépendances Python | Python dependencies
pip3 install qrcode pillow
```

#### Installation Odoo
```bash
# Télécharger Odoo 18.0 | Download Odoo 18.0
git clone https://github.com/odoo/odoo.git --depth 1 --branch 18.0

# Installer SAMA ÉTAT | Install SAMA ÉTAT
git clone https://github.com/loi200812/sama-etat.git
cp -r sama-etat/sama_etat /path/to/odoo/addons/

# Configurer et lancer | Configure and run
./odoo-bin -d sama_etat_db -i sama_etat
```

---

## 📚 Documentation | Documentation

### 📖 Guides Utilisateur | User Guides
- [Guide d'Installation Complet](INSTALLATION.md)
- [Guide de Déploiement](DEPLOYMENT_GUIDE.md)
- [Documentation des Fonctionnalités](IMPLEMENTATION_SUMMARY.md)

### 🔧 Documentation Technique | Technical Documentation
- [Architecture du Système](DELIVERABLE_SUMMARY.md)
- [Statut Final du Projet](FINAL_STATUS.md)
- [Données de Démonstration](DEMO_DATA_README.md)

### 🗺️ Cartographie | Mapping
- [Guide des Coordonnées GPS](MAP_COORDINATES_README.md)

---

## 🌟 Captures d'Écran | Screenshots

<div align="center">
  <img src="static/description/screenshots/dashboard.png" alt="Tableau de Bord" width="45%"/>
  <img src="static/description/screenshots/map.png" alt="Carte Interactive" width="45%"/>
</div>

---

## 🤝 Contribution | Contributing

Nous accueillons chaleureusement les contributions ! | We warmly welcome contributions!

### Comment Contribuer | How to Contribute
1. **Fork** le projet | Fork the project
2. **Créer** une branche feature | Create a feature branch
3. **Commiter** vos changements | Commit your changes
4. **Pousser** vers la branche | Push to the branch
5. **Ouvrir** une Pull Request | Open a Pull Request

### Standards de Code | Code Standards
- Suivre les conventions PEP 8 pour Python
- Documenter toutes les nouvelles fonctionnalités
- Inclure des tests unitaires
- Respecter l'architecture Odoo

---

## 📄 Licence | License

Ce projet est sous licence **LGPL-3.0**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

This project is licensed under **LGPL-3.0**. See the [LICENSE](LICENSE) file for details.

---

## 👥 Auteurs | Authors

<div align="center">

### 🎯 Équipe de Développement | Development Team

<table>
  <tr>
    <td align="center">
      <img src="https://github.com/loi200812.png" width="100px;" alt="Mamadou Mbagnick DOGUE"/><br />
      <sub><b>Mamadou Mbagnick DOGUE</b></sub><br />
      <sub>Architecte Principal | Lead Architect</sub>
    </td>
    <td align="center">
      <img src="https://github.com/rassoldogue.png" width="100px;" alt="Rassol DOGUE"/><br />
      <sub><b>Rassol DOGUE</b></sub><br />
      <sub>Développeur Senior | Senior Developer</sub>
    </td>
  </tr>
</table>

</div>

---

## 🌍 Impact Social | Social Impact

### 🎯 Objectifs de Développement Durable | Sustainable Development Goals

SAMA ÉTAT contribue directement aux ODD suivants :

- **ODD 16** : Paix, justice et institutions efficaces
- **ODD 11** : Villes et communautés durables  
- **ODD 17** : Partenariats pour la réalisation des objectifs
- **ODD 9** : Industrie, innovation et infrastructure

---

## 📞 Support et Contact | Support & Contact

### 🆘 Support Technique | Technical Support
- **Issues GitHub** : [Ouvrir un ticket](https://github.com/loi200812/sama-etat/issues)
- **Documentation** : [Wiki du projet](https://github.com/loi200812/sama-etat/wiki)

### 📧 Contact Professionnel | Professional Contact
- **Email** : contact@sama-etat.sn
- **LinkedIn** : [SAMA ÉTAT Official](https://linkedin.com/company/sama-etat)

---

## 🏆 Reconnaissance | Recognition

> *"Le peuple a conçu l'outil. À l'État de l'adopter, aux institutions de l'intégrer, aux citoyens de l'utiliser."*

> *"The people designed the tool. It is up to the State to adopt it, to institutions to integrate it, and to citizens to use it."*

---

<div align="center">
  
  **🇸🇳 Fait avec ❤️ au Sénégal | Made with ❤️ in Senegal 🇸🇳**
  
  ⭐ **N'oubliez pas de donner une étoile si ce projet vous plaît !** | **Don't forget to star if you like this project!** ⭐
  
</div>