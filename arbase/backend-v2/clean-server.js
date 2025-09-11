import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 4000;

// Middleware
app.use(cors({
  origin: ['http://localhost:3000', 'http://localhost:3001', 'http://localhost:3002', 'http://localhost:5173'],
  credentials: true
}));
app.use(express.json());

// Routes de base
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    version: '2.0.0-clean'
  });
});

app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    services: {
      database: 'mock',
      redis: 'mock',
      websocket: 'inactive'
    },
    timestamp: new Date().toISOString()
  });
});

// Route pour les expériences (mock)
app.get('/api/experiences/public', (req, res) => {
  res.json({
    experiences: [
      {
        id: 'demo_business_card',
        title: 'Carte de Visite AR Demo',
        description: 'Démonstration de carte de visite en réalité augmentée',
        category: 'business-card',
        views: 42,
        scans: 15,
        createdAt: new Date().toISOString()
      },
      {
        id: 'demo_product_3d',
        title: 'Produit 3D Demo',
        description: 'Démonstration de produit en 3D',
        category: 'product',
        views: 28,
        scans: 8,
        createdAt: new Date().toISOString()
      }
    ],
    pagination: {
      page: 1,
      limit: 20,
      total: 2,
      pages: 1
    }
  });
});

// Route pour récupérer une expérience
app.get('/api/experiences/:id', (req, res) => {
  const { id } = req.params;
  
  res.json({
    id,
    title: `Expérience AR ${id}`,
    description: 'Expérience de démonstration ARBase v2',
    category: 'demo',
    views: Math.floor(Math.random() * 100),
    scans: Math.floor(Math.random() * 50),
    interactions: Math.floor(Math.random() * 200),
    createdAt: new Date().toISOString(),
    content: [
      {
        type: 'text',
        data: { text: 'Bonjour ARBase v2!' },
        position: { x: 0, y: 0, z: 0 },
        rotation: { x: 0, y: 0, z: 0 },
        scale: { x: 1, y: 1, z: 1 }
      }
    ],
    settings: {
      autoStart: true,
      trackingMode: 'qr'
    }
  });
});

// Route pour enregistrer un scan
app.post('/api/experiences/:id/scan', (req, res) => {
  res.json({ message: 'Scan enregistré', experienceId: req.params.id });
});

// Route pour générer un QR code
app.post('/api/qr/generate', (req, res) => {
  res.json({
    qrCode: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==',
    data: req.body.data || 'demo',
    size: req.body.size || 256
  });
});

// Route 404
app.use('*', (req, res) => {
  res.status(404).json({
    error: 'Route not found',
    path: req.originalUrl,
    available: ['/health', '/api/health', '/api/experiences/public', '/api/qr/generate']
  });
});

// Gestion d'erreurs
app.use((error, req, res, next) => {
  console.error('Erreur serveur:', error);
  res.status(500).json({ error: 'Erreur serveur interne' });
});

// Démarrage avec gestion d'erreurs
const server = app.listen(PORT, () => {
  console.log(`🚀 Backend ARBase v2 démarré sur le port ${PORT}`);
  console.log(`📊 Health Check: http://localhost:${PORT}/health`);
  console.log(`🔗 API: http://localhost:${PORT}/api`);
}).on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.error(`❌ Port ${PORT} déjà utilisé`);
    process.exit(1);
  } else {
    console.error('❌ Erreur serveur:', err);
    process.exit(1);
  }
});

// Gestion de l'arrêt propre
process.on('SIGINT', () => {
  console.log('\n🔄 Arrêt du serveur...');
  server.close(() => {
    console.log('✅ Serveur arrêté proprement');
    process.exit(0);
  });
});

process.on('SIGTERM', () => {
  console.log('\n🔄 Arrêt du serveur...');
  server.close(() => {
    console.log('✅ Serveur arrêté proprement');
    process.exit(0);
  });
});
