# ARBase v2 - Plateforme de Réalité Augmentée Moderne

Une plateforme complète de réalité augmentée basée sur des technologies open source, utilisant des QR codes comme markers pour des expériences immersives de qualité professionnelle.

## 🌟 Nouveautés de la Version 2

### Architecture Moderne
- **Moteur AR personnalisé** basé sur WebXR, Three.js et AR.js
- **Frontend React** avec TypeScript et Tailwind CSS
- **Backend Node.js** avec Express et MongoDB
- **WebSocket** pour les interactions temps réel
- **PWA** pour une expérience mobile native

### Fonctionnalités Avancées
- ✅ **QR Codes comme Markers** - Détection et tracking robuste
- ✅ **WebXR Support** - AR native sur les appareils compatibles
- ✅ **Multi-Content** - Modèles 3D, vidéos, textes, images
- ✅ **Animations** - Système d'animation avancé
- ✅ **Interactions** - Clics, survol, gaze tracking
- ✅ **Analytics** - Métriques détaillées et temps réel
- ✅ **Admin Panel** - Interface de gestion moderne
- ✅ **API REST** - Intégration facile avec d'autres systèmes

## 🏗️ Architecture

```
arbase/
├── ar-engine-v2/          # Moteur AR moderne
│   ├── core/              # Core engine avec AREngine principal
│   ├── qr-tracking/       # Système de tracking QR codes
│   ├── rendering/         # Rendu 3D avec Three.js
│   ├── workers/           # Web Workers pour performance
│   └── utils/             # Utilitaires mathématiques
├── frontend-v2/           # Application React moderne
│   ├── src/
│   │   ├── components/ar/ # Composants AR (Scanner, etc.)
│   │   ├── pages/         # Pages de l'application
│   │   ├── stores/        # Gestion d'état avec Zustand
│   │   └── services/      # Services API
├── backend-v2/            # API REST Node.js
│   ├── src/
│   │   ├── models/        # Modèles de données MongoDB
│   │   ├── routes/        # Routes API
│   │   ├── services/      # Services (Redis, Analytics, WebSocket)
│   │   └── middleware/    # Middleware Express
└── start-arbase-v2.sh    # Script de démarrage unifié
```

## 🚀 Installation et Démarrage

### Prérequis
- **Node.js 18+**
- **npm 8+**
- **MongoDB** (optionnel, utilise une base en mémoire par défaut)
- **Redis** (optionnel, pour le cache et les sessions)

### Démarrage Rapide

```bash
# Cloner le projet (si pas déjà fait)
git clone <votre-repo>
cd arbase

# Démarrer ARBase v2
./start-arbase-v2.sh
```

Le script va automatiquement :
1. Vérifier les prérequis
2. Installer toutes les dépendances
3. Configurer l'environnement
4. Démarrer tous les services

### URLs d'Accès
- **Frontend** : http://localhost:3000
- **Scanner AR** : http://localhost:3000/scanner
- **API Backend** : http://localhost:4000
- **Health Check** : http://localhost:4000/health

## 📱 Utilisation

### Pour les Utilisateurs Finaux

1. **Accéder au Scanner**
   ```
   http://localhost:3000/scanner
   ```

2. **Autoriser la Caméra**
   - Accepter l'accès à la caméra
   - Pointer vers un QR code ARBase

3. **Profiter de l'Expérience AR**
   - Contenu 3D interactif
   - Animations fluides
   - Interactions tactiles

### Pour les Créateurs de Contenu

1. **Connexion Admin**
   ```
   Email: admin@arbase.com
   Mot de passe: password
   ```

2. **Créer une Expérience**
   - Utiliser l'API REST
   - Définir le contenu AR
   - Générer le QR code

3. **Partager**
   - QR code automatiquement généré
   - URLs de partage optimisées
   - Analytics intégrées

## 🔧 Configuration

### Variables d'Environnement

