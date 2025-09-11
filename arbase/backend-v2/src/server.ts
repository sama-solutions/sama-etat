/**
 * Serveur principal ARBase Backend v2
 * API REST moderne avec support WebSocket et Redis
 */

import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import morgan from 'morgan';
import { createServer } from 'http';
import { Server as SocketIOServer } from 'socket.io';
import mongoose from 'mongoose';
import dotenv from 'dotenv';

// Import des routes
import { authRoutes } from './routes/auth.js';
import { experienceRoutes } from './routes/experiences.js';
import { qrRoutes } from './routes/qr.js';
import { analyticsRoutes } from './routes/analytics.js';
import { assetsRoutes } from './routes/assets.js';
import { adminRoutes } from './routes/admin.js';

// Import des middlewares
import { errorHandler } from './middleware/errorHandler.js';
import { rateLimiter } from './middleware/rateLimiter.js';
import { authMiddleware } from './middleware/auth.js';

// Import des services
import { SocketService } from './services/SocketService.js';
import { RedisService } from './services/RedisService.js';
import { AnalyticsService } from './services/AnalyticsService.js';

// Configuration
dotenv.config();

const app = express();
const server = createServer(app);
const io = new SocketIOServer(server, {
  cors: {
    origin: process.env.FRONTEND_URL || "http://localhost:3000",
    methods: ["GET", "POST"]
  }
});

const PORT = process.env.PORT || 4000;
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/arbase_v2';

// Middleware de sécurité
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", "ws:", "wss:"],
      fontSrc: ["'self'"],
      objectSrc: ["'none'"],
      mediaSrc: ["'self'"],
      frameSrc: ["'none'"],
    },
  },
  crossOriginEmbedderPolicy: false
}));

// CORS
app.use(cors({
  origin: process.env.NODE_ENV === 'production' 
    ? [process.env.FRONTEND_URL!] 
    : ['http://localhost:3000', 'http://localhost:5173'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With']
}));

// Compression
app.use(compression());

// Logging
app.use(morgan(process.env.NODE_ENV === 'production' ? 'combined' : 'dev'));

// Body parsing
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Rate limiting
app.use(rateLimiter);

// Routes publiques
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    version: '2.0.0',
    environment: process.env.NODE_ENV || 'development'
  });
});

app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    services: {
      database: mongoose.connection.readyState === 1 ? 'connected' : 'disconnected',
      redis: RedisService.isConnected() ? 'connected' : 'disconnected',
      websocket: 'active'
    },
    timestamp: new Date().toISOString()
  });
});

// Routes API
app.use('/api/auth', authRoutes);
app.use('/api/experiences', experienceRoutes);
app.use('/api/qr', qrRoutes);
app.use('/api/analytics', analyticsRoutes);
app.use('/api/assets', assetsRoutes);
app.use('/api/admin', authMiddleware, adminRoutes);

// Servir les fichiers statiques
app.use('/uploads', express.static('uploads'));

// Route 404
app.use('*', (req, res) => {
  res.status(404).json({
    error: 'Route not found',
    path: req.originalUrl,
    method: req.method
  });
});

// Gestionnaire d'erreurs
app.use(errorHandler);

// Configuration WebSocket
const socketService = new SocketService(io);

// Connexion à MongoDB
async function connectDatabase() {
  try {
    await mongoose.connect(MONGODB_URI);
    console.log('✅ Connecté à MongoDB');
  } catch (error) {
    console.error('❌ Erreur de connexion MongoDB:', error);
    process.exit(1);
  }
}

// Connexion à Redis
async function connectRedis() {
  try {
    await RedisService.connect();
    console.log('✅ Connecté à Redis');
  } catch (error) {
    console.warn('⚠️  Redis non disponible, fonctionnement en mode dégradé');
  }
}

// Initialisation des services
async function initializeServices() {
  try {
    await AnalyticsService.initialize();
    console.log('✅ Services d\'analytics initialisés');
  } catch (error) {
    console.error('❌ Erreur d\'initialisation des services:', error);
  }
}

// Démarrage du serveur
async function startServer() {
  try {
    // Connexions aux bases de données
    await connectDatabase();
    await connectRedis();
    
    // Initialisation des services
    await initializeServices();
    
    // Démarrage du serveur HTTP
    server.listen(PORT, () => {
      console.log(`🚀 Serveur ARBase démarré sur le port ${PORT}`);
      console.log(`📱 Frontend URL: ${process.env.FRONTEND_URL || 'http://localhost:3000'}`);
      console.log(`🔗 API URL: http://localhost:${PORT}/api`);
      console.log(`📊 Health Check: http://localhost:${PORT}/health`);
      console.log(`🌍 Environnement: ${process.env.NODE_ENV || 'development'}`);
    });
  } catch (error) {
    console.error('❌ Erreur de démarrage du serveur:', error);
    process.exit(1);
  }
}

// Gestion des signaux de fermeture
process.on('SIGTERM', async () => {
  console.log('🔄 Arrêt du serveur...');
  
  server.close(async () => {
    await mongoose.connection.close();
    await RedisService.disconnect();
    console.log('✅ Serveur arrêté proprement');
    process.exit(0);
  });
});

process.on('SIGINT', async () => {
  console.log('🔄 Arrêt du serveur (SIGINT)...');
  
  server.close(async () => {
    await mongoose.connection.close();
    await RedisService.disconnect();
    console.log('✅ Serveur arrêté proprement');
    process.exit(0);
  });
});

// Gestion des erreurs non capturées
process.on('uncaughtException', (error) => {
  console.error('❌ Erreur non capturée:', error);
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('❌ Promesse rejetée non gérée:', reason);
  process.exit(1);
});

// Démarrage
startServer();

export { app, server, io };