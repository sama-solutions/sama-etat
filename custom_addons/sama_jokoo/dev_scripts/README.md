# Scripts de Développement Sama Jokoo

Ce dossier contient tous les scripts nécessaires pour le développement et les tests du module Sama Jokoo.

## 🚀 Scripts Principaux

### Scripts de Développement (`dev_scripts/`)

| Script | Description | Usage |
|--------|-------------|-------|
| `start_dev.sh` | Démarre Odoo en mode développement | `./start_dev.sh` |
| `stop_dev.sh` | Arrête le serveur de développement | `./stop_dev.sh` |
| `restart_dev.sh` | Redémarre le serveur de développement | `./restart_dev.sh` |
| `watch_logs.sh` | Surveille les logs en temps réel | `./watch_logs.sh` |
| `test_module.sh` | Lance tous les tests du module | `./test_module.sh` |
| `debug_cycle.sh` | Cycle automatique de débogage | `./debug_cycle.sh` |

### Scripts de Production (racine du module)

| Script | Description | Usage |
|--------|-------------|-------|
| `start_sama_jokoo.sh` | Démarre Sama Jokoo en production | `./start_sama_jokoo.sh` |
| `stop_sama_jokoo.sh` | Arrête Sama Jokoo | `./stop_sama_jokoo.sh` |
| `restart_sama_jokoo.sh` | Redémarre Sama Jokoo | `./restart_sama_jokoo.sh` |

### Scripts Mobile (`mobile_app/`)

| Script | Description | Usage |
|--------|-------------|-------|
| `start_mobile_dev.sh` | Initialise et démarre l'app mobile | `./start_mobile_dev.sh` |

## 📋 Configuration

### Ports Utilisés
- **Développement**: 8070
- **Production**: 8071
- **Tests**: 8072

### Bases de Données
- **Développement**: `sama_jokoo_dev`
- **Production**: `sama_jokoo_prod`
- **Tests**: `sama_jokoo_test`

### Chemins Configurés
```bash
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
CUSTOM_ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
```

## 🔄 Workflow de Développement

### 1. Démarrage Initial
```bash
cd /home/grand-as/psagsn/custom_addons/sama_jokoo
./dev_scripts/start_dev.sh
```

### 2. Surveillance des Logs
```bash
# Dans un autre terminal
./dev_scripts/watch_logs.sh
```

### 3. Tests
```bash
./dev_scripts/test_module.sh
```

### 4. Cycle de Débogage Automatique
```bash
./dev_scripts/debug_cycle.sh
```

## 🐛 Débogage

### Cycle de Débogage Automatique
Le script `debug_cycle.sh` effectue automatiquement :
1. **Démarrage** du module
2. **Tests** de fonctionnement
3. **Analyse** des logs
4. **Corrections** automatiques
5. **Redémarrage** si nécessaire

### Analyse Manuelle des Logs
```bash
# Voir les erreurs
grep "ERROR" dev_scripts/logs/odoo_dev.log

# Voir les avertissements
grep "WARNING" dev_scripts/logs/odoo_dev.log

# Suivre les logs en temps réel avec coloration
./dev_scripts/watch_logs.sh
```

### Vérification des Processus
```bash
# Voir les processus Odoo actifs
ps aux | grep odoo

# Voir les ports utilisés
lsof -i :8070
lsof -i :8071
```

## 📱 Développement Mobile

### Initialisation
```bash
cd mobile_app
./start_mobile_dev.sh
```

### Prérequis Flutter
- Flutter SDK installé
- Android Studio ou VS Code
- Émulateur Android ou appareil physique

## 🧪 Tests

### Tests Automatiques
```bash
./dev_scripts/test_module.sh
```

### Tests Manuels
1. Accéder à `http://localhost:8070`
2. Se connecter avec admin/admin123
3. Aller dans Apps > Sama Jokoo
4. Tester les fonctionnalités

## 📊 Monitoring

### Logs Disponibles
- `dev_scripts/logs/odoo_dev.log` - Logs de développement
- `dev_scripts/logs/test_install.log` - Logs d'installation
- `dev_scripts/logs/test_upgrade.log` - Logs de mise à jour
- `logs/sama_jokoo.log` - Logs de production

### Métriques
- Temps de démarrage
- Erreurs détectées
- Tests passés/échoués
- Performance des APIs

## 🔧 Dépannage

### Problèmes Courants

#### Port déjà utilisé
```bash
# Arrêter tous les processus sur le port
./dev_scripts/stop_dev.sh
```

#### Base de données corrompue
```bash
# Recréer la base de données
./dev_scripts/start_dev.sh  # Recrée automatiquement
```

#### Erreurs de permissions
```bash
# Corriger les permissions
find . -name "*.py" -exec chmod 644 {} \;
find . -name "*.xml" -exec chmod 644 {} \;
find . -name "*.sh" -exec chmod +x {} \;
```

#### Module non trouvé
```bash
# Vérifier la structure
ls -la __manifest__.py
ls -la models/
ls -la views/
```

### Nettoyage
```bash
# Nettoyer les logs
rm -f dev_scripts/logs/*.log

# Nettoyer les fichiers temporaires
rm -rf temp/
rm -rf __pycache__/
find . -name "*.pyc" -delete
```

## 📈 Optimisations

### Performance
- Cache Redis activé en développement
- Logs optimisés par niveau
- Rechargement automatique des modules

### Sécurité
- Isolation des ports
- Bases de données séparées
- Logs sécurisés

## 🎯 Prochaines Étapes

1. **Tests d'intégration** avec d'autres modules Odoo
2. **Tests de charge** avec de nombreux utilisateurs
3. **Optimisation** des performances
4. **Documentation** utilisateur
5. **Déploiement** en production

## 📞 Support

En cas de problème :
1. Vérifier les logs : `./dev_scripts/watch_logs.sh`
2. Lancer le cycle de débogage : `./dev_scripts/debug_cycle.sh`
3. Consulter la documentation Odoo 18
4. Vérifier la configuration PostgreSQL

---

**Sama Jokoo** - Développement simplifié et automatisé ! 🚀