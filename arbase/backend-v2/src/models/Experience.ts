/**
 * Modèle Experience - Expériences de réalité augmentée
 */

import mongoose, { Schema, Document } from 'mongoose';

export interface IARContent {
  type: 'model' | 'text' | 'image' | 'video' | 'html';
  data: any;
  position: {
    x: number;
    y: number;
    z: number;
  };
  rotation: {
    x: number;
    y: number;
    z: number;
  };
  scale: {
    x: number;
    y: number;
    z: number;
  };
  animations?: Array<{
    type: 'rotation' | 'scale' | 'position' | 'opacity';
    duration: number;
    loop: boolean;
    easing: string;
    keyframes: any[];
  }>;
  interactions?: Array<{
    type: 'click' | 'hover' | 'gaze';
    action: 'url' | 'animation' | 'sound' | 'custom';
    data: any;
  }>;
}

export interface IARSettings {
  autoStart: boolean;
  trackingMode: 'qr' | 'marker' | 'markerless';
  renderDistance: number;
  occlusionCulling: boolean;
}

export interface IExperience extends Document {
  id: string;
  title: string;
  description?: string;
  qrCode: string;
  qrCodeImage?: string;
  content: IARContent[];
  settings: IARSettings;
  
  // Métadonnées
  createdBy: mongoose.Types.ObjectId;
  isPublic: boolean;
  isActive: boolean;
  tags: string[];
  category: string;
  
  // Analytics
  views: number;
  scans: number;
  interactions: number;
  averageSessionTime: number;
  
  // Timestamps
  createdAt: Date;
  updatedAt: Date;
  publishedAt?: Date;
  
  // Méthodes
  generateQRCode(): Promise<string>;
  incrementViews(): Promise<void>;
  incrementScans(): Promise<void>;
  addInteraction(type: string, data?: any): Promise<void>;
}

const ARContentSchema = new Schema({
  type: {
    type: String,
    enum: ['model', 'text', 'image', 'video', 'html'],
    required: true
  },
  data: {
    type: Schema.Types.Mixed,
    required: true
  },
  position: {
    x: { type: Number, default: 0 },
    y: { type: Number, default: 0 },
    z: { type: Number, default: 0 }
  },
  rotation: {
    x: { type: Number, default: 0 },
    y: { type: Number, default: 0 },
    z: { type: Number, default: 0 }
  },
  scale: {
    x: { type: Number, default: 1 },
    y: { type: Number, default: 1 },
    z: { type: Number, default: 1 }
  },
  animations: [{
    type: {
      type: String,
      enum: ['rotation', 'scale', 'position', 'opacity']
    },
    duration: Number,
    loop: Boolean,
    easing: String,
    keyframes: [Schema.Types.Mixed]
  }],
  interactions: [{
    type: {
      type: String,
      enum: ['click', 'hover', 'gaze']
    },
    action: {
      type: String,
      enum: ['url', 'animation', 'sound', 'custom']
    },
    data: Schema.Types.Mixed
  }]
});

const ARSettingsSchema = new Schema({
  autoStart: { type: Boolean, default: true },
  trackingMode: {
    type: String,
    enum: ['qr', 'marker', 'markerless'],
    default: 'qr'
  },
  renderDistance: { type: Number, default: 10 },
  occlusionCulling: { type: Boolean, default: false }
});

const ExperienceSchema = new Schema({
  id: {
    type: String,
    required: true,
    unique: true,
    index: true
  },
  title: {
    type: String,
    required: true,
    trim: true,
    maxlength: 100
  },
  description: {
    type: String,
    trim: true,
    maxlength: 500
  },
  qrCode: {
    type: String,
    required: true,
    unique: true,
    index: true
  },
  qrCodeImage: {
    type: String // URL de l'image QR code générée
  },
  content: [ARContentSchema],
  settings: {
    type: ARSettingsSchema,
    default: () => ({})
  },
  
  // Métadonnées
  createdBy: {
    type: Schema.Types.ObjectId,
    ref: 'User',
    required: true,
    index: true
  },
  isPublic: {
    type: Boolean,
    default: false,
    index: true
  },
  isActive: {
    type: Boolean,
    default: true,
    index: true
  },
  tags: [{
    type: String,
    trim: true,
    lowercase: true
  }],
  category: {
    type: String,
    enum: ['business-card', 'product', 'art', 'education', 'entertainment', 'other'],
    default: 'other',
    index: true
  },
  
  // Analytics
  views: {
    type: Number,
    default: 0,
    min: 0
  },
  scans: {
    type: Number,
    default: 0,
    min: 0
  },
  interactions: {
    type: Number,
    default: 0,
    min: 0
  },
  averageSessionTime: {
    type: Number,
    default: 0,
    min: 0
  },
  
  // Timestamps
  publishedAt: Date
}, {
  timestamps: true,
  toJSON: { virtuals: true },
  toObject: { virtuals: true }
});

