# SAMA ÉTAT

<div align="center">
  <img src="logo.png" alt="SAMA ÉTAT Logo" width="200"/>
  
  **Plateforme citoyenne de gouvernance stratégique, opérationnelle et transparente**
  
  [![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
  [![Odoo Version](https://img.shields.io/badge/Odoo-18.0-purple.svg)](https://www.odoo.com/)
  [![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
</div>

---

## 🌍 À propos

**SAMA ÉTAT** est une plateforme numérique open source révolutionnaire conçue pour digitaliser intégralement la gouvernance publique vers le zéro-papier. Elle vise à structurer, piloter et rendre visible toute action publique, au service d'une République transparente, performante et inclusive.

### Une plateforme pensée pour résoudre un vrai problème public

Aujourd'hui, les projets gouvernementaux sont trop souvent dispersés, peu traçables, et inaccessibles aux citoyens. SAMA ÉTAT centralise l'information, connecte les décisions, aligne les parties prenantes et outille les citoyens.

Elle transforme l'État, non par promesse, mais par architecture logicielle.

---

## 🎯 Vision et Mission

**Vision :** Transformer l'État sénégalais en une administration 100% numérique, transparente et redevable devant ses citoyens.

**Mission :** Fournir une plateforme technologique qui centralise, structure et rend accessible toute l'information gouvernementale, permettant un pilotage efficace des politiques publiques et une participation citoyenne éclairée.

---

## ✨ Ce que fait SAMA ÉTAT

- 🏛️ **Regroupe et structure** tous les projets publics (nationaux, ministériels, territoriaux) sous une feuille de route unique
- ⏱️ **Suit en temps réel** les décisions du Président, du Premier Ministre, du Conseil des ministres et des ministres
- 🌐 **Connecte** toute l'administration territoriale (maires, préfets, sous-préfets, gouverneurs)
- 🔧 **Intègre** un moteur de pilotage, d'exécution, de suivi-évaluation et d'observabilité des politiques publiques
- 👥 **Rapproche** le citoyen des projets, des budgets et des responsabilités

---

## 🚀 Fonctionnalités Principales

### 🏛️ Gestion Gouvernementale
- **Projets Publics** : Centralisation et suivi de tous les projets gouvernementaux
- **Décisions Officielles** : Traçabilité des décisions présidentielles et ministérielles
- **Événements Publics** : Gestion des événements et communications officielles
- **Budgets Transparents** : Suivi en temps réel des allocations et dépenses

### 🗺️ Cartographie Interactive
- **Géolocalisation GPS** : Coordonnées réalistes de tous les projets et initiatives
- **Visualisation Territoriale** : Carte interactive des 14 régions du Sénégal
- **Suivi Géographique** : Répartition spatiale des investissements publics

### 📊 Tableau de Bord Stratégique
- **Plan Sénégal 2050** : Alignement avec les objectifs stratégiques nationaux
- **Indicateurs Clés** : KPIs de performance et de suivi
- **Rapports Automatisés** : Génération de rapports de transparence

### 👥 Participation Citoyenne
- **Accès Public** : Interface citoyenne pour consulter les projets
- **Transparence Totale** : Visibilité sur l'exécution et les budgets
- **Responsabilité** : Mécanismes de reddition de comptes

---

## 🎯 Avantages pour chaque acteur

### 🏛️ Pour le gouvernement
- ✅ Un tableau de bord centralisé du Plan Sénégal 2050
- ✅ Un outil unique pour coordonner, contrôler et corriger les politiques publiques
- ✅ Carte interactive avec coordonnées GPS réalistes de tous les projets, décisions et événements
- ✅ Zéro coût de licence, 100% open source, 100% aligné avec les ODD
- ✅ Une plateforme nationale qui institutionnalise la reddition de comptes

### 👨‍👩‍👧‍👦 Pour les citoyens
- ✅ Accès libre à tous les projets publics en cours, localement et nationalement
- ✅ Visualisation géographique des initiatives gouvernementales dans leur région
- ✅ Suivi en temps réel de l'exécution, des retards, et des budgets
- ✅ Possibilité d'interpellation légitime et de participation active à la vie publique
- ✅ Une République qui rend des comptes, projet par projet

### 🏢 Pour les entreprises, ONG ou institutions
- ✅ Un outil d'alignement sur les feuilles de route gouvernementales
- ✅ Réduction des doublons, meilleure coordination avec l'État
- ✅ Plateforme adaptée à tout plan stratégique ou portefeuille de projets, quelle que soit la taille
- ✅ Outil de reporting, de suivi contractuel et de transparence

---

## 🛠️ Technologies Utilisées

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

## 📦 Installation

### 🐳 Installation Docker (Recommandée)

```bash
# Cloner le dépôt
git clone https://github.com/loi200812/sama-etat.git
cd sama-etat

# Lancer avec Docker Compose
docker-compose up -d

# Accéder à l'application
# http://localhost:8069
```

### 🔧 Installation Manuelle

#### Prérequis
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql python3 python3-pip git

# Dépendances Python
pip3 install qrcode pillow
```

#### Installation Odoo
```bash
# Télécharger Odoo 18.0
git clone https://github.com/odoo/odoo.git --depth 1 --branch 18.0

# Installer SAMA ÉTAT
git clone https://github.com/loi200812/sama-etat.git
cp -r sama-etat/sama_etat /path/to/odoo/addons/

# Configurer et lancer
./odoo-bin -d sama_etat_db -i sama_etat
```

---

## 📚 Documentation

### 📖 Guides Utilisateur
- [Guide d'Installation Complet](INSTALLATION.md)
- [Guide de Déploiement](DEPLOYMENT_GUIDE.md)
- [Documentation des Fonctionnalités](IMPLEMENTATION_SUMMARY.md)

### 🔧 Documentation Technique
- [Architecture du Système](DELIVERABLE_SUMMARY.md)
- [Statut Final du Projet](FINAL_STATUS.md)
- [Données de Démonstration](DEMO_DATA_README.md)

### 🗺️ Cartographie
- [Guide des Coordonnées GPS](MAP_COORDINATES_README.md)

---

## 🌟 Transparence par design

SAMA ÉTAT place la transparence au cœur de son fonctionnement. Chaque projet, chaque acteur, chaque ressource est visible, traçable et responsable.

La confiance ne se décrète pas. Elle se construit ligne par ligne, API par API, dans un écosystème fiable, neutre et opposable.

Le peuple a conçu l'outil. À l'État de l'adopter, aux institutions de l'intégrer, aux citoyens de l'utiliser.

---

## 🤝 Contribution

Nous accueillons chaleureusement les contributions !

### Comment Contribuer
1. **Fork** le projet
2. **Créer** une branche feature (`git checkout -b feature/AmazingFeature`)
3. **Commiter** vos changements (`git commit -m 'Add some AmazingFeature'`)
4. **Pousser** vers la branche (`git push origin feature/AmazingFeature`)
5. **Ouvrir** une Pull Request

### Standards de Code
- Suivre les conventions PEP 8 pour Python
- Documenter toutes les nouvelles fonctionnalités
- Inclure des tests unitaires
- Respecter l'architecture Odoo

---

## 📄 Licence

Ce projet est sous licence **LGPL-3.0**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 👥 Auteurs

<div align="center">

### 🎯 Équipe de Développement

<table>
  <tr>
    <td align="center">
      <img src="https://github.com/loi200812.png" width="100px;" alt="Mamadou Mbagnick DOGUE"/><br />
      <sub><b>Mamadou Mbagnick DOGUE</b></sub><br />
      <sub>Architecte Principal</sub>
    </td>
    <td align="center">
      <img src="https://github.com/rassoldogue.png" width="100px;" alt="Rassol DOGUE"/><br />
      <sub><b>Rassol DOGUE</b></sub><br />
      <sub>Développeur Senior</sub>
    </td>
  </tr>
</table>

</div>

---

## 🌍 Impact Social

### 🎯 Objectifs de Développement Durable

SAMA ÉTAT contribue directement aux ODD suivants :

- **ODD 16** : Paix, justice et institutions efficaces
- **ODD 11** : Villes et communautés durables  
- **ODD 17** : Partenariats pour la réalisation des objectifs
- **ODD 9** : Industrie, innovation et infrastructure

---

## 📞 Support et Contact

### 🆘 Support Technique
- **Issues GitHub** : [Ouvrir un ticket](https://github.com/loi200812/sama-etat/issues)
- **Documentation** : [Wiki du projet](https://github.com/loi200812/sama-etat/wiki)

### 📧 Contact Professionnel
- **Email** : contact@sama-etat.sn
- **LinkedIn** : [SAMA ÉTAT Official](https://linkedin.com/company/sama-etat)

---

## 🏆 Reconnaissance

> *"Le peuple a conçu l'outil. À l'État de l'adopter, aux institutions de l'intégrer, aux citoyens de l'utiliser."*

---

<div align="center">
  
  **🇸🇳 Fait avec ❤️ au Sénégal 🇸🇳**
  
  ⭐ **N'oubliez pas de donner une étoile si ce projet vous plaît !** ⭐
  
</div>