/**
 * Routes pour la gestion des assets (fichiers)
 */

import { Router } from 'express';
import multer from 'multer';
import sharp from 'sharp';
import path from 'path';
import fs from 'fs/promises';
import { authMiddleware } from '../middleware/auth.js';

const router = Router();

// Configuration Multer pour l'upload
const storage = multer.diskStorage({
  destination: async (req, file, cb) => {
    const uploadDir = 'uploads';
    try {
      await fs.mkdir(uploadDir, { recursive: true });
      cb(null, uploadDir);
    } catch (error) {
      cb(error, uploadDir);
    }
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
  }
});

const upload = multer({
  storage,
  limits: {
    fileSize: 10 * 1024 * 1024, // 10MB
    files: 5
  },
  fileFilter: (req, file, cb) => {
    const allowedTypes = [
      'image/jpeg',
      'image/png',
      'image/gif',
      'image/webp',
      'video/mp4',
      'video/webm',
      'model/gltf+json',
      'model/gltf-binary'
    ];

    if (allowedTypes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error('Type de fichier non autorisé'));
    }
  }
});

// POST /api/assets/upload - Upload de fichiers
router.post('/upload', authMiddleware, upload.array('files', 5), async (req, res) => {
  try {
    const files = req.files as Express.Multer.File[];
    
    if (!files || files.length === 0) {
      return res.status(400).json({ error: 'Aucun fichier fourni' });
    }

    const processedFiles = await Promise.all(
      files.map(async (file) => {
        let processedPath = file.path;
        
        // Traitement des images
        if (file.mimetype.startsWith('image/')) {
          const outputPath = file.path.replace(path.extname(file.path), '_processed.webp');
          
          await sharp(file.path)
            .resize(1920, 1080, { 
              fit: 'inside',
              withoutEnlargement: true 
            })
            .webp({ quality: 85 })
            .toFile(outputPath);
          
          // Supprimer l'original et utiliser la version traitée
          await fs.unlink(file.path);
          processedPath = outputPath;
        }

        return {
          originalName: file.originalname,
          filename: path.basename(processedPath),
          path: processedPath,
          mimetype: file.mimetype.startsWith('image/') ? 'image/webp' : file.mimetype,
          size: (await fs.stat(processedPath)).size,
          url: `/uploads/${path.basename(processedPath)}`
        };
      })
    );

    res.json({
      message: 'Fichiers uploadés avec succès',
      files: processedFiles
    });
  } catch (error) {
    console.error('Erreur upload:', error);
    res.status(500).json({ error: 'Erreur lors de l\'upload' });
  }
});

// GET /api/assets/:filename - Récupérer un asset
router.get('/:filename', async (req, res) => {
  try {
    const { filename } = req.params;
    const filePath = path.join('uploads', filename);

    // Vérifier que le fichier existe
    try {
      await fs.access(filePath);
    } catch {
      return res.status(404).json({ error: 'Fichier non trouvé' });
    }

    // Définir le type de contenu
    const ext = path.extname(filename).toLowerCase();
    const mimeTypes: { [key: string]: string } = {
      '.jpg': 'image/jpeg',
      '.jpeg': 'image/jpeg',
      '.png': 'image/png',
      '.gif': 'image/gif',
      '.webp': 'image/webp',
      '.mp4': 'video/mp4',
      '.webm': 'video/webm',
      '.gltf': 'model/gltf+json',
      '.glb': 'model/gltf-binary'
    };

    const contentType = mimeTypes[ext] || 'application/octet-stream';
    res.setHeader('Content-Type', contentType);
    res.setHeader('Cache-Control', 'public, max-age=31536000'); // 1 an

    res.sendFile(path.resolve(filePath));
  } catch (error) {
    console.error('Erreur récupération asset:', error);
    res.status(500).json({ error: 'Erreur serveur' });
  }
});

// DELETE /api/assets/:filename - Supprimer un asset
router.delete('/:filename', authMiddleware, async (req, res) => {
  try {
    const { filename } = req.params;
    const filePath = path.join('uploads', filename);

    // Vérifier que le fichier existe
    try {
      await fs.access(filePath);
    } catch {
      return res.status(404).json({ error: 'Fichier non trouvé' });
    }

    // Supprimer le fichier
    await fs.unlink(filePath);

    res.json({ message: 'Fichier supprimé avec succès' });
  } catch (error) {
    console.error('Erreur suppression asset:', error);
    res.status(500).json({ error: 'Erreur serveur' });
  }
});

// GET /api/assets - Lister les assets de l'utilisateur
router.get('/', authMiddleware, async (req, res) => {
  try {
    const uploadsDir = 'uploads';
    
    try {
      const files = await fs.readdir(uploadsDir);
      
      const assets = await Promise.all(
        files.map(async (filename) => {
          const filePath = path.join(uploadsDir, filename);
          const stats = await fs.stat(filePath);
          
          return {
            filename,
            url: `/uploads/${filename}`,
            size: stats.size,
            createdAt: stats.birthtime,
            modifiedAt: stats.mtime
          };
        })
      );

      res.json({
        assets: assets.sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime())
      });
    } catch {
      res.json({ assets: [] });
    }
  } catch (error) {
    console.error('Erreur listage assets:', error);
    res.status(500).json({ error: 'Erreur serveur' });
  }
});

export { router as assetsRoutes };