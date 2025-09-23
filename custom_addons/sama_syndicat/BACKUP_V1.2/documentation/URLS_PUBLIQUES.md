# 🌐 URLS PUBLIQUES - SAMA SYNDICAT V1.1

## 📋 Configuration Serveur

- **URL Serveur :** `http://localhost:8070`
- **Base de données :** `sama_syndicat_final_1756812346`
- **Port :** `8070`
- **Version :** V1.1 Stable

---

## 🔐 URLs d'Administration

### Connexion et Dashboard
- **Connexion Admin :** `http://localhost:8070/web/login`
- **Dashboard Principal :** `http://localhost:8070/web#action=&model=&view_type=&menu_id=`
- **Configuration Modules :** `http://localhost:8070/web#action=&model=ir.module.module&view_type=kanban&menu_id=`

### Connexion Directe avec Base
- **Connexion Rapide :** `http://localhost:8070/web/login?db=sama_syndicat_final_1756812346`

---

## 🏢 URLs SAMA SYNDICAT - Backend

### 📊 Dashboard Syndicat
- **Vue Kanban :** `http://localhost:8070/web#action=&model=syndicat.dashboard&view_type=kanban&menu_id=`
- **Accès Direct :** `http://localhost:8070/web?db=sama_syndicat_final_1756812346#action=&model=syndicat.dashboard&view_type=kanban`

### 👥 Gestion des Adhérents
- **Vue Kanban :** `http://localhost:8070/web#action=&model=syndicat.adherent&view_type=kanban&menu_id=`
- **Vue Liste :** `http://localhost:8070/web#action=&model=syndicat.adherent&view_type=list&menu_id=`
- **Vue Formulaire :** `http://localhost:8070/web#action=&model=syndicat.adherent&view_type=form&menu_id=`
- **Accès Direct :** `http://localhost:8070/web?db=sama_syndicat_final_1756812346#action=&model=syndicat.adherent&view_type=kanban`

### 💰 Gestion des Cotisations
- **Vue Liste :** `http://localhost:8070/web#action=&model=syndicat.cotisation&view_type=list&menu_id=`
- **Vue Formulaire :** `http://localhost:8070/web#action=&model=syndicat.cotisation&view_type=form&menu_id=`

### 🏛️ Assemblées Générales
- **Vue Kanban :** `http://localhost:8070/web#action=&model=syndicat.assemblee&view_type=kanban&menu_id=`
- **Vue Calendrier :** `http://localhost:8070/web#action=&model=syndicat.assemblee&view_type=calendar&menu_id=`
- **Vue Liste :** `http://localhost:8070/web#action=&model=syndicat.assemblee&view_type=list&menu_id=`

### ⚖️ Revendications
- **Vue Kanban :** `http://localhost:8070/web#action=&model=syndicat.revendication&view_type=kanban&menu_id=`
- **Vue Liste :** `http://localhost:8070/web#action=&model=syndicat.revendication&view_type=list&menu_id=`

### 🎯 Actions Syndicales
- **Vue Kanban :** `http://localhost:8070/web#action=&model=syndicat.action&view_type=kanban&menu_id=`
- **Vue Liste :** `http://localhost:8070/web#action=&model=syndicat.action&view_type=list&menu_id=`

### 🎓 Formations
- **Vue Kanban :** `http://localhost:8070/web#action=&model=syndicat.formation&view_type=kanban&menu_id=`
- **Vue Liste :** `http://localhost:8070/web#action=&model=syndicat.formation&view_type=list&menu_id=`

### 🤝 Médiations
- **Vue Liste :** `http://localhost:8070/web#action=&model=syndicat.mediation&view_type=list&menu_id=`
- **Vue Formulaire :** `http://localhost:8070/web#action=&model=syndicat.mediation&view_type=form&menu_id=`

### 📢 Communications
- **Vue Kanban :** `http://localhost:8070/web#action=&model=syndicat.communication&view_type=kanban&menu_id=`
- **Vue Liste :** `http://localhost:8070/web#action=&model=syndicat.communication&view_type=list&menu_id=`

### 📄 Conventions
- **Vue Liste :** `http://localhost:8070/web#action=&model=syndicat.convention&view_type=list&menu_id=`
- **Vue Formulaire :** `http://localhost:8070/web#action=&model=syndicat.convention&view_type=form&menu_id=`

---

## 🌐 URLs Publiques - Frontend

> **Note :** Les URLs publiques nécessitent la configuration du module Website d'Odoo

### 🏠 Pages Principales
- **Accueil :** `http://localhost:8070/syndicat`
- **Accueil Alt :** `http://localhost:8070/syndicat/home`

