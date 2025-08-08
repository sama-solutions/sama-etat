# SAMA ÉTAT – Plateforme citoyenne de gouvernance stratégique, opérationnelle et transparente

Auteur·e·s: Mamadou Mbagnick DOGUE, Rassol DOGUE

Version: 2.0

SAMA ÉTAT est une plateforme numérique open source conçue pour digitaliser intégralement la gouvernance publique vers le zéro-papier. Elle vise à structurer, piloter et rendre visible toute action publique, au service d’une République transparente, performante et inclusive.

## Fonctionnalités Clés

*   **Gestion de Projets :**
    *   Définir et gérer les projets gouvernementaux avec des informations détaillées, y compris les objectifs, les calendriers et les budgets.
    *   Suivre l'avancement des projets, les jalons et les tâches.
    *   Affecter des chefs de projet et des équipes de différents ministères.
    *   Lier les projets aux objectifs stratégiques du gouvernement.

*   **Gestion Budgétaire :**
    *   Allouer et suivre les budgets des projets et des ministères.
    *   Gérer les lignes budgétaires, les engagements et les dépenses.
    *   Assurer la conformité financière et le reporting.

*   **Gestion des Ministères et des Employés :**
    *   Organiser la structure gouvernementale avec les ministères et les départements.
    *   Gérer les informations et les rôles des employés.

*   **Tableau de Bord et Rapports :**
    *   Visualiser les données clés des projets et des finances grâce à un tableau de bord intuitif.
    *   Générer des rapports sur l'état des projets, l'exécution du budget, etc.

*   **Personnalisable et Extensible :**
    *   Construit sur le framework flexible d'Odoo, permettant une personnalisation et une intégration faciles avec d'autres modules.

## Dépendances (Odoo et Python)

- Odoo 18.0
- Modules Odoo: `base`, `project`, `mail`, `website`, `hr`, `calendar`, `website_event` (et selon votre usage: `helpdesk`/`portal`)
- Dépendances Python: `qrcode`, `pillow`, `requests`, `cryptography`

## Installation (Docker recommandé)

1) Cloner le dépôt
```bash
git clone https://github.com/loi200812/sama-etat
cd sama_etat
```

2) Exemple de `docker-compose.yml`
```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=odoo_db
      - POSTGRES_PASSWORD=odoo
      - POSTGRES_USER=odoo
    ports: ["5432:5432"]
    volumes:
      - odoo-db-data:/var/lib/postgresql/data

  odoo:
    image: odoo:18.0
    depends_on: [db]
    ports: ["8069:8069", "8071:8071"]
    environment:
      - HOST=db
      - USER=odoo
      - PASSWORD=odoo
    volumes:
      - odoo-web-data:/var/lib/odoo
      - ./:/mnt/extra-addons/sama_etat_repo
    command: --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons/sama_etat_repo/custom_addons -d odoo_db

volumes:
  odoo-db-data:
  odoo-web-data:
```

3) (Optionnel) Dockerfile si vous souhaitez builder votre image
```dockerfile
FROM odoo:18.0
RUN pip install qrcode pillow requests cryptography
COPY ./custom_addons /mnt/extra-addons
```

4) Lancer
```bash
docker compose up -d --build
# puis ouvrir http://localhost:8069
```

5) Installation manuelle (Linux)
- Postgres 15, Python 3.10+
- `pip install qrcode pillow requests cryptography`
- Démarrez Odoo 18 avec `--addons-path` incluant `custom_addons`

## Intégration IA: rôle et périmètre

SAMA ÉTAT embarque une configuration unifiée des fournisseurs IA via le modèle `ai.provider.config`:
- Fournisseurs supportés: OpenAI (ChatGPT), Google (Gemini), Microsoft (Azure OpenAI), Ollama (local)
- Méthodes: clé API (par défaut) et OAuth pour Google/Microsoft si configuré
- Options: sélection du fournisseur par défaut, test de connexion, paramètres de génération (tokens, température)

Cas d’usage typiques:
- Aide à la rédaction de contenus (notes, résumés, e-mails, descriptions de projets)
- Assistance à l’analyse (explications, reformulations) dans l’interface agent
- Démonstrations locales via Ollama sans dépendance cloud

Respect des données:
- Les contenus générés restent dans Odoo (chatter, champs texte)
- Le choix du fournisseur et des endpoints appartient à l’administrateur

## Utilisation

Une fois installé, vous pouvez accéder aux fonctionnalités du module depuis le menu principal d'Odoo. Le module est organisé en plusieurs sections :

*   **Tableau de Bord :** Obtenez un aperçu rapide des projets et des budgets.
*   **Projets :** Gérez tous les projets gouvernementaux.
*   **Budgets :** Suivez les informations financières.
*   **Ministères :** Visualisez et gérez les ministères du gouvernement.

## Contribuer

Les contributions sont les bienvenues ! Si vous avez des suggestions, des rapports de bogues ou des demandes de fonctionnalités, veuillez ouvrir une issue ou soumettre une pull request sur le [dépôt GitHub](https://github.com/loi200812/sama-etat).

## Licence

Ce module est sous licence [MIT License](LICENSE).
