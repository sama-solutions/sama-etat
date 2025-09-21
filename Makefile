# Makefile pour SAMA ÉTAT
# Auteurs: Mamadou Mbagnick DOGUE, Rassol DOGUE

.PHONY: help install test lint format clean docker-build docker-run docker-test deploy docs

# Variables
PYTHON := python3
PIP := pip3
DOCKER := docker
DOCKER_COMPOSE := docker-compose
PROJECT_NAME := sama-etat
VERSION := 1.0.0

# Couleurs pour l'affichage
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
PURPLE := \033[0;35m
NC := \033[0m # No Color

# Aide par défaut
help: ## Afficher cette aide
	@echo -e "${BLUE}SAMA ÉTAT - Makefile${NC}"
	@echo -e "${PURPLE}Auteurs: Mamadou Mbagnick DOGUE, Rassol DOGUE${NC}"
	@echo ""
	@echo -e "${GREEN}Commandes disponibles:${NC}"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  ${YELLOW}%-20s${NC} %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Installation et configuration
install: ## Installer les dépendances
	@echo -e "${BLUE}📦 Installation des dépendances...${NC}"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo -e "${GREEN}✅ Dépendances installées${NC}"

install-dev: ## Installer les dépendances de développement
	@echo -e "${BLUE}🔧 Installation des dépendances de développement...${NC}"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-cov black flake8 isort mypy bandit safety
	@echo -e "${GREEN}✅ Dépendances de développement installées${NC}"

# Tests
test: ## Exécuter tous les tests
	@echo -e "${BLUE}🧪 Exécution des tests...${NC}"
	$(PYTHON) -m pytest tests/ -v
	@echo -e "${GREEN}✅ Tests terminés${NC}"

test-unit: ## Exécuter les tests unitaires
	@echo -e "${BLUE}🧪 Tests unitaires...${NC}"
	$(PYTHON) -m pytest tests/ -v -m "unit"

test-integration: ## Exécuter les tests d'intégration
	@echo -e "${BLUE}🧪 Tests d'intégration...${NC}"
	$(PYTHON) -m pytest tests/ -v -m "integration"

test-coverage: ## Exécuter les tests avec couverture
	@echo -e "${BLUE}📊 Tests avec couverture...${NC}"
	$(PYTHON) -m pytest tests/ --cov=. --cov-report=html --cov-report=term
	@echo -e "${GREEN}✅ Rapport de couverture généré dans coverage/html/${NC}"

test-performance: ## Exécuter les tests de performance
	@echo -e "${BLUE}⚡ Tests de performance...${NC}"
	$(PYTHON) -m pytest tests/ -v -m "performance"

# Qualité du code
lint: ## Vérifier la qualité du code
	@echo -e "${BLUE}🔍 Vérification de la qualité du code...${NC}"
	flake8 . --count --statistics
	@echo -e "${GREEN}✅ Vérification terminée${NC}"

format: ## Formater le code
	@echo -e "${BLUE}🎨 Formatage du code...${NC}"
	black .
	isort .
	@echo -e "${GREEN}✅ Code formaté${NC}"

format-check: ## Vérifier le formatage sans modifier
	@echo -e "${BLUE}🎨 Vérification du formatage...${NC}"
	black --check --diff .
	isort --check-only --diff .

type-check: ## Vérifier les types
	@echo -e "${BLUE}🔬 Vérification des types...${NC}"
	mypy . --ignore-missing-imports

# Sécurité
security: ## Analyser la sécurité
	@echo -e "${BLUE}🔒 Analyse de sécurité...${NC}"
	bandit -r . -f json -o reports/bandit-report.json
	safety check --json --output reports/safety-report.json
	@echo -e "${GREEN}✅ Analyse de sécurité terminée${NC}"

# Docker
docker-build: ## Construire l'image Docker
	@echo -e "${BLUE}🐳 Construction de l'image Docker...${NC}"
	$(DOCKER) build -t $(PROJECT_NAME):$(VERSION) .
	$(DOCKER) build -t $(PROJECT_NAME):latest .
	@echo -e "${GREEN}✅ Image Docker construite${NC}"

docker-build-test: ## Construire l'image Docker de test
	@echo -e "${BLUE}🐳 Construction de l'image Docker de test...${NC}"
	$(DOCKER) build -f Dockerfile.test -t $(PROJECT_NAME):test .
	@echo -e "${GREEN}✅ Image Docker de test construite${NC}"

docker-run: ## Lancer l'application avec Docker
	@echo -e "${BLUE}🚀 Lancement de l'application avec Docker...${NC}"
	$(DOCKER_COMPOSE) up -d
	@echo -e "${GREEN}✅ Application lancée sur http://localhost:8069${NC}"

docker-stop: ## Arrêter l'application Docker
	@echo -e "${BLUE}🛑 Arrêt de l'application Docker...${NC}"
	$(DOCKER_COMPOSE) down
	@echo -e "${GREEN}✅ Application arrêtée${NC}"

docker-test: ## Exécuter les tests dans Docker
	@echo -e "${BLUE}🧪 Tests dans Docker...${NC}"
	$(DOCKER_COMPOSE) -f docker-compose.test.yml up --build --abort-on-container-exit
	$(DOCKER_COMPOSE) -f docker-compose.test.yml down -v
	@echo -e "${GREEN}✅ Tests Docker terminés${NC}"

docker-logs: ## Afficher les logs Docker
	@echo -e "${BLUE}📋 Logs Docker...${NC}"
	$(DOCKER_COMPOSE) logs -f

docker-clean: ## Nettoyer les ressources Docker
	@echo -e "${BLUE}🧹 Nettoyage Docker...${NC}"
	$(DOCKER_COMPOSE) down -v --remove-orphans
	$(DOCKER) system prune -f
	@echo -e "${GREEN}✅ Nettoyage terminé${NC}"

# Base de données
db-init: ## Initialiser la base de données
	@echo -e "${BLUE}🗄️ Initialisation de la base de données...${NC}"
	$(DOCKER_COMPOSE) exec odoo odoo --init=sama_etat --stop-after-init
	@echo -e "${GREEN}✅ Base de données initialisée${NC}"

db-update: ## Mettre à jour la base de données
	@echo -e "${BLUE}🔄 Mise à jour de la base de données...${NC}"
	$(DOCKER_COMPOSE) exec odoo odoo --update=sama_etat --stop-after-init
	@echo -e "${GREEN}✅ Base de données mise à jour${NC}"

db-backup: ## Sauvegarder la base de données
	@echo -e "${BLUE}💾 Sauvegarde de la base de données...${NC}"
	mkdir -p backups
	$(DOCKER_COMPOSE) exec db pg_dump -U odoo sama_etat > backups/sama_etat_$(shell date +%Y%m%d_%H%M%S).sql
	@echo -e "${GREEN}✅ Sauvegarde créée dans backups/${NC}"

db-restore: ## Restaurer la base de données (usage: make db-restore FILE=backup.sql)
	@echo -e "${BLUE}📥 Restauration de la base de données...${NC}"
	@if [ -z "$(FILE)" ]; then echo -e "${RED}❌ Veuillez spécifier FILE=backup.sql${NC}"; exit 1; fi
	$(DOCKER_COMPOSE) exec -T db psql -U odoo -d sama_etat < $(FILE)
	@echo -e "${GREEN}✅ Base de données restaurée${NC}"

# Documentation
docs: ## Générer la documentation
	@echo -e "${BLUE}📚 Génération de la documentation...${NC}"
	mkdir -p docs
	@echo "Documentation générée automatiquement" > docs/index.html
	@echo -e "${GREEN}✅ Documentation générée dans docs/${NC}"

docs-serve: ## Servir la documentation localement
	@echo -e "${BLUE}🌐 Service de documentation sur http://localhost:8000${NC}"
	cd docs && $(PYTHON) -m http.server 8000

# Déploiement
deploy-staging: ## Déployer en staging
	@echo -e "${BLUE}🚀 Déploiement en staging...${NC}"
	@echo -e "${YELLOW}⚠️ Fonctionnalité à implémenter${NC}"

deploy-production: ## Déployer en production
	@echo -e "${BLUE}🚀 Déploiement en production...${NC}"
	@echo -e "${YELLOW}⚠️ Fonctionnalité à implémenter${NC}"

# Utilitaires
clean: ## Nettoyer les fichiers temporaires
	@echo -e "${BLUE}🧹 Nettoyage des fichiers temporaires...${NC}"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	rm -rf coverage/
	rm -rf reports/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf dist/
	rm -rf build/
	@echo -e "${GREEN}✅ Nettoyage terminé${NC}"

version: ## Afficher la version
	@echo -e "${BLUE}SAMA ÉTAT v$(VERSION)${NC}"
	@echo -e "${PURPLE}Auteurs: Mamadou Mbagnick DOGUE, Rassol DOGUE${NC}"

status: ## Afficher le statut du projet
	@echo -e "${BLUE}📊 Statut du projet SAMA ÉTAT${NC}"
	@echo -e "${GREEN}Version:${NC} $(VERSION)"
	@echo -e "${GREEN}Python:${NC} $(shell $(PYTHON) --version)"
	@echo -e "${GREEN}Docker:${NC} $(shell $(DOCKER) --version)"
	@echo -e "${GREEN}Docker Compose:${NC} $(shell $(DOCKER_COMPOSE) --version)"
	@echo ""
	@echo -e "${BLUE}📁 Structure du projet:${NC}"
	@find . -maxdepth 2 -type f -name "*.py" | wc -l | xargs echo "  Fichiers Python:"
	@find . -maxdepth 2 -type f -name "*.xml" | wc -l | xargs echo "  Fichiers XML:"
	@find . -maxdepth 2 -type f -name "*.js" | wc -l | xargs echo "  Fichiers JavaScript:"

# Commandes de développement
dev-setup: install-dev ## Configuration complète pour le développement
	@echo -e "${BLUE}🔧 Configuration de l'environnement de développement...${NC}"
	mkdir -p coverage reports logs
	@echo -e "${GREEN}✅ Environnement de développement configuré${NC}"

dev-test: format-check lint type-check test-coverage security ## Tests complets de développement
	@echo -e "${GREEN}✅ Tous les tests de développement sont passés${NC}"

dev-run: ## Lancer en mode développement
	@echo -e "${BLUE}🚀 Lancement en mode développement...${NC}"
	DEV_MODE=true $(DOCKER_COMPOSE) up

# Commandes CI/CD
ci: format-check lint type-check test-coverage security ## Pipeline CI/CD
	@echo -e "${GREEN}✅ Pipeline CI/CD terminé avec succès${NC}"

# Commandes de release
release-check: ci ## Vérifier avant release
	@echo -e "${BLUE}🔍 Vérification avant release...${NC}"
	@echo -e "${GREEN}✅ Prêt pour la release${NC}"

release: release-check ## Créer une release
	@echo -e "${BLUE}🏷️ Création de la release v$(VERSION)...${NC}"
	git tag -a v$(VERSION) -m "Release version $(VERSION)"
	@echo -e "${GREEN}✅ Release v$(VERSION) créée${NC}"
	@echo -e "${YELLOW}💡 N'oubliez pas de pousser le tag: git push origin v$(VERSION)${NC}"

# Commande par défaut
.DEFAULT_GOAL := help