/**
 * Routes pour la gestion des QR codes
 */

import { Router } from 'express';
import { body, param, validationResult } from 'express-validator';
import QRCode from 'qrcode';
import { Experience } from '../models/Experience.js';
import { authMiddleware } from '../middleware/auth.js';

const router = Router();

// POST /api/qr/generate - Générer un QR code
router.post('/generate', authMiddleware, [
  body('data').isLength({ min: 1 }).withMessage('Les données sont requises'),
  body('size').optional().isInt({ min: 64, max: 1024 }).withMessage('Taille invalide'),
  body('errorCorrectionLevel').optional().isIn(['L', 'M', 'Q', 'H']).withMessage('Niveau de correction invalide')
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { data, size = 256, errorCorrectionLevel = 'M' } = req.body;

    const qrCodeOptions = {
      errorCorrectionLevel,
      type: 'image/png' as const,
      quality: 0.92,
      margin: 1,
      color: {
        dark: '#000000',
        light: '#FFFFFF'
      },
      width: size
    };

    // Générer le QR code en base64
    const qrCodeDataURL = await QRCode.toDataURL(data, qrCodeOptions);

    res.json({
      qrCode: qrCodeDataURL,
      data,
      size,
      errorCorrectionLevel
    });
  } catch (error) {
    console.error('Erreur génération QR code:', error);
    res.status(500).json({ error: 'Erreur lors de la génération du QR code' });
  }
});

// GET /api/qr/scanner - QR code pour accéder au scanner
router.get('/scanner', async (req, res) => {
  try {
    const scannerUrl = `${process.env.FRONTEND_URL || 'http://localhost:3000'}/scanner`;
    
    const qrCodeOptions = {
      errorCorrectionLevel: 'M' as const,
      type: 'image/png' as const,
      quality: 0.92,
      margin: 1,
      color: {
        dark: '#000000',
        light: '#FFFFFF'
      },
      width: 256
    };

    const qrCodeDataURL = await QRCode.toDataURL(scannerUrl, qrCodeOptions);

    res.json({
      qr: {
        url: scannerUrl,
        image: qrCodeDataURL
      }
    });
  } catch (error) {
    console.error('Erreur génération QR scanner:', error);
    res.status(500).json({ error: 'Erreur lors de la génération du QR code' });
  }
});

// GET /api/qr/experience/:id - QR code pour une expérience spécifique
router.get('/experience/:id', async (req, res) => {
  try {
    const { id } = req.params;

    const experience = await Experience.findOne({ id, isActive: true });
    if (!experience) {
      return res.status(404).json({ error: 'Expérience non trouvée' });
    }

    // URL de l'expérience
    const experienceUrl = `${process.env.FRONTEND_URL || 'http://localhost:3000'}/experience/${id}`;
    
    // Données du QR code avec métadonnées
    const qrData = {
      type: 'arbase_experience',
      id: experience.id,
      title: experience.title,
      url: experienceUrl
    };

    const qrCodeOptions = {
      errorCorrectionLevel: 'M' as const,
      type: 'image/png' as const,
      quality: 0.92,
      margin: 1,
      color: {
        dark: '#000000',
        light: '#FFFFFF'
      },
      width: 256
    };

    const qrCodeDataURL = await QRCode.toDataURL(JSON.stringify(qrData), qrCodeOptions);

    res.json({
      qr: {
        data: qrData,
        url: experienceUrl,
        image: qrCodeDataURL
      },
      experience: {
        id: experience.id,
        title: experience.title,
        description: experience.description,
        category: experience.category
      }
    });
  } catch (error) {
    console.error('Erreur génération QR expérience:', error);
    res.status(500).json({ error: 'Erreur lors de la génération du QR code' });
  }
});

// POST /api/qr/decode - Décoder un QR code
router.post('/decode', [
  body('image').isLength({ min: 1 }).withMessage('Image requise')
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { image } = req.body;

    // Note: Pour décoder un QR code, nous aurions besoin d'une bibliothèque comme jimp + qrcode-reader
    // Pour cette implémentation, nous retournons une réponse simulée
    
    res.json({
      message: 'Décodage QR code non implémenté dans cette version',
      suggestion: 'Utilisez le scanner frontend pour décoder les QR codes'
    });
  } catch (error) {
    console.error('Erreur décodage QR code:', error);
    res.status(500).json({ error: 'Erreur lors du décodage du QR code' });
  }
});

// GET /api/qr/batch/:experienceId - Générer plusieurs QR codes pour une expérience
router.get('/batch/:experienceId', authMiddleware, async (req, res) => {
  try {
    const { experienceId } = req.params;
    const userId = req.user!.id;
    const sizes = [128, 256, 512, 1024];

    const experience = await Experience.findOne({ id: experienceId });
    if (!experience) {
      return res.status(404).json({ error: 'Expérience non trouvée' });
    }

    // Vérifier les permissions
    if (experience.createdBy.toString() !== userId) {
      return res.status(403).json({ error: 'Accès non autorisé' });
    }

    const experienceUrl = `${process.env.FRONTEND_URL || 'http://localhost:3000'}/experience/${experienceId}`;
    
    const qrData = {
      type: 'arbase_experience',
      id: experience.id,
      title: experience.title,
      url: experienceUrl
    };

    // Générer les QR codes pour différentes tailles
    const qrCodes = await Promise.all(
      sizes.map(async (size) => {
        const qrCodeOptions = {
          errorCorrectionLevel: 'M' as const,
          type: 'image/png' as const,
          quality: 0.92,
          margin: 1,
          color: {
            dark: '#000000',
            light: '#FFFFFF'
          },
          width: size
        };

        const qrCodeDataURL = await QRCode.toDataURL(JSON.stringify(qrData), qrCodeOptions);
        
        return {
          size,
          image: qrCodeDataURL,
          filename: `qr_${experience.id}_${size}x${size}.png`
        };
      })
    );

    res.json({
      experience: {
        id: experience.id,
        title: experience.title
      },
      qrCodes,
      data: qrData
    });
  } catch (error) {
    console.error('Erreur génération QR codes batch:', error);
    res.status(500).json({ error: 'Erreur lors de la génération des QR codes' });
  }
});

// GET /api/qr/stats - Statistiques des QR codes
router.get('/stats', authMiddleware, async (req, res) => {
  try {
    const userId = req.user!.id;

    // Statistiques des expériences de l'utilisateur
    const stats = await Experience.aggregate([
      { $match: { createdBy: userId } },
      {
        $group: {
          _id: null,
          totalExperiences: { $sum: 1 },
          totalScans: { $sum: '$scans' },
          totalViews: { $sum: '$views' },
          totalInteractions: { $sum: '$interactions' },
          avgScansPerExperience: { $avg: '$scans' },
          avgViewsPerExperience: { $avg: '$views' }
        }
      }
    ]);

    const result = stats[0] || {
      totalExperiences: 0,
      totalScans: 0,
      totalViews: 0,
      totalInteractions: 0,
      avgScansPerExperience: 0,
      avgViewsPerExperience: 0
    };

    // Expériences les plus scannées
    const topExperiences = await Experience.find({ createdBy: userId })
      .sort({ scans: -1 })
      .limit(5)
      .select('id title scans views interactions category')
      .lean();

    res.json({
      stats: result,
      topExperiences
    });
  } catch (error) {
    console.error('Erreur récupération stats QR:', error);
    res.status(500).json({ error: 'Erreur serveur' });
  }
});

export { router as qrRoutes };