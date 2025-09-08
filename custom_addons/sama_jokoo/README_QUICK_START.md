# 🚀 Sama Jokoo - Quick Start Guide

## Démarrage Rapide

### 1. Validation de l'Installation
```bash
./dev_scripts/validate_installation.sh
```

### 2. Développement
```bash
# Démarrer le développement (port 8070)
./dev_scripts/start_dev.sh

# Surveiller les logs (nouveau terminal)
./dev_scripts/watch_logs.sh

# Aide complète
./dev_scripts/help.sh
```

### 3. Production
```bash
# Démarrer en production (port 8071)
./start_sama_jokoo.sh

# Arrêter
./stop_sama_jokoo.sh
```

### 4. Application Mobile
```bash
cd mobile_app
./start_mobile_dev.sh
```

## 🔧 Dépannage Rapide

### Cycle de Débogage Automatique
```bash
./dev_scripts/debug_cycle.sh
```

### Vérifier l'État
```bash
./dev_scripts/help.sh status
```

### Nettoyer l'Environnement
```bash
./dev_scripts/help.sh clean
```

### Réinitialiser Complètement
```bash
./dev_scripts/help.sh reset
```

## 📊 Accès aux Interfaces

- **Développement**: http://localhost:8070
- **Production**: http://localhost:8071
- **Login**: admin / admin123

## 📱 Fonctionnalités Activées

✅ **Vues Kanban** - Interface moderne et intuitive  
✅ **Dashboard** - Tableaux de bord analytiques  
✅ **Charts** - Graphiques et analyses de données  
✅ **Pivot Tables** - Tableaux croisés dynamiques  
✅ **Mobile App** - Application Flutter native  

## 🎯 Navigation Rapide

### Menu Social
- **Feed** → Dashboard et Mon Feed
- **Contenu** → Posts, Commentaires, Hashtags, Médias
- **Utilisateurs** → Notifications, Suivis, Profils
- **Analytics** → Analyses Posts, Hashtags, Notifications, Utilisateurs
- **Modération** → Outils de modération (Modérateurs+)
- **Configuration** → Paramètres (Admins)

### APIs Disponibles
- `/api/social/auth/*` - Authentification
- `/api/social/posts/*` - Gestion des posts
- `/api/social/users/*` - Gestion des utilisateurs
- `/api/social/notifications/*` - Notifications

## 🆘 Support

En cas de problème :
1. `./dev_scripts/debug_cycle.sh` - Débogage automatique
2. `./dev_scripts/help.sh` - Aide complète
3. Consulter `dev_scripts/README.md` - Documentation détaillée

---

**Sama Jokoo** - Votre réseau social Odoo 18 CE ! 🎉