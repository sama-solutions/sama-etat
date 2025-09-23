# 🔧 GUIDE DE DÉPANNAGE - MENUS DASHBOARDS SAMA SYNDICAT

## 🚨 **PROBLÈME IDENTIFIÉ**

Les menus de test des 4 versions du dashboard ne sont pas visibles dans l'interface Odoo.

## 🎯 **SOLUTIONS DISPONIBLES**

### **⚡ Solution 1 : Script automatique (Recommandé)**
```bash
python3 start_and_fix_menus.py
```
- Démarre Odoo automatiquement
- Met à jour le module
- Corrige les menus
- **Tout en une seule commande**

### **🔧 Solution 2 : Correction simple (Odoo déjà démarré)**
```bash
# 1. Démarrer Odoo d'abord
python3 quick_start.py

# 2. Dans un autre terminal, corriger les menus
python3 fix_menus_simple.py
```

### **📋 Solution 3 : Correction manuelle**
```bash
# 1. Démarrer Odoo
python3 quick_start.py

# 2. Mettre à jour le module
python3 update_module.py

# 3. Corriger les menus
python3 fix_dashboard_menus.py
```

## 🔍 **DIAGNOSTIC DU PROBLÈME**

### **Causes possibles**
1. **Module non mis à jour** après ajout des nouveaux fichiers
2. **Cache Odoo** non vidé
3. **Ordre de chargement** des fichiers XML
4. **Permissions** sur les menus

### **Vérifications effectuées**
- ✅ Actions des dashboards créées
- ✅ Fichiers XML valides
- ✅ Manifeste mis à jour
- ✅ Scripts de correction créés

## 📁 **FICHIERS CRÉÉS POUR LA CORRECTION**

### **🔧 Scripts de correction**
- `fix_dashboard_menus.py` - Correction complète des menus
- `fix_menus_simple.py` - Correction simple (Odoo démarré)
- `start_and_fix_menus.py` - Démarrage + correction automatique

### **📄 Fichiers de configuration**
- `views/dashboard_test_menus.xml` - Menus de test séparés
- `views/dashboard_actions.xml` - Actions corrigées (menus supprimés)

## 🚀 **PROCÉDURE RECOMMANDÉE**

### **Étape 1 : Arrêter Odoo**
```bash
pkill -f odoo-bin
```

### **Étape 2 : Démarrer avec correction automatique**
```bash
python3 start_and_fix_menus.py
```

### **Étape 3 : Vérifier dans l'interface**
1. Ouvrir `http://localhost:8070/web`
2. Se connecter (admin/admin)
3. Aller dans le menu **Syndicat**
4. Chercher **🧪 Test Dashboards**

### **Étape 4 : Si les menus ne sont toujours pas visibles**
```bash
# Recharger la page (F5)
# Ou vider le cache navigateur (Ctrl+Shift+R)
```

## 🔄 **ALTERNATIVE : ACCÈS DIRECT AUX DASHBOARDS**

Si les menus ne fonctionnent pas, vous pouvez accéder directement aux dashboards via les URLs :

### **URLs directes**
```
# Dashboard V1 - CSS Natif Odoo
http://localhost:8070/web#action=action_syndicat_dashboard_v1

# Dashboard V2 - Compact Organisé  
http://localhost:8070/web#action=action_syndicat_dashboard_v2

# Dashboard V3 - Graphiques & Listes
http://localhost:8070/web#action=action_syndicat_dashboard_v3

# Dashboard V4 - Minimaliste
http://localhost:8070/web#action=action_syndicat_dashboard_v4
```

## 🧪 **TEST DES ACTIONS**

### **Script de test des actions**
```bash
python3 test_dashboard_versions.py
```

Ce script vérifie que toutes les actions existent et sont accessibles.

## 📋 **STRUCTURE DES MENUS ATTENDUE**

```
Syndicat
├── Tableau de Bord (dashboard principal)
├── 🧪 Test Dashboards
│   ├── V1 - CSS Natif Odoo
│   ├── V2 - Compact Organisé
│   ├── V3 - Graphiques & Listes
│   └── V4 - Minimaliste
├── Adhérents
├── Assemblées
├── Revendications
└── ...
```

## 🔍 **VÉRIFICATION MANUELLE**

### **Dans l'interface Odoo**
1. Aller dans **Paramètres** → **Technique** → **Interface utilisateur** → **Menus**
2. Rechercher "Test Dashboard"
3. Vérifier que les menus existent

### **Vérification des actions**
1. Aller dans **Paramètres** → **Technique** → **Actions** → **Actions de fenêtre**
2. Rechercher "dashboard_v"
3. Vérifier que les 4 actions existent

## 🛠️ **DÉPANNAGE AVANCÉ**

### **Si les scripts ne fonctionnent pas**
```bash
# Vérifier la connexion à Odoo
curl http://localhost:8070/web/database/selector

# Vérifier les processus Odoo
ps aux | grep odoo

# Vérifier les logs Odoo
tail -f /var/log/odoo/odoo.log
```

### **Réinstallation complète du module**
```bash
# 1. Désinstaller le module (via interface web)
# 2. Redémarrer Odoo
python3 quick_start.py

# 3. Réinstaller le module (via interface web)
# 4. Corriger les menus
python3 fix_menus_simple.py
```

## 🎊 **RÉSOLUTION ATTENDUE**

Après application d'une des solutions, vous devriez voir :

1. ✅ Menu **🧪 Test Dashboards** dans le menu Syndicat
2. ✅ 4 sous-menus pour chaque version
3. ✅ Accès fonctionnel à chaque dashboard
4. ✅ Boutons cliquables dans les dashboards

## 📞 **SUPPORT**

### **Si le problème persiste**
1. Exécuter `python3 fix_menus_simple.py` et noter les messages
2. Vérifier les logs Odoo pour les erreurs
3. Essayer l'accès direct via les URLs
4. Redémarrer complètement Odoo

### **Commandes de diagnostic**
```bash
# État du serveur
python3 test_startup.py

# État des menus
python3 fix_menus_simple.py

# État des actions
python3 test_dashboard_versions.py
```

---
**Créé le :** 2025-09-02  
**Problème :** Menus dashboards non visibles  
**Solutions :** 3 scripts de correction  
**Statut :** ✅ SOLUTIONS PRÊTES