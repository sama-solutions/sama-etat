/**
 * Routes d'administration
 */

import { Router } from 'express';
import { adminMiddleware } from '../middleware/auth.js';
import { Experience } from '../models/Experience.js';
import { AnalyticsService } from '../services/AnalyticsService.js';

const router = Router();

// GET /api/admin/stats - Statistiques globales
router.get('/stats', adminMiddleware, async (req, res) => {
  try {
    const [
      totalExperiences,
      publicExperiences,
      activeExperiences,
      totalViews,
      totalScans,
      totalInteractions
    ] = await Promise.all([
      Experience.countDocuments(),
      Experience.countDocuments({ isPublic: true }),
      Experience.countDocuments({ isActive: true }),
      Experience.aggregate([{ $group: { _id: null, total: { $sum: '$views' } } }]),
      Experience.aggregate([{ $group: { _id: null, total: { $sum: '$scans' } } }]),
      Experience.aggregate([{ $group: { _id: null, total: { $sum: '$interactions' } } }])
    ]);

    const stats = {
      experiences: {
        total: totalExperiences,
        public: publicExperiences,
        active: activeExperiences,
        private: totalExperiences - publicExperiences
      },
      engagement: {
        totalViews: totalViews[0]?.total || 0,
        totalScans: totalScans[0]?.total || 0,
        totalInteractions: totalInteractions[0]?.total || 0
      }
    };

    // Calculer les taux
    stats.engagement.conversionRate = stats.engagement.totalViews > 0 
      ? (stats.engagement.totalScans / stats.engagement.totalViews * 100).toFixed(2)
      : '0';
    
    stats.engagement.engagementRate = stats.engagement.totalScans > 0
      ? (stats.engagement.totalInteractions / stats.engagement.totalScans * 100).toFixed(2)
      : '0';

    res.json(stats);
  } catch (error) {
    console.error('Erreur récupération stats admin:', error);
    res.status(500).json({ error: 'Erreur serveur' });
  }
});

// GET /api/admin/experiences - Toutes les expériences
router.get('/experiences', adminMiddleware, async (req, res) => {
  try {
    const page = parseInt(req.query.page as string) || 1;
    const limit = Math.min(parseInt(req.query.limit as string) || 20, 100);
    const status = req.query.status as string; // 'active', 'inactive', 'public', 'private'

    let query: any = {};
    
    switch (status) {
      case 'active':
        query.isActive = true;
        break;
      case 'inactive':
        query.isActive = false;
        break;
      case 'public':
        query.isPublic = true;
        break;
      case 'private':
        query.isPublic = false;
        break;
    }

    const skip = (page - 1) * limit;

    const [experiences, total] = await Promise.all([
      Experience.find(query)
        .sort({ createdAt: -1 })
        .skip(skip)
        .limit(limit)
        .populate('createdBy', 'username email')
        .lean(),
      Experience.countDocuments(query)
    ]);

    res.json({
      experiences,
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit),
        hasNext: page < Math.ceil(total / limit),
        hasPrev: page > 1
      }
    });
  } catch (error) {
    console.error('Erreur récupération expériences admin:', error);
    res.status(500).json({ error: 'Erreur serveur' });
  }
});

// PUT /api/admin/experiences/:id/status - Modifier le statut d'une expérience
router.put('/experiences/:id/status', adminMiddleware, async (req, res) => {
  try {
    const { id } = req.params;
    const { isActive, isPublic } = req.body;

    const experience = await Experience.findOne({ id });
    if (!experience) {
      return res.status(404).json({ error: 'Expérience non trouvée' });
    }

    if (typeof isActive === 'boolean') {
      experience.isActive = isActive;
    }
    
    if (typeof isPublic === 'boolean') {
      experience.isPublic = isPublic;
    }

    await experience.save();

    res.json({
      message: 'Statut mis à jour avec succès',
      experience: {
        id: experience.id,
        isActive: experience.isActive,
        isPublic: experience.isPublic
      }
    });
  } catch (error) {
    console.error('Erreur modification statut expérience:', error);
    res.status(500).json({ error: 'Erreur serveur' });
  }
});

// DELETE /api/admin/experiences/:id - Supprimer une expérience
router.delete('/experiences/:id', adminMiddleware, async (req, res) => {
  try {
    const { id } = req.params;

    const experience = await Experience.findOne({ id });
    if (!experience) {
      return res.status(404).json({ error: 'Expérience non trouvée' });
    }

    await Experience.deleteOne({ id });

    res.json({ message: 'Expérience supprimée avec succès' });
  } catch (error) {
    console.error('Erreur suppression expérience admin:', error);
    res.status(500).json({ error: 'Erreur serveur' });
  }
});

// GET /api/admin/analytics - Analytics détaillées
router.get('/analytics', adminMiddleware, async (req, res) => {
  try {
    const days = parseInt(req.query.days as string) || 30;

    // Récupérer les analytics globales
    const globalStats = await AnalyticsService.getGlobalStats(days);

    // Top expériences par catégorie
    const topByCategory = await Experience.aggregate([
      { $match: { isPublic: true, isActive: true } },
      {
        $group: {
          _id: '$category',
          totalViews: { $sum: '$views' },
          totalScans: { $sum: '$scans' },
          totalInteractions: { $sum: '$interactions' },
          count: { $sum: 1 }
        }
      },
      { $sort: { totalViews: -1 } }
    ]);

    // Expériences les plus populaires
    const topExperiences = await Experience.find({
      isPublic: true,
      isActive: true
    })
      .sort({ views: -1, scans: -1 })
      .limit(10)
      .select('id title category views scans interactions createdAt')
      .populate('createdBy', 'username')
      .lean();

    res.json({
      period: {
        days,
        from: new Date(Date.now() - days * 24 * 60 * 60 * 1000).toISOString(),
        to: new Date().toISOString()
      },
      globalStats,
      topByCategory,
      topExperiences
    });
  } catch (error) {
    console.error('Erreur récupération analytics admin:', error);
    res.status(500).json({ error: 'Erreur serveur' });
  }
});

export { router as adminRoutes };