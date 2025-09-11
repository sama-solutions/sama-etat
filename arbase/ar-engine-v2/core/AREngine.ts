/**
 * AREngine - Moteur de réalité augmentée moderne
 * Support WebXR, AR.js et QR codes comme markers
 */

import * as THREE from 'three';
import { QRTracker } from '../qr-tracking/QRTracker';
import { ARRenderer } from '../rendering/ARRenderer';
import { ARScene } from '../rendering/ARScene';
import { ARCamera } from '../rendering/ARCamera';
import { EventEmitter } from '../utils/EventEmitter';

export interface AREngineConfig {
  container: HTMLElement;
  video?: HTMLVideoElement;
  canvas?: HTMLCanvasElement;
  debug?: boolean;
  enableWebXR?: boolean;
  enableQRTracking?: boolean;
  qrTrackingConfig?: {
    scanInterval?: number;
    minConfidence?: number;
    maxDistance?: number;
  };
}

export interface ARExperience {
  id: string;
  qrCode: string;
  content: ARContent[];
  settings: ARSettings;
}

export interface ARContent {
  type: 'model' | 'text' | 'image' | 'video' | 'html';
  data: any;
  position: THREE.Vector3;
  rotation: THREE.Euler;
  scale: THREE.Vector3;
  animations?: ARAnimation[];
  interactions?: ARInteraction[];
}

export interface ARSettings {
  autoStart: boolean;
  trackingMode: 'qr' | 'marker' | 'markerless';
  renderDistance: number;
  occlusionCulling: boolean;
}

export interface ARAnimation {
  type: 'rotation' | 'scale' | 'position' | 'opacity';
  duration: number;
  loop: boolean;
  easing: string;
  keyframes: any[];
}

export interface ARInteraction {
  type: 'click' | 'hover' | 'gaze';
  action: 'url' | 'animation' | 'sound' | 'custom';
  data: any;
}

export class AREngine extends EventEmitter {
  private config: AREngineConfig;
  private renderer: ARRenderer;
  private scene: ARScene;
  private camera: ARCamera;
  private qrTracker: QRTracker;
  
  private isInitialized = false;
  private isRunning = false;
  private currentExperience: ARExperience | null = null;
  
  private animationFrameId: number | null = null;
  private lastFrameTime = 0;
  private frameCount = 0;
  private fps = 0;

  constructor(config: AREngineConfig) {
    super();
    this.config = {
      debug: false,
      enableWebXR: true,
      enableQRTracking: true,
      qrTrackingConfig: {
        scanInterval: 100,
        minConfidence: 0.8,
        maxDistance: 10
      },
      ...config
    };

    this.validateConfig();
    this.initializeComponents();
  }

  private validateConfig(): void {
    if (!this.config.container) {
      throw new Error('Container element is required');
    }
  }

  private initializeComponents(): void {
    // Initialiser le renderer
    this.renderer = new ARRenderer({
      container: this.config.container,
      canvas: this.config.canvas,
      debug: this.config.debug
    });

    // Initialiser la scène
    this.scene = new ARScene();

    // Initialiser la caméra
    this.camera = new ARCamera({
      video: this.config.video,
      enableWebXR: this.config.enableWebXR
    });

    // Initialiser le tracker QR
    if (this.config.enableQRTracking) {
      this.qrTracker = new QRTracker({
        video: this.config.video,
        ...this.config.qrTrackingConfig
      });

      this.qrTracker.on('qrDetected', this.handleQRDetected.bind(this));
      this.qrTracker.on('qrLost', this.handleQRLost.bind(this));
    }
  }

  async initialize(): Promise<void> {
    try {
      this.emit('initializing');

      // Initialiser les composants
      await this.camera.initialize();
      await this.renderer.initialize();
      
      if (this.qrTracker) {
        await this.qrTracker.initialize();
      }

      // Configurer les événements
      this.setupEventListeners();

      this.isInitialized = true;
      this.emit('initialized');

      if (this.config.debug) {
        console.log('AREngine initialized successfully');
      }
    } catch (error) {
      this.emit('error', error);
      throw error;
    }
  }

