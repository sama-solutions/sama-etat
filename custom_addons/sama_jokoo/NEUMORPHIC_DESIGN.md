# 🎨 Design System Neumorphique - Sama Jokoo

## 🎯 Vision
Créer une application sociale avec un design neumorphique moderne, élégant et intuitif, connectée directement à Odoo.

---

## 🎨 DESIGN SYSTEM

### 🌈 Palette de Couleurs

#### Couleurs Principales
```css
/* Base neumorphique */
--bg-primary: #f0f0f3;      /* Fond principal clair */
--bg-secondary: #e6e6e9;    /* Fond secondaire */
--bg-dark: #2d2d30;         /* Mode sombre */

/* Ombres neumorphiques */
--shadow-light: #ffffff;     /* Ombre claire (relief) */
--shadow-dark: #d1d1d4;      /* Ombre foncée (creux) */
--shadow-inset-light: #ffffff; /* Ombre interne claire */
--shadow-inset-dark: #d1d1d4;  /* Ombre interne foncée */

/* Couleurs d'accent */
--accent-primary: #667eea;   /* Bleu principal */
--accent-secondary: #764ba2; /* Violet secondaire */
--accent-success: #4ecdc4;   /* Vert succès */
--accent-warning: #ffe66d;   /* Jaune attention */
--accent-error: #ff6b6b;     /* Rouge erreur */

/* Texte */
--text-primary: #2d3748;     /* Texte principal */
--text-secondary: #718096;   /* Texte secondaire */
--text-muted: #a0aec0;       /* Texte atténué */
```

#### Mode Sombre
```css
/* Base sombre */
--bg-primary-dark: #2d2d30;
--bg-secondary-dark: #3a3a3d;
--shadow-light-dark: #404040;
--shadow-dark-dark: #1a1a1c;
--text-primary-dark: #f7fafc;
--text-secondary-dark: #e2e8f0;
```

### 🔲 Composants de Base

#### 1. Boutons Neumorphiques
```css
.neu-button {
  background: var(--bg-primary);
  border-radius: 12px;
  border: none;
  padding: 12px 24px;
  box-shadow: 
    6px 6px 12px var(--shadow-dark),
    -6px -6px 12px var(--shadow-light);
  transition: all 0.3s ease;
}

.neu-button:hover {
  box-shadow: 
    4px 4px 8px var(--shadow-dark),
    -4px -4px 8px var(--shadow-light);
}

.neu-button:active {
  box-shadow: 
    inset 2px 2px 4px var(--shadow-dark),
    inset -2px -2px 4px var(--shadow-light);
}
```

#### 2. Cartes Neumorphiques
```css
.neu-card {
  background: var(--bg-primary);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 
    8px 8px 16px var(--shadow-dark),
    -8px -8px 16px var(--shadow-light);
  margin: 16px;
}

.neu-card-inset {
  box-shadow: 
    inset 4px 4px 8px var(--shadow-dark),
    inset -4px -4px 8px var(--shadow-light);
}
```

#### 3. Champs de Saisie
```css
.neu-input {
  background: var(--bg-primary);
  border: none;
  border-radius: 12px;
  padding: 12px 16px;
  box-shadow: 
    inset 3px 3px 6px var(--shadow-dark),
    inset -3px -3px 6px var(--shadow-light);
  color: var(--text-primary);
}

.neu-input:focus {
  outline: none;
  box-shadow: 
    inset 3px 3px 6px var(--shadow-dark),
    inset -3px -3px 6px var(--shadow-light),
    0 0 0 3px rgba(102, 126, 234, 0.1);
}
```

### 📱 Composants Spécialisés

#### 1. Post Card
```css
.post-card {
  background: var(--bg-primary);
  border-radius: 20px;
  padding: 24px;
  margin: 16px;
  box-shadow: 
    10px 10px 20px var(--shadow-dark),
    -10px -10px 20px var(--shadow-light);
}

.post-header {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  box-shadow: 
    4px 4px 8px var(--shadow-dark),
    -4px -4px 8px var(--shadow-light);
}
```

