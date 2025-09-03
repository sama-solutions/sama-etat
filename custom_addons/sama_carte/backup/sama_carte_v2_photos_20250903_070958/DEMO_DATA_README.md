# 📊 Données de Démonstration - Module Sama Carte

## 🎯 **Vue d'ensemble**

Le module sama_carte inclut maintenant **11 profils de démonstration** représentant différents types de membres d'une organisation professionnelle sénégalaise.

## 👥 **Profils de Démonstration**

### **Membres Actifs (10 profils)**

| N° | Nom | Poste/Fonction | N° Membre | Expiration |
|---|---|---|---|---|
| 1 | **Jean-Baptiste DIALLO** | Directeur Général | SN-MBR-00001 | Sept 2026 |
| 2 | **Fatou NDIAYE** | Responsable Marketing | SN-MBR-00002 | Juin 2026 |
| 3 | **Amadou FALL** | Développeur Senior | SN-MBR-00003 | Oct 2026 |
| 4 | **Aïssatou BA** | Consultante RH | SN-MBR-00004 | Mai 2026 |
| 5 | **Moussa SARR** | Chef de Projet | SN-MBR-00005 | Août 2026 |
| 6 | **Mariama CISSÉ** | Analyste Financier | SN-MBR-00006 | Juin 2026 |
| 7 | **Ousmane DIOUF** | Responsable Commercial | SN-MBR-00007 | Juil 2026 |
| 8 | **Khady MBAYE** | Designer UX/UI | SN-MBR-00008 | Juin 2026 |
| 9 | **Ibrahima SECK** | Ingénieur Système | SN-MBR-00009 | Sept 2026 |
| 10 | **Bineta THIAM** | Responsable Qualité | SN-MBR-00010 | Juil 2026 |

### **Membre Expiré (1 profil pour test)**

| N° | Nom | Statut | N° Membre | Expiration |
|---|---|---|---|---|
| 11 | **Modou KANE** | Stagiaire | SN-MBR-00011 | ❌ Août 2025 |

## 🚀 **Installation et Utilisation**

### **1. Backup V1 créé**
```bash
backup/sama_carte_v1_20250903_063908/
```

### **2. Installation avec données de démonstration**
```bash
./scripts/install_with_demo.sh
```

### **3. Démarrage avec base de démonstration**
```bash
./scripts/start_demo.sh
```

### **4. Test des données**
```bash
./scripts/test_demo_members.sh
```

## 🌐 **Accès aux Interfaces**

### **Interface d'Administration**
- **URL** : http://localhost:8071
- **Login** : admin / admin
- **Menu** : Gestion des Membres > Membres

### **Pages Publiques de Test**
- **Membre non trouvé** : http://localhost:8071/member/token-inexistant
- **Jean-Baptiste DIALLO** : http://localhost:8071/member/3d45e112-4ed9-4aa8-a899-482d539094f0
- **Fatou NDIAYE** : http://localhost:8071/member/ebeb418d-3cd8-442d-8593-04167fa9e0ba
- **Amadou FALL** : http://localhost:8071/member/bb01e2ca-84ca-4bdc-8dbb-a378661c7183

## 📋 **Fonctionnalités Testables**

### **✅ Gestion des Membres**
- Visualisation de la liste des 11 membres
- Consultation des fiches détaillées
- Génération automatique des QR codes
- Impression des cartes PDF

### **✅ Pages Publiques**
- Validation des cartes via QR code
- Affichage du statut (valide/expirée)
- Design responsive et professionnel
- Gestion des erreurs (membre non trouvé)

### **✅ Cas de Test**
- **10 cartes valides** avec différentes dates d'expiration
- **1 carte expirée** pour tester la validation
- **Tokens UUID uniques** pour chaque membre
- **Noms sénégalais authentiques** pour le réalisme

## 🔧 **Configuration Technique**

### **Base de Données**
- **Nom** : `sama_carte_demo`
- **Port Odoo** : 8071
- **Utilisateur** : odoo / odoo

### **Fichiers Ajoutés**
- `data/demo_members.xml` - Données de démonstration
- `scripts/install_with_demo.sh` - Installation avec démo
- `scripts/start_demo.sh` - Démarrage base démo
- `scripts/test_demo_members.sh` - Tests des données

### **Manifest Modifié**
```python
'demo': [
    'data/demo_members.xml',
],
```

## 📊 **Statistiques**

- **Total membres** : 11
- **Cartes valides** : 10
- **Cartes expirées** : 1
- **Tokens uniques** : 11 UUID4
- **Pages publiques** : 11 + page d'erreur

## 🎯 **Prochaines Étapes**

1. **Tester l'interface admin** avec les 11 profils
2. **Imprimer des cartes PDF** pour validation
3. **Scanner les QR codes** pour tester les pages publiques
4. **Valider le design** des cartes recto-verso
5. **Tester la validation** des cartes expirées

---

**🎉 Module sama_carte V2 avec données de démonstration prêt !**