  async start(): Promise<void> {
    if (!this.isInitialized) {
      await this.initialize();
    }

    try {
      this.emit('starting');

      // Démarrer la caméra
      await this.camera.start();

      // Démarrer le tracker QR
      if (this.qrTracker) {
        await this.qrTracker.start();
      }

      // Démarrer la boucle de rendu
      this.startRenderLoop();

      this.isRunning = true;
      this.emit('started');

      if (this.config.debug) {
        console.log('AREngine started successfully');
      }
    } catch (error) {
      this.emit('error', error);
      throw error;
    }
  }

  stop(): void {
    if (!this.isRunning) return;

    this.emit('stopping');

    // Arrêter la boucle de rendu
    this.stopRenderLoop();

    // Arrêter les composants
    this.camera.stop();
    
    if (this.qrTracker) {
      this.qrTracker.stop();
    }

    this.isRunning = false;
    this.emit('stopped');

    if (this.config.debug) {
      console.log('AREngine stopped');
    }
  }

  loadExperience(experience: ARExperience): void {
    this.currentExperience = experience;
    this.scene.clear();
    
    // Charger le contenu de l'expérience
    experience.content.forEach(content => {
      this.scene.addContent(content);
    });

    this.emit('experienceLoaded', experience);
  }

  private startRenderLoop(): void {
    const render = (timestamp: number) => {
      if (!this.isRunning) return;

      // Calculer FPS
      this.calculateFPS(timestamp);

      // Mettre à jour la scène
      this.scene.update(timestamp);

      // Rendu
      this.renderer.render(this.scene.getScene(), this.camera.getCamera());

      // Continuer la boucle
      this.animationFrameId = requestAnimationFrame(render);
    };

    this.animationFrameId = requestAnimationFrame(render);
  }

  private stopRenderLoop(): void {
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }
  }

  private calculateFPS(timestamp: number): void {
    this.frameCount++;
    
    if (timestamp - this.lastFrameTime >= 1000) {
      this.fps = this.frameCount;
      this.frameCount = 0;
      this.lastFrameTime = timestamp;
      
      if (this.config.debug) {
        this.emit('fpsUpdate', this.fps);
      }
    }
  }

  private handleQRDetected(qrData: any): void {
    if (this.config.debug) {
      console.log('QR Code detected:', qrData);
    }

    // Vérifier si on a une expérience pour ce QR code
    if (this.currentExperience && this.currentExperience.qrCode === qrData.data) {
      this.scene.setVisible(true);
      this.scene.updateTracking(qrData.transform);
      this.emit('trackingStarted', qrData);
    } else {
      // Charger l'expérience correspondante
      this.emit('qrCodeDetected', qrData);
    }
  }

  private handleQRLost(): void {
    if (this.config.debug) {
      console.log('QR Code tracking lost');
    }

    this.scene.setVisible(false);
    this.emit('trackingLost');
  }

  private setupEventListeners(): void {
    // Gestion du redimensionnement
    window.addEventListener('resize', this.handleResize.bind(this));

    // Gestion de la visibilité de la page
    document.addEventListener('visibilitychange', this.handleVisibilityChange.bind(this));
  }

  private handleResize(): void {
    this.camera.updateAspectRatio();
    this.renderer.resize();
  }

  private handleVisibilityChange(): void {
    if (document.hidden) {
      this.pause();
    } else {
      this.resume();
    }
  }

  pause(): void {
    if (this.isRunning) {
      this.stopRenderLoop();
      this.emit('paused');
    }
  }

  resume(): void {
    if (this.isRunning) {
      this.startRenderLoop();
      this.emit('resumed');
    }
  }

  // Getters
  getRenderer(): ARRenderer {
    return this.renderer;
  }

  getScene(): ARScene {
    return this.scene;
  }

  getCamera(): ARCamera {
    return this.camera;
  }

  getQRTracker(): QRTracker | null {
    return this.qrTracker;
  }

  getFPS(): number {
    return this.fps;
  }

  isInitializedState(): boolean {
    return this.isInitialized;
  }

  isRunningState(): boolean {
    return this.isRunning;
  }

  getCurrentExperience(): ARExperience | null {
    return this.currentExperience;
  }

  // Nettoyage
  dispose(): void {
    this.stop();
    
    this.renderer.dispose();
    this.scene.dispose();
    this.camera.dispose();
    
    if (this.qrTracker) {
      this.qrTracker.dispose();
    }

    window.removeEventListener('resize', this.handleResize.bind(this));
    document.removeEventListener('visibilitychange', this.handleVisibilityChange.bind(this));

    this.emit('disposed');
  }
}