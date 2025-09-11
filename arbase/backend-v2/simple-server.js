import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 4000;

// Middleware
app.use(cors({
  origin: ['http://localhost:3000', 'http://localhost:5173'],
  credentials: true
}));
app.use(express.json());

// Routes de base
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    version: '2.0.0-simple'
  });
});

app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    services: {
      database: 'disconnected',
      redis: 'disconnected',
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
      }
    ],
    pagination: {
      page: 1,
      limit: 20,
      total: 1,
      pages: 1
    }
  });
});

// Route pour récupérer une expérience
app.get('/api/experiences/:id', (req, res) => {
  const { id } = req.params;
  
  res.json({
    id,
    title: 'Expérience AR Demo',
    description: 'Expérience de démonstration',
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
  res.json({ message: 'Scan enregistré' });
});

// Route pour générer un QR code
app.post('/api/qr/generate', (req, res) => {
  res.json({
    qrCode: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==',
    data: req.body.data || 'demo'
  });
});

// Route 404
app.use('*', (req, res) => {
  res.status(404).json({
    error: 'Route not found',
    path: req.originalUrl
  });
});

// Démarrage
app.listen(PORT, () => {
  console.log(`🚀 Backend simple démarré sur le port ${PORT}`);
  console.log(`📊 Health Check: http://localhost:${PORT}/health`);
});
