# SAMA SYNDICAT - Gestion Zéro Papier d'un Syndicat

## Description

SAMA SYNDICAT est un module Odoo 18 CE complet pour la gestion zéro papier d'un syndicat ou groupement professionnel. Il s'inspire du module `sama_depute` et adapte ses fonctionnalités au contexte syndical.

## Fonctionnalités Principales

### 🏢 Gestion des Adhérents
- **Fiche complète des adhérents** : informations personnelles, professionnelles, syndicales
- **Gestion des cotisations** : suivi automatique, alertes de retard, historique
- **Statuts d'adhésion** : actif, suspendu, démission, exclusion, retraite
- **Responsabilités syndicales** : président, secrétaire, trésorier, délégués

### 🏛️ Assemblées et Réunions
- **Types d'assemblées** : générales ordinaires/extraordinaires, bureau exécutif, commissions
- **Gestion complète** : convocations, ordre du jour, présences, votes, procès-verbaux
- **Système de vote** : différents types de majorité, votes secrets, résultats automatiques
- **Quorum automatique** : calcul et vérification selon le type d'assemblée

### ⚖️ Revendications et Négociations
- **Gestion des revendications** : création, suivi, négociation, résolution
- **Types variés** : salaires, conditions de travail, sécurité, formation, etc.
- **Suivi des négociations** : séances, accords, désaccords, prochaines étapes
- **Statistiques** : taux de succès, délais de résolution

### 🚩 Actions Syndicales
- **Types d'actions** : grèves, manifestations, pétitions, campagnes, etc.
- **Organisation complète** : planification, autorisations, logistique, sécurité
- **Suivi des participants** : inscriptions, présences, évaluations
- **Communication** : médias, communiqués de presse

### 📢 Communications
- **Multi-canaux** : email, SMS, affichage, réseaux sociaux, site web
- **Ciblage précis** : tous adhérents, filtres par statut/responsabilité
- **Suivi des performances** : taux d'ouverture, lectures, réponses
- **Validation** : workflow de validation pour les communications importantes

### 🎓 Formations Syndicales
- **Catalogue de formations** : initiation, leadership, négociation, droit du travail
- **Gestion complète** : inscriptions, présences, évaluations, certifications
- **Suivi pédagogique** : notes, taux de réussite, satisfaction
- **Formateurs** : internes et externes

### 📋 Conventions Collectives
- **Types de conventions** : entreprise, branche, sectorielles, accords cadres
- **Suivi complet** : négociation, signature, application, révision
- **Commission de suivi** : réunions, évaluations, respect des accords
- **Alertes** : expirations, renouvellements

### 🤝 Médiation et Conflits
- **Gestion des conflits** : individuels, collectifs, disciplinaires
- **Processus de médiation** : interventions, négociations, résolutions
- **Suivi temporel** : délais, efficacité, satisfaction
- **Prévention** : mesures recommandées, formations

### 📊 Tableau de Bord et Statistiques
- **Vue d'ensemble** : adhérents, cotisations, assemblées, actions
- **Indicateurs clés** : taux de participation, succès des revendications
- **Graphiques** : évolution des adhérents, répartition par types
- **Alertes** : cotisations en retard, assemblées sans quorum

### 🌐 Interface Publique
- **Site web syndical** : actualités, actions, formations
- **Portail adhérents** : accès personnalisé aux informations
- **Formulaires** : adhésion en ligne, contact
- **Transparence** : publication des actions et résultats

## Architecture Technique

### Modèles Principaux
- `syndicat.adherent` : Gestion des adhérents
- `syndicat.assemblee` : Assemblées et réunions
- `syndicat.revendication` : Revendications syndicales
- `syndicat.action` : Actions syndicales
- `syndicat.communication` : Communications
- `syndicat.formation` : Formations
- `syndicat.convention` : Conventions collectives
- `syndicat.mediation` : Médiations et conflits
- `syndicat.dashboard` : Tableau de bord

### Sécurité
- **Groupes d'utilisateurs** : Adhérent, Utilisateur, Responsable, Secrétaire, Trésorier, Formateur
- **Règles d'accès** : par enregistrement selon les rôles
- **Confidentialité** : niveaux de confidentialité pour les informations sensibles

### Intégrations
- **Module Mail** : notifications et communications
- **Module Website** : interface publique
- **Module Portal** : accès adhérents
- **Module HR** : intégration RH
- **Module Calendar** : planification des événements

## Installation

### Prérequis
- Odoo 18 Community Edition
- Modules dépendants : `base`, `mail`, `website`, `portal`, `hr`, `calendar`, `document`, `survey`

### Étapes d'installation
1. Copier le module dans le répertoire `addons`
2. Redémarrer Odoo
3. Aller dans Apps et rechercher "SAMA SYNDICAT"
4. Cliquer sur "Installer"

### Configuration initiale
1. Créer les groupes d'utilisateurs
2. Assigner les droits aux utilisateurs
3. Configurer les séquences
4. Importer les données de base
5. Configurer les paramètres de communication

## Utilisation

### Pour les Responsables Syndicaux
1. **Tableau de bord** : Vue d'ensemble des activités
2. **Gestion des adhérents** : Suivi des adhésions et cotisations
3. **Planification** : Assemblées, actions, formations
4. **Communication** : Diffusion d'informations aux adhérents
5. **Suivi** : Revendications, médiations, conventions

### Pour les Adhérents
1. **Portail personnel** : Accès aux informations personnelles
2. **Assemblées** : Convocations, ordres du jour, résultats
3. **Actions** : Participation aux actions syndicales
4. **Formations** : Inscriptions et suivi des formations
5. **Communications** : Réception des informations syndicales

### Pour le Public
1. **Site web** : Actualités et informations publiques
2. **Adhésion** : Formulaire d'adhésion en ligne
3. **Contact** : Formulaire de contact
4. **Transparence** : Actions et résultats publics

## Personnalisation

Le module est conçu pour être facilement personnalisable :

### Champs personnalisés
- Ajout de champs spécifiques selon les besoins
- Modification des listes de sélection
- Adaptation des workflows

### Rapports
- Rapports personnalisés avec QWeb
- Exports Excel/PDF
- Statistiques avancées

### Interface
- Personnalisation des vues
- Ajout de tableaux de bord spécifiques
- Modification des menus

## Support et Maintenance

### Documentation
- Guide utilisateur complet
- Documentation technique
- Exemples de configuration

### Formation
- Formation des utilisateurs
- Support technique
- Mise à jour et évolution

## Licence

Ce module est distribué sous licence LGPL-3.

## Auteur

**POLITECH SÉNÉGAL**
- Site web : https://www.politech.sn
- Email : contact@politech.sn

## Inspiration

Ce module s'inspire du module `sama_depute` et adapte ses concepts au contexte syndical, en conservant la philosophie de gestion zéro papier et d'efficacité administrative.

---

*SAMA SYNDICAT - Pour une gestion moderne et efficace de votre syndicat*