/**
 * Routes pour les analytics
 */

import { Router } from 'express';
import { param, query, validationResult } from 'express-validator';
import { authMiddleware } from '../middleware/auth.js';
import { AnalyticsService } from '../services/AnalyticsService.js';
import { Experience } from '../models/Experience.js';

const router = Router();

// GET /api/analytics/experience/:id - Analytics d'une expérience
router.get('/experience/:id', authMiddleware, [
  param('id').isLength({ min: 1 }),
  query('days').optional().isInt({ min: 1, max: 365 })
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { id } = req.params;
    const days = parseInt(req.query.days as string) || 7;
    const userId = req.user!.id;

    // Vérifier que l'expérience appartient à l'utilisateur
    const experience = await Experience.findOne({ id });
    if (!experience) {
      return res.status(404).json({ error: 'Expérience non trouvée' });
    }

    if (experience.createdBy.toString() !== userId) {
      return res.status(403).json({ error: 'Accès non autorisé' });
    }

    // Récupérer les analytics
    const stats = await AnalyticsService.getExperienceStats(id, days);

    res.json({
      experienceId: id,
      period: {
        days,
        from: new Date(Date.now() - days * 24 * 60 * 60 * 1000).toISOString(),
        to: new Date().toISOString()
      },
      stats
    });
  } catch (error) {
    console.error('Erreur récupération analytics expérience:', error);
    res.status(500).json({ error: 'Erreur serveur' });
  }
});

// GET /api/analytics/global - Analytics globales (admin seulement)
router.get('/global', authMiddleware, [
  query('days').optional().isInt({ min: 1, max: 365 })
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    // Vérifier les permissions admin
    if (req.user!.role !== 'admin') {
      return res.status(403).json({ error: 'Accès administrateur requis' });
    }

    const days = parseInt(req.query.days as string) || 7;

    // Récupérer les analytics globales
    const stats = await AnalyticsService.getGlobalStats(days);

    res.json({
      period: {
        days,
        from: new Date(Date.now() - days * 24 * 60 * 60 * 1000).toISOString(),
        to: new Date().toISOString()
      },
      stats
    });
  } catch (error) {
    console.error('Erreur récupération analytics globales:', error);
    res.status(500).json({ error: 'Erreur serveur' });
  }
});

// GET /api/analytics/dashboard - Dashboard utilisateur
router.get('/dashboard', authMiddleware, async (req, res) => {
  try {
    const userId = req.user!.id;

    // Récupérer les expériences de l'utilisateur
    const experiences = await Experience.find({ createdBy: userId })
      .select('id title views scans interactions createdAt')
      .sort({ updatedAt: -1 })
      .limit(10)
      .lean();

    // Calculer les totaux
    const totals = experiences.reduce((acc, exp) => ({
      views: acc.views + exp.views,
      scans: acc.scans + exp.scans,
      interactions: acc.interactions + exp.interactions
    }), { views: 0, scans: 0, interactions: 0 });

    // Expérience la plus populaire
    const topExperience = experiences.reduce((top, exp) => 
      exp.views > (top?.views || 0) ? exp : top, null);

    res.json({
      summary: {
        totalExperiences: experiences.length,
        totalViews: totals.views,
        totalScans: totals.scans,
        totalInteractions: totals.interactions,
        conversionRate: totals.views > 0 ? (totals.scans / totals.views * 100).toFixed(2) : 0,
        engagementRate: totals.scans > 0 ? (totals.interactions / totals.scans * 100).toFixed(2) : 0
      },
      topExperience,
      recentExperiences: experiences.slice(0, 5)
    });
  } catch (error) {
    console.error('Erreur récupération dashboard:', error);
    res.status(500).json({ error: 'Erreur serveur' });
  }
});

// GET /api/analytics/realtime/:id - Analytics temps réel
router.get('/realtime/:id', authMiddleware, [
  param('id').isLength({ min: 1 })
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { id } = req.params;
    const userId = req.user!.id;

    // Vérifier les permissions
    const experience = await Experience.findOne({ id });
    if (!experience) {
      return res.status(404).json({ error: 'Expérience non trouvée' });
    }

    if (experience.createdBy.toString() !== userId) {
      return res.status(403).json({ error: 'Accès non autorisé' });
    }

    // Récupérer les stats temps réel via WebSocket service
    // Pour cette implémentation, on retourne des données simulées
    const realtimeStats = {
      activeUsers: Math.floor(Math.random() * 10),
      currentScans: Math.floor(Math.random() * 5),
      currentInteractions: Math.floor(Math.random() * 15),
      timestamp: new Date()
    };

    res.json(realtimeStats);
  } catch (error) {
    console.error('Erreur récupération analytics temps réel:', error);
    res.status(500).json({ error: 'Erreur serveur' });
  }
});

export { router as analyticsRoutes };