**Backend** (`backend-v2/.env`)
```env
NODE_ENV=development
PORT=4000
MONGODB_URI=mongodb://localhost:27017/arbase_v2
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-key
FRONTEND_URL=http://localhost:3000
```

**Frontend** (`frontend-v2/.env`)
```env
VITE_API_URL=http://localhost:4000
VITE_WS_URL=ws://localhost:4000
VITE_APP_NAME=ARBase
VITE_APP_VERSION=2.0.0
```

## 🎯 API REST

### Expériences AR

```javascript
// Récupérer les expériences publiques
GET /api/experiences/public

// Créer une nouvelle expérience
POST /api/experiences
{
  "title": "Ma Carte de Visite AR",
  "qrCode": "unique-qr-data",
  "content": [
    {
      "type": "text",
      "data": { "text": "Bonjour !" },
      "position": { "x": 0, "y": 0, "z": 0 },
      "animations": [...]
    }
  ]
}

// Enregistrer un scan
POST /api/experiences/:id/scan
```

### QR Codes

```javascript
// Générer un QR code
POST /api/qr/generate
{
  "data": "contenu-du-qr",
  "size": 256
}

// QR code pour le scanner
GET /api/qr/scanner

// QR code pour une expérience
GET /api/qr/experience/:id
```

## 🎨 Moteur AR

### Utilisation du Moteur

```typescript
import { AREngine, createAREngine } from './ar-engine-v2';

// Créer une instance du moteur
const engine = createAREngine({
  container: document.getElementById('ar-container'),
  enableQRTracking: true,
  enableWebXR: true,
  debug: true
});

// Initialiser et démarrer
await engine.initialize();
await engine.start();

// Charger une expérience
engine.loadExperience({
  id: 'mon-experience',
  qrCode: 'qr-data',
  content: [
    {
      type: 'model',
      data: { url: '/models/objet.glb' },
      position: { x: 0, y: 0, z: 0 },
      animations: [
        {
          type: 'rotation',
          duration: 5,
          loop: true,
          keyframes: [0, Math.PI * 2]
        }
      ]
    }
  ],
  settings: {
    autoStart: true,
    trackingMode: 'qr'
  }
});
```

### Types de Contenu Supportés

- **Modèles 3D** : .glb, .gltf avec animations
- **Texte** : Texte 3D avec styles personnalisés
- **Images** : PNG, JPG, WebP avec transparence
- **Vidéos** : MP4, WebM avec contrôles
- **HTML** : Contenu HTML rendu en texture

### Animations Disponibles

- **Rotation** : Rotation continue ou par étapes
- **Position** : Déplacement dans l'espace 3D
- **Échelle** : Agrandissement/rétrécissement
- **Opacité** : Effets de fondu

## 📊 Analytics

### Métriques Collectées

- **Vues** : Nombre de fois qu'une expérience est vue
- **Scans** : Nombre de scans QR réussis
- **Interactions** : Clics et interactions avec le contenu
- **Temps d'Engagement** : Durée des sessions
- **Appareils** : Types d'appareils utilisés

### API Analytics

```javascript
// Analytics d'une expérience
GET /api/analytics/experience/:id?days=7

// Dashboard utilisateur
GET /api/analytics/dashboard

// Stats temps réel
GET /api/analytics/realtime/:id
```

## 🔌 WebSocket

### Événements Temps Réel

```javascript
// Connexion WebSocket
const socket = io('http://localhost:4000');

// Rejoindre une expérience
socket.emit('join', { 
  experienceId: 'exp-123',
  userId: 'user-456' 
});

// Écouter les événements AR
socket.on('ar:scan:detected', (data) => {
  console.log('Nouveau scan détecté:', data);
});

socket.on('ar:interaction:detected', (data) => {
  console.log('Interaction détectée:', data);
});
```

## 🛠️ Développement

### Structure des Composants

```typescript
// Composant AR Scanner
import { ARScanner } from './components/ar/ARScanner';

<ARScanner
  onExperienceDetected={(exp) => console.log(exp)}
  onError={(error) => console.error(error)}
/>
```

### Gestion d'État