// Index composés pour les requêtes fréquentes
ExperienceSchema.index({ isPublic: 1, isActive: 1, createdAt: -1 });
ExperienceSchema.index({ createdBy: 1, isActive: 1, updatedAt: -1 });
ExperienceSchema.index({ category: 1, isPublic: 1, views: -1 });
ExperienceSchema.index({ tags: 1, isPublic: 1 });

// Virtuals
ExperienceSchema.virtual('engagementRate').get(function() {
  return this.scans > 0 ? (this.interactions / this.scans) * 100 : 0;
});

ExperienceSchema.virtual('conversionRate').get(function() {
  return this.views > 0 ? (this.scans / this.views) * 100 : 0;
});

// Méthodes d'instance
ExperienceSchema.methods.generateQRCode = async function(): Promise<string> {
  const QRCode = await import('qrcode');
  const qrData = {
    type: 'arbase_experience',
    id: this.id,
    url: `${process.env.FRONTEND_URL}/experience/${this.id}`
  };
  
  const qrCodeDataURL = await QRCode.toDataURL(JSON.stringify(qrData), {
    errorCorrectionLevel: 'M',
    type: 'image/png',
    quality: 0.92,
    margin: 1,
    color: {
      dark: '#000000',
      light: '#FFFFFF'
    },
    width: 256
  });
  
  return qrCodeDataURL;
};

ExperienceSchema.methods.incrementViews = async function(): Promise<void> {
  this.views += 1;
  await this.save();
};

ExperienceSchema.methods.incrementScans = async function(): Promise<void> {
  this.scans += 1;
  await this.save();
};

ExperienceSchema.methods.addInteraction = async function(type: string, data?: any): Promise<void> {
  this.interactions += 1;
  await this.save();
  
  // Enregistrer l'interaction détaillée dans les analytics
  const AnalyticsService = await import('../services/AnalyticsService.js');
  await AnalyticsService.AnalyticsService.recordInteraction(this.id, type, data);
};

// Méthodes statiques
ExperienceSchema.statics.findPublic = function() {
  return this.find({ isPublic: true, isActive: true });
};

ExperienceSchema.statics.findByCategory = function(category: string) {
  return this.find({ category, isPublic: true, isActive: true });
};

ExperienceSchema.statics.findPopular = function(limit: number = 10) {
  return this.find({ isPublic: true, isActive: true })
    .sort({ views: -1, scans: -1 })
    .limit(limit);
};

ExperienceSchema.statics.search = function(query: string) {
  return this.find({
    isPublic: true,
    isActive: true,
    $or: [
      { title: { $regex: query, $options: 'i' } },
      { description: { $regex: query, $options: 'i' } },
      { tags: { $in: [new RegExp(query, 'i')] } }
    ]
  });
};

// Middleware pre-save
ExperienceSchema.pre('save', async function(next) {
  if (this.isNew || this.isModified('content')) {
    // Générer le QR code si nécessaire
    if (!this.qrCodeImage) {
      try {
        this.qrCodeImage = await this.generateQRCode();
      } catch (error) {
        console.error('Erreur génération QR code:', error);
      }
    }
  }
  
  if (this.isModified('isPublic') && this.isPublic && !this.publishedAt) {
    this.publishedAt = new Date();
  }
  
  next();
});

// Middleware post-save
ExperienceSchema.post('save', async function(doc) {
  // Mettre à jour le cache Redis si disponible
  try {
    const RedisService = await import('../services/RedisService.js');
    await RedisService.RedisService.invalidatePattern(`experience:${doc.id}:*`);
  } catch (error) {
    // Redis non disponible, continuer
  }
});

export const Experience = mongoose.model<IExperience>('Experience', ExperienceSchema);