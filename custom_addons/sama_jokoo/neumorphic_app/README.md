# 🎨 Sama Jokoo - Application Neumorphique

## 🌟 Vue d'ensemble

Application sociale moderne avec design neumorphique, connectée directement à Odoo via API REST.

### ✨ Caractéristiques

- **🎨 Design Neumorphique** - Interface moderne avec effets d'ombres et de reliefs
- **📱 Responsive** - Optimisé pour mobile et desktop
- **🚀 PWA** - Progressive Web App installable
- **🔐 Authentification** - Connexion sécurisée avec Odoo
- **⚡ Temps Réel** - Synchronisation instantanée avec la base de données
- **🎯 Minimaliste** - Interface épurée et intuitive

---

## 🏗️ Architecture Technique

### **Frontend**
- **Vue.js 3** - Framework JavaScript moderne
- **Vite** - Build tool ultra-rapide
- **Vue Router** - Navigation SPA
- **Pinia** - Gestion d'état
- **CSS Natif** - Variables CSS et design system

### **Backend**
- **Odoo 18 CE** - ERP/CRM open source
- **API JSON-RPC** - Communication avec Odoo
- **PostgreSQL** - Base de données

### **Design System**
```css
/* Variables neumorphiques */
--bg-primary: #f0f0f3;
--shadow-light: #ffffff;
--shadow-dark: #d1d1d4;
--accent-primary: #667eea;
```

---

## 🚀 Démarrage Rapide

### **Prérequis**
- Node.js 18+ et npm
- Serveur Odoo fonctionnel (port 8070)
- Base de données sama_jokoo_dev

### **Installation**
```bash
# Depuis le dossier sama_jokoo
./start_neumorphic_app.sh
```

### **Développement Manuel**
```bash
cd neumorphic_app
npm install
npm run dev
```

### **Accès**
- **Application** : http://localhost:3000
- **Login** : admin / admin

---

## 📱 Composants Neumorphiques

### **NeuButton**
```vue
<NeuButton variant="primary" size="large" @click="handleClick">
  Connexion
</NeuButton>
```

**Variantes** : `default`, `primary`, `success`, `warning`, `error`  
**Tailles** : `small`, `normal`, `large`

### **NeuCard**
```vue
<NeuCard variant="inset" :hoverable="true">
  <p>Contenu de la carte</p>
</NeuCard>
```

**Variantes** : `default`, `inset`, `flat`  
**Options** : `hoverable`, `padding`

### **NeuInput**
```vue
<NeuInput 
  v-model="value"
  label="Nom d'utilisateur"
  placeholder="Entrez votre nom"
  :error="errorMessage"
/>
```

---

## 🔌 Service API

### **Authentification**
```javascript
import odooApi from '@/services/odooApi.js'

// Connexion
const result = await odooApi.login('admin', 'admin')
if (result.success) {
  // Redirection vers le feed
}
```

### **Gestion des Posts**
```javascript
// Récupérer les posts
const posts = await odooApi.getPosts(20, 0)

// Créer un post
const newPost = await odooApi.createPost('Contenu du post')

// Liker un post
await odooApi.toggleLike(postId)
```

### **Commentaires**
```javascript
// Récupérer les commentaires
const comments = await odooApi.getComments(postId)

// Créer un commentaire
await odooApi.createComment(postId, 'Mon commentaire')
```

---

## 🎨 Design System

### **Palette de Couleurs**
- **Primaire** : `#667eea` (Bleu)
- **Secondaire** : `#764ba2` (Violet)
- **Succès** : `#4ecdc4` (Vert)
- **Attention** : `#ffe66d` (Jaune)
- **Erreur** : `#ff6b6b` (Rouge)

### **Espacements**
- **XS** : 4px
- **SM** : 8px
- **MD** : 16px (défaut)
- **LG** : 24px
- **XL** : 32px
- **XXL** : 48px

### **Rayons de Bordure**
- **SM** : 8px
- **MD** : 12px (défaut)
- **LG** : 16px
- **XL** : 20px
- **Full** : 50% (cercle)

---

## 📂 Structure du Projet

```
neumorphic_app/
├── public/
│   ├── index.html
│   └── manifest.json
├── src/
│   ├── components/
│   │   └── neumorphic/
│   │       ├── NeuButton.vue
│   │       ├── NeuCard.vue
│   │       └── NeuInput.vue
│   ├── views/
│   │   ├── LoginView.vue
│   │   └── FeedView.vue
│   ├── services/
│   │   └── odooApi.js
│   ├── styles/
│   │   └── neumorphic.css
│   ├── App.vue
│   └── main.js
├── package.json
├── vite.config.js
└── README.md
```

---

## 🔧 Configuration

### **Proxy API**
```javascript
// vite.config.js
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8070',
      changeOrigin: true
    }
  }
}
```

### **PWA**
```javascript
// Manifest automatique
{
  "name": "Sama Jokoo",
  "short_name": "SamaJokoo",
  "theme_color": "#667eea",
  "display": "standalone"
}
```

---

## 🧪 Tests et Validation

### **Test de Connexion**
```javascript
// Vérifier la connexion Odoo
const isConnected = await odooApi.testConnection()
```

### **Validation Formulaires**
```javascript
// Validation automatique
const isValid = computed(() => {
  return username.value.length > 0 && password.value.length > 0
})
```

---

## 🚀 Déploiement

### **Build de Production**
```bash
npm run build
```

### **Prévisualisation**
```bash
npm run preview
```

### **Serveur de Production**
```bash
npm run serve
```

---

## 📱 Fonctionnalités Mobiles

- **Touch Gestures** - Interactions tactiles optimisées
- **Responsive Design** - Adaptation automatique à l'écran
- **PWA** - Installation sur l'écran d'accueil
- **Offline Ready** - Fonctionnement hors ligne (cache)

---

## 🎯 Roadmap

### **Phase Actuelle** ✅
- [x] Design system neumorphique
- [x] Authentification
- [x] Connexion API Odoo
- [x] Interface login

### **Prochaines Étapes** 🔄
- [ ] Vue feed des posts
- [ ] Création de posts
- [ ] Système de likes
- [ ] Commentaires
- [ ] Notifications push
- [ ] Mode sombre
- [ ] Internationalisation

---

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature
3. Commit les changements
4. Push vers la branche
5. Ouvrir une Pull Request

---

## 📄 Licence

MIT License - Voir le fichier LICENSE pour plus de détails.

---

**🎨 Sama Jokoo - L'expérience sociale neumorphique ! ✨**