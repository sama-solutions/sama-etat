/**
 * Routes pour la gestion des expériences AR
 */

import { Router } from 'express';
import { body, param, query, validationResult } from 'express-validator';
import { Experience, IExperience } from '../models/Experience.js';
import { authMiddleware, optionalAuthMiddleware } from '../middleware/auth.js';
import { RedisService } from '../services/RedisService.js';
import { AnalyticsService } from '../services/AnalyticsService.js';

const router = Router();

// Validation schemas
const createExperienceValidation = [
  body('title').isLength({ min: 1, max: 100 }).trim().escape(),
  body('description').optional().isLength({ max: 500 }).trim().escape(),
  body('qrCode').isLength({ min: 1 }).trim(),
  body('content').isArray({ min: 1 }),
  body('content.*.type').isIn(['model', 'text', 'image', 'video', 'html']),
  body('isPublic').optional().isBoolean(),
  body('category').optional().isIn(['business-card', 'product', 'art', 'education', 'entertainment', 'other']),
  body('tags').optional().isArray()
];

// GET /api/experiences/public - Récupérer les expériences publiques
router.get('/public', async (req, res) => {
  try {
    const page = parseInt(req.query.page as string) || 1;
    const limit = Math.min(parseInt(req.query.limit as string) || 20, 100);
    const category = req.query.category as string;
    const search = req.query.search as string;
    const sort = req.query.sort as string || 'recent';

    // Construire la requête
    let query: any = { isPublic: true, isActive: true };
    
    if (category) {
      query.category = category;
    }
    
    if (search) {
      query.$or = [
        { title: { $regex: search, $options: 'i' } },
        { description: { $regex: search, $options: 'i' } },
        { tags: { $in: [new RegExp(search, 'i')] } }
      ];
    }

    // Définir le tri
    let sortQuery: any = {};
    switch (sort) {
      case 'popular':
        sortQuery = { views: -1, scans: -1 };
        break;
      case 'recent':
        sortQuery = { createdAt: -1 };
        break;
      case 'alphabetical':
        sortQuery = { title: 1 };
        break;
      default:
        sortQuery = { createdAt: -1 };
    }

    const skip = (page - 1) * limit;
    
    const [results, total] = await Promise.all([
      Experience.find(query)
        .sort(sortQuery)
        .skip(skip)
        .limit(limit)
        .select('-qrCodeImage')
        .lean(),
      Experience.countDocuments(query)
    ]);

    const experiences = {
      experiences: results,
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit),
        hasNext: page < Math.ceil(total / limit),
        hasPrev: page > 1
      }
    };

    res.json(experiences);
  } catch (error) {
    console.error('Erreur récupération expériences publiques:', error);
    res.status(500).json({ error: 'Erreur serveur' });
  }
});

// GET /api/experiences/:id - Récupérer une expérience spécifique
router.get('/:id', optionalAuthMiddleware, async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user?.id;

    const experience = await Experience.findOne({ id }).lean();

    if (!experience) {
      return res.status(404).json({ error: 'Expérience non trouvée' });
    }

    // Vérifier les permissions
    if (!experience.isPublic && (!userId || experience.createdBy.toString() !== userId)) {
      return res.status(403).json({ error: 'Accès non autorisé' });
    }

    // Incrémenter les vues (de manière asynchrone)
    Experience.findOneAndUpdate(
      { id },
      { $inc: { views: 1 } }
    ).exec().catch(console.error);

    res.json(experience);
  } catch (error) {
    console.error('Erreur récupération expérience:', error);
    res.status(500).json({ error: 'Erreur serveur' });
  }
});

// POST /api/experiences - Créer une nouvelle expérience
router.post('/', authMiddleware, createExperienceValidation, async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const userId = req.user!.id;
    const experienceData = {
      ...req.body,
      id: `exp_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      createdBy: userId
    };

    const experience = new Experience(experienceData);
    await experience.save();

    res.status(201).json({
      message: 'Expérience créée avec succès',
      experience: {
        id: experience.id,
        title: experience.title,
        qrCode: experience.qrCode,
        qrCodeImage: experience.qrCodeImage
      }
    });
  } catch (error) {
    console.error('Erreur création expérience:', error);
    
    if (error.code === 11000) {
      return res.status(409).json({ error: 'QR code déjà utilisé' });
    }
    
    res.status(500).json({ error: 'Erreur serveur' });
  }
});

// POST /api/experiences/:id/scan - Enregistrer un scan
router.post('/:id/scan', async (req, res) => {
  try {
    const { id } = req.params;

    const experience = await Experience.findOne({ id, isActive: true });
    if (!experience) {
      return res.status(404).json({ error: 'Expérience non trouvée' });
    }

    // Incrémenter les scans
    await experience.incrementScans();

    res.json({
      message: 'Scan enregistré',
      experience: {
        id: experience.id,
        title: experience.title,
        content: experience.content,
        settings: experience.settings
      }
    });
  } catch (error) {
    console.error('Erreur enregistrement scan:', error);
    res.status(500).json({ error: 'Erreur serveur' });
  }
});

export { router as experienceRoutes };