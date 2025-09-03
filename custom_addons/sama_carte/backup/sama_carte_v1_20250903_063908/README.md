# Module Sama Carte - Gestion des Cartes de Membre

## Description
Module Odoo 18 CE pour la gestion des cartes de membre avec QR code et page publique de validation.

## Fonctionnalités
- ✅ Gestion des membres avec photos
- ✅ Génération automatique de numéros de membre
- ✅ QR codes pointant vers une page publique
- ✅ Page publique stylisée pour validation des cartes
- ✅ Impression de cartes recto-verso format carte de crédit
- ✅ Gestion de la validité des cartes

## Installation et Tests

### Prérequis
- Odoo 18 CE installé dans `/var/odoo/odoo18`
- Environnement virtuel dans `/home/grand-as/odoo18-venv`
- PostgreSQL avec utilisateur `odoo` / mot de passe `odoo`
- Module `qrcode` Python installé

### Scripts de test disponibles

#### 1. Test complet automatique
```bash
./scripts/test_cycle.sh
```
Ce script effectue un cycle complet :
- Installation du module
- Démarrage d'Odoo sur le port 8070
- Tests de connectivité
- Vérification de l'installation

#### 2. Installation manuelle du module
```bash
./scripts/install_module.sh
```

#### 3. Démarrage manuel d'Odoo
```bash
./scripts/start_odoo_test.sh
```

#### 4. Arrêt des tests
```bash
./scripts/stop_test.sh
```

### Configuration de test
- **Port**: 8070
- **Base de données**: sama_carte_test
- **Interface web**: http://localhost:8070
- **Logs**: `/tmp/odoo_sama_carte_test.log`

## Utilisation

### 1. Création d'un membre
1. Aller dans "Gestion des Membres" > "Membres"
2. Créer un nouveau membre avec nom et photo
3. Le numéro de membre et QR code sont générés automatiquement

### 2. Page publique
- Scanner le QR code ou accéder à l'URL `/member/<token>`
- La page affiche les informations du membre et la validité de la carte
- Design responsive adapté mobile et desktop

### 3. Impression de cartes
- Utiliser l'action "Carte de Membre" sur un membre
- Format carte de crédit (55x85mm) recto-verso
- QR code intégré sur le recto

## Structure du module
```
sama_carte/
├── __manifest__.py              # Configuration du module
├── __init__.py                  # Initialisation
├── models/                      # Modèles de données
│   ├── __init__.py
│   └── membership_member.py     # Modèle membre
├── controllers/                 # Contrôleurs web
│   ├── __init__.py
│   └── main.py                  # Contrôleur page publique
├── views/                       # Vues et templates
│   ├── membership_views.xml     # Interface admin
│   └── website_member_views.xml # Page publique
├── reports/                     # Rapports PDF
│   ├── paper_format.xml         # Format carte
│   └── report_member_card.xml   # Template carte
├── security/                    # Sécurité
│   └── ir.model.access.csv      # Droits d'accès
├── data/                        # Données
│   └── sequence.xml             # Séquence numéros
└── scripts/                     # Scripts de test
    ├── start_odoo_test.sh       # Démarrage Odoo
    ├── install_module.sh        # Installation module
    ├── test_cycle.sh            # Cycle complet
    └── stop_test.sh             # Arrêt tests
```

## Dépendances
- `base`: Socle Odoo
- `mail`: Système de messagerie
- `website`: Pages publiques
- `portal`: Interface publique

## Logs et Débogage
- Logs Odoo: `/tmp/odoo_sama_carte_test.log`
- Logs installation: `/tmp/odoo_install_sama_carte.log`
- Logs cycle test: `/tmp/sama_carte_test_cycle.log`

## Sécurité
- Tokens d'accès UUID4 uniques par membre
- Pages publiques sans authentification
- Validation de la validité des cartes
- Gestion des erreurs (membre non trouvé, carte expirée)