```typescript
// Store Zustand
import { useARStore } from './stores/arStore';

const { 
  currentExperience, 
  isScanning, 
  settings,
  updateSettings 
} = useARStore();
```

### Services

```typescript
// Service API
import { experienceService } from './services/api';

const experiences = await experienceService.getPublic();
const newExp = await experienceService.create(data);
```

## 📱 PWA (Progressive Web App)

### Fonctionnalités PWA

- **Installation** : Installable sur mobile et desktop
- **Offline** : Fonctionne hors ligne (cache intelligent)
- **Notifications** : Notifications push (optionnel)
- **Partage** : API de partage native

### Manifest

```json
{
  "name": "ARBase - Réalité Augmentée",
  "short_name": "ARBase",
  "display": "standalone",
  "orientation": "portrait",
  "theme_color": "#000000",
  "background_color": "#000000"
}
```

## 🔒 Sécurité

### Mesures de Sécurité

- **HTTPS** : Chiffrement des communications
- **JWT** : Authentification sécurisée
- **CORS** : Protection contre les requêtes malveillantes
- **Rate Limiting** : Protection contre les abus
- **Validation** : Validation stricte des données
- **Sanitization** : Nettoyage des entrées utilisateur

### Permissions

- **Caméra** : Accès caméra pour l'AR
- **Géolocalisation** : Optionnel pour les analytics
- **Stockage** : Cache local pour les performances

## 🧪 Tests

### Tests Automatisés

```bash
# Tests du moteur AR
cd ar-engine-v2
npm test

# Tests du backend
cd backend-v2
npm test

# Tests du frontend
cd frontend-v2
npm test
```

### Tests Manuels

1. **Scanner QR** : Tester avec différents QR codes
2. **Performances** : Vérifier les FPS et la fluidité
3. **Compatibilité** : Tester sur différents appareils
4. **Réseau** : Tester avec connexion lente

## 🚀 Déploiement

### Production

```bash
# Build de production
npm run build

# Variables d'environnement production
NODE_ENV=production
MONGODB_URI=mongodb://prod-server/arbase
REDIS_URL=redis://prod-server:6379
FRONTEND_URL=https://votre-domaine.com
```

### Docker (Optionnel)

```dockerfile
# Dockerfile pour le backend
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 4000
CMD ["npm", "start"]
```

## 📈 Performance

### Optimisations

- **Lazy Loading** : Chargement à la demande
- **Code Splitting** : Division du code en chunks
- **Compression** : Compression gzip/brotli
- **CDN** : Distribution de contenu
- **Cache** : Cache intelligent multi-niveaux

### Métriques de Performance

- **FPS** : 60 FPS en AR
- **Temps de Chargement** : < 3 secondes
- **Taille des Bundles** : Optimisée
- **Memory Usage** : Gestion mémoire efficace

## 🤝 Contribution

### Guide de Contribution

1. **Fork** le projet
2. **Créer une branche** feature
3. **Développer** avec les standards du projet
4. **Tester** toutes les fonctionnalités
5. **Soumettre** une Pull Request

### Standards de Code

- **TypeScript** : Typage strict
- **ESLint** : Linting automatique
- **Prettier** : Formatage du code
- **Conventional Commits** : Messages de commit standardisés

## 📞 Support

### Ressources

- **Documentation** : README et docs/
- **Issues** : GitHub Issues
- **Discussions** : GitHub Discussions
- **Wiki** : Documentation détaillée

### Contact

- **Email** : support@arbase.com
- **Discord** : Serveur communautaire
- **Twitter** : @ARBase_Platform

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- **Three.js** : Moteur 3D
- **AR.js** : Framework AR
- **React** : Interface utilisateur
- **Node.js** : Runtime serveur
- **MongoDB** : Base de données
- **Communauté Open Source** : Contributions et feedback

---

**ARBase v2** - La plateforme de réalité augmentée moderne et open source ! 🚀

*Créez des expériences AR exceptionnelles avec des QR codes comme markers.*