### ℹ️ Informations
- **À Propos :** `http://localhost:8070/syndicat/about`
- **Présentation :** `http://localhost:8070/syndicat/presentation`

### 👥 Adhésion
- **Adhésion en Ligne :** `http://localhost:8070/syndicat/adhesion`
- **Rejoindre :** `http://localhost:8070/syndicat/rejoindre`

### 📰 Actualités
- **Actualités :** `http://localhost:8070/syndicat/actualites`
- **News :** `http://localhost:8070/syndicat/news`

### 📞 Contact
- **Contact :** `http://localhost:8070/syndicat/contact`
- **Nous Contacter :** `http://localhost:8070/syndicat/nous-contacter`

### 📋 Revendications Publiques
- **Revendications :** `http://localhost:8070/syndicat/revendications`
- **Nos Combats :** `http://localhost:8070/syndicat/nos-combats`

### 🎓 Formations Ouvertes
- **Formations :** `http://localhost:8070/syndicat/formations`
- **Inscription Formation :** `http://localhost:8070/syndicat/formation-inscription`

---

## 🔧 URLs d'API et Services

### 📊 API REST (si activée)
- **Adhérents :** `http://localhost:8070/api/v1/syndicat/adherents`
- **Cotisations :** `http://localhost:8070/api/v1/syndicat/cotisations`
- **Assemblées :** `http://localhost:8070/api/v1/syndicat/assemblees`

### 📱 Services
- **JSON-RPC :** `http://localhost:8070/jsonrpc`

### 🔐 Authentification
- **OAuth Authorize :** `http://localhost:8070/oauth2/authorize`
- **OAuth Token :** `http://localhost:8070/oauth2/token`

---

## 📱 URLs Mobiles

### Interface Mobile
- **Mobile :** `http://localhost:8070/web/mobile`
- **Dashboard Mobile :** `http://localhost:8070/web/mobile#action=&model=syndicat.dashboard`

---

## 🛠️ URLs de Développement

### 🔍 Mode Debug
- **Debug Standard :** `http://localhost:8070/web?debug=1`
- **Debug Assets :** `http://localhost:8070/web?debug=assets`

### 📊 Administration
- **Database Manager :** `http://localhost:8070/web/database/manager`
- **Database Selector :** `http://localhost:8070/web/database/selector`

### 🔧 Informations Techniques
- **Version Info :** `http://localhost:8070/web/webclient/version_info`
- **Session Info :** `http://localhost:8070/web/session/get_session_info`

---

## 📋 URLs Spécifiques SAMA SYNDICAT

### 🎯 Actions Rapides
- **Dashboard Action :** `http://localhost:8070/web#action=syndicat_dashboard_action`
- **Adhérents Action :** `http://localhost:8070/web#action=syndicat_adherent_action`
- **Cotisations Action :** `http://localhost:8070/web#action=syndicat_cotisation_action`

### 📊 Rapports
- **Rapport Adhérents :** `http://localhost:8070/web#action=syndicat_rapport_adherents`
- **Rapport Cotisations :** `http://localhost:8070/web#action=syndicat_rapport_cotisations`
- **Rapport Assemblées :** `http://localhost:8070/web#action=syndicat_rapport_assemblees`

---

## 🚀 URLs Recommandées

### 🎯 Accès Principal
```
http://localhost:8070/web/login?db=sama_syndicat_final_1756812346
```

### 📊 Dashboard Direct
```
http://localhost:8070/web?db=sama_syndicat_final_1756812346#action=&model=syndicat.dashboard&view_type=kanban
```

### 👥 Adhérents Direct
```
http://localhost:8070/web?db=sama_syndicat_final_1756812346#action=&model=syndicat.adherent&view_type=kanban
```

---

## 📝 Notes Importantes

- ✅ **Serveur Actif :** Port 8070 ouvert et fonctionnel
- 🌐 **URLs Publiques :** Nécessitent le module Website d'Odoo
- 🔐 **Authentification :** Certaines URLs nécessitent une connexion
- 🔧 **API :** Nécessite une configuration spécifique
- 🐛 **Debug :** Utilisez `?debug=1` pour le mode développement

---

## 🎯 Démarrage Rapide

1. **Démarrer le serveur :**
   ```bash
   ./start_sama_syndicat.sh
   ```

2. **Accéder à l'interface :**
   ```
   http://localhost:8070/web/login?db=sama_syndicat_final_1756812346
   ```

3. **Vérifier l'état :**
   ```bash
   ./monitor_sama_syndicat.sh -s
   ```

---

**SAMA SYNDICAT V1.1** - Version Gold Standard  
*Développé par POLITECH SÉNÉGAL*