#### 2. Navigation Bar
```css
.nav-bar {
  background: var(--bg-primary);
  border-radius: 25px;
  padding: 8px;
  margin: 16px;
  box-shadow: 
    6px 6px 12px var(--shadow-dark),
    -6px -6px 12px var(--shadow-light);
  display: flex;
  justify-content: space-around;
}

.nav-item {
  padding: 12px;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.nav-item.active {
  box-shadow: 
    inset 3px 3px 6px var(--shadow-dark),
    inset -3px -3px 6px var(--shadow-light);
}
```

---

## 📱 ARCHITECTURE APPLICATION

### 🛠️ Choix Technologique
**Recommandation : Progressive Web App (PWA)**

**Avantages :**
- ✅ Déploiement simple
- ✅ Mise à jour automatique
- ✅ Fonctionne sur tous les appareils
- ✅ Intégration native avec Odoo
- ✅ Développement rapide

**Stack Technique :**
- **Frontend** : Vue.js 3 + Vite
- **CSS** : CSS natif avec variables
- **API** : Fetch API vers Odoo
- **PWA** : Service Worker + Manifest

### 📁 Structure Projet
```
sama_jokoo_app/
├── public/
│   ├── manifest.json
│   └── sw.js
├── src/
│   ├── components/
│   │   ├── neumorphic/
│   │   │   ├── NeuButton.vue
│   │   │   ├── NeuCard.vue
│   │   │   └── NeuInput.vue
│   │   └── social/
│   │       ├── PostCard.vue
│   │       ├── UserAvatar.vue
│   │       └── NavBar.vue
│   ├── views/
│   │   ├── LoginView.vue
│   │   ├── FeedView.vue
│   │   └── ProfileView.vue
│   ├── services/
│   │   ├── odooApi.js
│   │   └── auth.js
│   ├── styles/
│   │   ├── neumorphic.css
│   │   └── variables.css
│   └── main.js
├── package.json
└── vite.config.js
```

### 🔌 Connexion Odoo

#### Service API
```javascript
// services/odooApi.js
class OdooAPI {
  constructor(baseURL = 'http://localhost:8070') {
    this.baseURL = baseURL;
    this.sessionId = null;
  }

  async login(username, password) {
    const response = await fetch(`${this.baseURL}/web/session/authenticate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        method: 'call',
        params: {
          db: 'sama_jokoo_dev',
          login: username,
          password: password
        }
      })
    });
    
    const data = await response.json();
    if (data.result && data.result.uid) {
      this.sessionId = data.result.session_id;
      return data.result;
    }
    throw new Error('Authentication failed');
  }

  async getPosts() {
    return this.call('social.post', 'search_read', []);
  }

  async createPost(content) {
    return this.call('social.post', 'create', [{ content }]);
  }

  async call(model, method, args = []) {
    const response = await fetch(`${this.baseURL}/web/dataset/call_kw`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Cookie': `session_id=${this.sessionId}`
      },
      body: JSON.stringify({
        jsonrpc: '2.0',
        method: 'call',
        params: {
          model,
          method,
          args,
          kwargs: {}
        }
      })
    });
    
    const data = await response.json();
    return data.result;
  }
}

export default new OdooAPI();
```

---

## 🎯 ÉCRANS PRINCIPAUX

### 1. Écran de Connexion
- **Design** : Carte centrale neumorphique
- **Éléments** : Logo, champs login/password, bouton connexion
- **Animations** : Transition douce vers le feed

### 2. Feed Principal
- **Design** : Liste de cartes posts neumorphiques
- **Éléments** : Navigation bar, posts, bouton création
- **Interactions** : Scroll infini, pull-to-refresh

### 3. Création de Post
- **Design** : Modal neumorphique
- **Éléments** : Zone de texte, boutons médias, publication
- **Animations** : Apparition en douceur

### 4. Profil Utilisateur
- **Design** : Carte profil + liste posts
- **Éléments** : Avatar, stats, posts personnels
- **Interactions** : Édition profil

---

## 🚀 PLAN DE DÉVELOPPEMENT

### Phase 1 : Setup Minimal ⏳
1. Initialiser projet Vue.js + Vite
2. Créer composants neumorphiques de base
3. Tester connexion Odoo
4. Écran login fonctionnel

### Phase 2 : Feed Basique ⏳
1. Service API posts
2. Affichage liste posts
3. Création post simple
4. Navigation de base

### Phase 3 : Interactions ⏳
1. Système de likes
2. Commentaires
3. Profil utilisateur
4. Notifications

---

*Dernière mise à jour : 2025-09-08 17:00*