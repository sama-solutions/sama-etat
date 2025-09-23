# 🚀 SAMA SYNDICAT - SCRIPTS DE DÉMARRAGE

## 📋 **APERÇU**

3 scripts de démarrage automatique ont été créés pour **SAMA SYNDICAT**. Ils arrêtent automatiquement les processus existants sur le port 8070 et démarrent le module.

## 🎯 **SCRIPTS DISPONIBLES**

### **🐍 start_sama_syndicat.py** (Version complète)
- **Fonctionnalités** : Détection avancée des processus, gestion d'erreurs robuste
- **Dépendances** : Python3 + psutil (optionnel)
- **Avantages** : Gestion complète des processus, messages détaillés

### **🐍 start_simple.py** (Version basique)
- **Fonctionnalités** : Démarrage simple et efficace
- **Dépendances** : Python3 uniquement
- **Avantages** : Rapide, sans dépendances externes

### **🐚 start_sama_syndicat.sh** (Version bash)
- **Fonctionnalités** : Script bash avec couleurs et gestion d'erreurs
- **Dépendances** : Bash + outils système standard
- **Avantages** : Compatible avec tous les systèmes Unix/Linux

## ⚡ **DÉMARRAGE RAPIDE**

### **Méthode recommandée**
```bash
python3 start_simple.py
```

### **Autres méthodes**
```bash
# Version complète
./start_sama_syndicat.py

# Version bash
./start_sama_syndicat.sh

# Ou directement
python3 start_sama_syndicat.py
bash start_sama_syndicat.sh
```

## 🔧 **CONFIGURATION**

### **Paramètres par défaut**
- **Port** : 8070
- **Base de données** : `sama_syndicat_final_1756812346`
- **Odoo** : `/var/odoo/odoo18/odoo-bin`
- **Addons** : `/var/odoo/odoo18/odoo/addons,/var/odoo/odoo18/addons,/tmp/addons_sama_syndicat`

### **Personnalisation**
Pour modifier la configuration, éditez les variables en haut de chaque script :

```python
# Dans les scripts Python
PORT = 8070
DATABASE = "votre_base_de_donnees"
ODOO_BIN = "/chemin/vers/odoo-bin"
```

```bash
# Dans le script bash
PORT=8070
DATABASE="votre_base_de_donnees"
ODOO_BIN="/chemin/vers/odoo-bin"
```

## 🛠️ **FONCTIONNALITÉS**

### **✅ Arrêt automatique des processus**
- Détection des processus sur le port 8070
- Arrêt propre avec SIGTERM puis SIGKILL si nécessaire
- Utilisation de `lsof`, `pkill`, `fuser` selon disponibilité
- Vérification de la libération du port

### **✅ Démarrage intelligent**
- Vérification de l'existence d'Odoo
- Recherche automatique dans les emplacements communs
- Mode développement activé (`--dev=reload,xml`)
- Configuration optimisée pour le développement

### **✅ Gestion d'erreurs**
- Messages d'erreur clairs et colorés
- Gestion des interruptions (Ctrl+C)
- Nettoyage automatique en cas d'arrêt
- Fallback sur différentes méthodes

## 🌐 **ACCÈS APRÈS DÉMARRAGE**

### **URLs disponibles**
- **Interface principale** : `http://localhost:8070`
- **Backend Odoo** : `http://localhost:8070/web`
- **Login direct** : `http://localhost:8070/web/login?db=sama_syndicat_final_1756812346`
- **Dashboard SAMA** : `http://localhost:8070/web` (menu Syndicat)

### **Versions du dashboard**
- **V1 - CSS Natif** : Menu → Syndicat → 🧪 Test Dashboards → V1
- **V2 - Compact** : Menu → Syndicat → 🧪 Test Dashboards → V2
- **V3 - Graphiques** : Menu → Syndicat → 🧪 Test Dashboards → V3
- **V4 - Minimaliste** : Menu → Syndicat → 🧪 Test Dashboards → V4

## 🛑 **ARRÊT DU SERVEUR**

### **Méthodes d'arrêt**
```bash
# Dans le terminal où le script tourne
Ctrl+C

# Depuis un autre terminal
pkill -f odoo-bin

# Ou forcer l'arrêt
pkill -9 -f odoo-bin

# Libérer le port spécifiquement
fuser -k 8070/tcp
```

## 🧪 **TEST DES SCRIPTS**

### **Script de test inclus**
```bash
python3 test_startup.py
```

Ce script vérifie :
- ✅ Existence et permissions des scripts
- ✅ Disponibilité des dépendances
- ✅ Chemins Odoo
- ✅ État du port 8070

## 🔍 **DÉPANNAGE**

### **❌ "Odoo non trouvé"**
1. Vérifiez le chemin dans la variable `ODOO_BIN`
2. Installez Odoo ou ajustez le chemin
3. Le script recherche automatiquement dans :
   - `/var/odoo/odoo18/odoo-bin`
   - `/usr/bin/odoo`
   - `/usr/local/bin/odoo`
   - `/opt/odoo/odoo-bin`

### **❌ "Port 8070 occupé"**
1. Le script arrête automatiquement les processus
2. Si le problème persiste : `fuser -k 8070/tcp`
3. Ou changez le port dans la configuration

### **❌ "Permission denied"**
```bash
chmod +x start_*.py start_*.sh
```

### **❌ "Module sama_syndicat non trouvé"**
1. Vérifiez que le module est dans `/tmp/addons_sama_syndicat`
2. Ou ajustez `ADDONS_PATH` dans le script

## 📊 **LOGS ET DEBUG**

### **Logs Odoo**
Les logs s'affichent directement dans le terminal. Pour plus de détails :
```bash
# Modifier le niveau de log dans le script
--log-level=debug
```

### **Logs système**
```bash
# Vérifier les processus
ps aux | grep odoo

# Vérifier le port
lsof -i :8070
netstat -tlnp | grep 8070
```

## 🎊 **AVANTAGES DES SCRIPTS**

### **✅ Simplicité**
- Un seul script pour tout faire
- Pas de configuration manuelle
- Démarrage en une commande

### **✅ Robustesse**
- Gestion automatique des conflits de port
- Arrêt propre des processus existants
- Récupération d'erreurs

### **✅ Flexibilité**
- 3 versions selon les préférences
- Configuration facilement modifiable
- Compatible avec différents environnements

### **✅ Développement**
- Mode développement activé
- Rechargement automatique des modifications
- Logs en temps réel

## 📋 **RÉSUMÉ D'UTILISATION**

```bash
# 1. Démarrage rapide
python3 start_simple.py

# 2. Accès à l'interface
# Ouvrir http://localhost:8070/web

# 3. Tester les dashboards
# Menu Syndicat → 🧪 Test Dashboards

# 4. Arrêt
# Ctrl+C dans le terminal
```

**Les scripts de démarrage SAMA SYNDICAT sont prêts à l'emploi !** 🚀

---
**Créé le :** 2025-09-02  
**Scripts :** 3 versions complètes  
**Statut :** ✅ Prêt pour utilisation  
**Support :** Tous systèmes Unix/Linux