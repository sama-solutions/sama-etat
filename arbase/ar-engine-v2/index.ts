/**
 * ARBase Engine v2 - Moteur de réalité augmentée moderne
 * Export principal de tous les composants
 */

// Core Engine
export { AREngine } from './core/AREngine';
export type { 
  AREngineConfig, 
  ARExperience, 
  ARContent, 
  ARSettings, 
  ARAnimation, 
  ARInteraction 
} from './core/AREngine';

// QR Tracking
export { QRTracker } from './qr-tracking/QRTracker';
export type { 
  QRTrackerConfig, 
  QRDetection 
} from './qr-tracking/QRTracker';

// Rendering
export { ARRenderer } from './rendering/ARRenderer';
export type { ARRendererConfig } from './rendering/ARRenderer';

export { ARScene } from './rendering/ARScene';
export { ARCamera } from './rendering/ARCamera';
export type { ARCameraConfig } from './rendering/ARCamera';

// Utils
export { EventEmitter } from './utils/EventEmitter';
export type { EventListener } from './utils/EventEmitter';
export { MathUtils } from './utils/MathUtils';

// Version
export const VERSION = '2.0.0';

// Factory function pour créer une instance complète
export function createAREngine(config: AREngineConfig) {
  return new AREngine(config);
}

// Utilitaires de détection de support
export const ARSupport = {
  /**
   * Vérifie si WebXR est supporté
   */
  isWebXRSupported(): boolean {
    return 'xr' in navigator;
  },

  /**
   * Vérifie si la caméra est accessible
   */
  async isCameraSupported(): Promise<boolean> {
    try {
      const devices = await navigator.mediaDevices.enumerateDevices();
      return devices.some(device => device.kind === 'videoinput');
    } catch {
      return false;
    }
  },

  /**
   * Vérifie si WebGL est supporté
   */
  isWebGLSupported(): boolean {
    try {
      const canvas = document.createElement('canvas');
      const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
      return !!gl;
    } catch {
      return false;
    }
  },

  /**
   * Vérifie si les Web Workers sont supportés
   */
  isWebWorkerSupported(): boolean {
    return typeof Worker !== 'undefined';
  },

  /**
   * Vérifie le support complet de l'AR
   */
  async checkFullSupport(): Promise<{
    webxr: boolean;
    camera: boolean;
    webgl: boolean;
    webworker: boolean;
    overall: boolean;
  }> {
    const webxr = this.isWebXRSupported();
    const camera = await this.isCameraSupported();
    const webgl = this.isWebGLSupported();
    const webworker = this.isWebWorkerSupported();
    
    const overall = camera && webgl; // WebXR et WebWorker sont optionnels
    
    return { webxr, camera, webgl, webworker, overall };
  }
};

// Configuration par défaut
export const DEFAULT_CONFIG: Partial<AREngineConfig> = {
  debug: false,
  enableWebXR: true,
  enableQRTracking: true,
  qrTrackingConfig: {
    scanInterval: 100,
    minConfidence: 0.8,
    maxDistance: 10
  }
};

// Types d'expériences prédéfinies
export const ExperienceTemplates = {
  /**
   * Template pour une carte de visite AR
   */
  businessCard: (qrCode: string, data: any): ARExperience => ({
    id: `business_card_${Date.now()}`,
    qrCode,
    content: [
      {
        type: 'text',
        data: {
          text: data.name || 'John Doe',
          fontSize: 32,
          color: '#ffffff'
        },
        position: { x: 0, y: 0.5, z: 0 },
        rotation: { x: 0, y: 0, z: 0 },
        scale: { x: 1, y: 1, z: 1 },
        animations: [{
          type: 'scale',
          duration: 1,
          loop: false,
          easing: 'easeOut',
          keyframes: [1.2, 1]
        }]
      },
      {
        type: 'text',
        data: {
          text: data.title || 'CEO',
          fontSize: 24,
          color: '#cccccc'
        },
        position: { x: 0, y: 0.2, z: 0 },
        rotation: { x: 0, y: 0, z: 0 },
        scale: { x: 1, y: 1, z: 1 }
      }
    ],
    settings: {
      autoStart: true,
      trackingMode: 'qr',
      renderDistance: 5,
      occlusionCulling: false
    }
  }),

  /**
   * Template pour un produit 3D
   */
  product3D: (qrCode: string, data: any): ARExperience => ({
    id: `product_3d_${Date.now()}`,
    qrCode,
    content: [
      {
        type: 'model',
        data: {
          url: data.modelUrl,
          autoPlay: true
        },
        position: { x: 0, y: 0, z: 0 },
        rotation: { x: 0, y: 0, z: 0 },
        scale: { x: 1, y: 1, z: 1 },
        animations: [{
          type: 'rotation',
          duration: 5,
          loop: true,
          easing: 'linear',
          keyframes: [0, Math.PI * 2]
        }],
        interactions: [{
          type: 'click',
          action: 'url',
          data: { url: data.productUrl }
        }]
      }
    ],
    settings: {
      autoStart: true,
      trackingMode: 'qr',
      renderDistance: 10,
      occlusionCulling: true
    }
  }),

  /**
   * Template pour une galerie d'images
   */
  imageGallery: (qrCode: string, data: any): ARExperience => ({
    id: `gallery_${Date.now()}`,
    qrCode,
    content: data.images.map((imageUrl: string, index: number) => ({
      type: 'image',
      data: { url: imageUrl },
      position: { 
        x: (index - data.images.length / 2) * 0.3, 
        y: 0, 
        z: 0 
      },
      rotation: { x: 0, y: 0, z: 0 },
      scale: { x: 0.5, y: 0.5, z: 1 },
      animations: [{
        type: 'position',
        duration: 2,
        loop: false,
        easing: 'easeOut',
        keyframes: [
          { x: 0, y: -1, z: 0 },
          { x: (index - data.images.length / 2) * 0.3, y: 0, z: 0 }
        ]
      }]
    })),
    settings: {
      autoStart: true,
      trackingMode: 'qr',
      renderDistance: 8,
      occlusionCulling: false
    }
  })
};