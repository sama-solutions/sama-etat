/**
 * Routes d'authentification
 */

import { Router } from 'express';
import { body, validationResult } from 'express-validator';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { authRateLimiter } from '../middleware/rateLimiter.js';

const router = Router();

// Modèle utilisateur simplifié (en production, utiliser une vraie base de données)
const users = new Map([
  ['admin@arbase.com', {
    id: 'admin_001',
    email: 'admin@arbase.com',
    password: '$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // password
    role: 'admin',
    username: 'Admin ARBase'
  }],
  ['demo@arbase.com', {
    id: 'demo_001',
    email: 'demo@arbase.com',
    password: '$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // password
    role: 'user',
    username: 'Utilisateur Demo'
  }]
]);

// POST /api/auth/login - Connexion
router.post('/login', authRateLimiter, [
  body('email').isEmail().normalizeEmail(),
  body('password').isLength({ min: 1 })
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { email, password } = req.body;

    // Vérifier si l'utilisateur existe
    const user = users.get(email);
    if (!user) {
      return res.status(401).json({ error: 'Email ou mot de passe incorrect' });
    }

    // Vérifier le mot de passe
    const isValidPassword = await bcrypt.compare(password, user.password);
    if (!isValidPassword) {
      return res.status(401).json({ error: 'Email ou mot de passe incorrect' });
    }

    // Générer le token JWT
    const token = jwt.sign(
      { 
        id: user.id, 
        email: user.email, 
        role: user.role 
      },
      process.env.JWT_SECRET || 'default-secret',
      { expiresIn: '7d' }
    );

    res.json({
      message: 'Connexion réussie',
      token,
      user: {
        id: user.id,
        email: user.email,
        username: user.username,
        role: user.role
      }
    });
  } catch (error) {
    console.error('Erreur connexion:', error);
    res.status(500).json({ error: 'Erreur serveur' });
  }
});

// POST /api/auth/register - Inscription (désactivée pour cette démo)
router.post('/register', (req, res) => {
  res.status(501).json({ 
    error: 'Inscription désactivée pour cette démo',
    message: 'Utilisez les comptes de démonstration disponibles'
  });
});

// GET /api/auth/me - Profil utilisateur
router.get('/me', async (req, res) => {
  try {
    const token = req.header('Authorization')?.replace('Bearer ', '');
    
    if (!token) {
      return res.status(401).json({ error: 'Token requis' });
    }

    const decoded = jwt.verify(token, process.env.JWT_SECRET || 'default-secret') as any;
    const user = users.get(decoded.email);

    if (!user) {
      return res.status(404).json({ error: 'Utilisateur non trouvé' });
    }

    res.json({
      user: {
        id: user.id,
        email: user.email,
        username: user.username,
        role: user.role
      }
    });
  } catch (error) {
    res.status(401).json({ error: 'Token invalide' });
  }
});

// POST /api/auth/logout - Déconnexion
router.post('/logout', (req, res) => {
  // Dans une vraie application, on invaliderait le token
  res.json({ message: 'Déconnexion réussie' });
});

export { router as authRoutes };