# Scripts de Gestion SAMA SYNDICAT

Ce répertoire contient plusieurs scripts pour faciliter la gestion du module SAMA SYNDICAT.

## 📋 Scripts Disponibles

### 1. `start_sama_syndicat.sh` - Script Principal
Script complet avec toutes les fonctionnalités et options.

**Utilisation :**
```bash
# Démarrage normal
./start_sama_syndicat.sh

# Démarrage sur un port différent
./start_sama_syndicat.sh -p 8080

# Démarrage sans mise à jour du module
./start_sama_syndicat.sh --no-update

# Afficher l'aide
./start_sama_syndicat.sh --help
```

**Fonctionnalités :**
- ✅ Vérification des prérequis
- ✅ Arrêt automatique des processus sur le port
- ✅ Gestion des options en ligne de commande
- ✅ Messages colorés et informatifs
- ✅ Gestion des erreurs

### 2. `quick_start.sh` - Démarrage Rapide
Script simplifié pour un démarrage rapide sans options.

**Utilisation :**
```bash
./quick_start.sh
```

**Fonctionnalités :**
- ✅ Arrêt rapide des processus
- ✅ Démarrage immédiat
- ✅ Configuration par défaut

### 3. `stop_sama_syndicat.sh` - Arrêt du Serveur
Script pour arrêter proprement le serveur SAMA SYNDICAT.

**Utilisation :**
```bash
./stop_sama_syndicat.sh
```

**Fonctionnalités :**
- ✅ Arrêt propre avec SIGTERM
- ✅ Arrêt forcé si nécessaire (SIGKILL)
- ✅ Vérification de la libération du port
- ✅ Messages de statut

## 🚀 Démarrage Rapide

### Première utilisation :
```bash
# Rendre les scripts exécutables (si pas déjà fait)
chmod +x *.sh

# Démarrer SAMA SYNDICAT
./start_sama_syndicat.sh
```

### Utilisation quotidienne :
```bash
# Démarrage rapide
./quick_start.sh

# Ou arrêt puis démarrage
./stop_sama_syndicat.sh && ./quick_start.sh
```

## ⚙️ Configuration

### Paramètres par défaut :
- **Port :** 8070
- **Base de données :** sama_syndicat_final_1756812346
- **Chemin Odoo :** /var/odoo/odoo18
- **Module :** sama_syndicat

### Modification des paramètres :
Éditez les variables en haut des scripts pour changer la configuration :

```bash
# Dans start_sama_syndicat.sh
PORT=8070
DATABASE="sama_syndicat_final_1756812346"
ODOO_PATH="/var/odoo/odoo18"
MODULE_NAME="sama_syndicat"
```

## 🔧 Dépannage

### Problème : Port déjà utilisé
```bash
# Vérifier les processus sur le port
lsof -i:8070

# Arrêter manuellement
./stop_sama_syndicat.sh
```

### Problème : Permissions
```bash
# Rendre les scripts exécutables
chmod +x *.sh

# Ou exécuter avec bash
bash start_sama_syndicat.sh
```

### Problème : Module non trouvé
Vérifiez que le module existe dans :
```
/tmp/addons_sama_syndicat/sama_syndicat/
```

## 📝 Logs et Débogage

### Voir les logs en temps réel :
Les scripts affichent les logs directement. Pour plus de détails :

```bash
# Démarrage avec logs détaillés
./start_sama_syndicat.sh --log-level=debug
```

### Fichiers de logs Odoo :
Les logs sont généralement dans :
- `/var/log/odoo/` (si configuré)
- Ou affichés directement dans le terminal

## 🌐 Accès à l'Interface

Une fois démarré, accédez à SAMA SYNDICAT via :
- **URL :** http://localhost:8070
- **Utilisateur :** admin
- **Mot de passe :** (celui configuré lors de l'installation)

## 🛡️ Sécurité

### Recommandations :
- Ne pas exécuter en tant que root sauf si nécessaire
- Vérifier les permissions des fichiers
- Utiliser un firewall pour limiter l'accès au port

### Arrêt d'urgence :
```bash
# Arrêt immédiat de tous les processus Odoo
sudo pkill -f odoo-bin

# Libération forcée du port
sudo fuser -k 8070/tcp
```

## 📞 Support

En cas de problème :
1. Vérifiez les logs affichés par les scripts
2. Consultez la documentation Odoo
3. Vérifiez la configuration du module SAMA SYNDICAT

---

**SAMA SYNDICAT** - Gestion Zéro Papier d'un Syndicat
*Développé par POLITECH SÉNÉGAL*