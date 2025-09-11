/**
 * QRTracker - Système de détection et tracking de QR codes
 * Utilise jsQR et OpenCV.js pour une détection robuste
 */

import jsQR from 'jsqr';
import * as THREE from 'three';
import { EventEmitter } from '../utils/EventEmitter';

export interface QRTrackerConfig {
  video?: HTMLVideoElement;
  canvas?: HTMLCanvasElement;
  scanInterval?: number;
  minConfidence?: number;
  maxDistance?: number;
  enablePoseEstimation?: boolean;
  debug?: boolean;
}

export interface QRDetection {
  data: string;
  location: {
    topLeftCorner: { x: number; y: number };
    topRightCorner: { x: number; y: number };
    bottomLeftCorner: { x: number; y: number };
    bottomRightCorner: { x: number; y: number };
  };
  confidence: number;
  timestamp: number;
  transform?: THREE.Matrix4;
  pose?: {
    position: THREE.Vector3;
    rotation: THREE.Euler;
    scale: THREE.Vector3;
  };
}

export class QRTracker extends EventEmitter {
  private config: QRTrackerConfig;
  private video: HTMLVideoElement;
  private canvas: HTMLCanvasElement;
  private context: CanvasRenderingContext2D;
  
  private isInitialized = false;
  private isRunning = false;
  private scanIntervalId: number | null = null;
  
  private lastDetection: QRDetection | null = null;
  private detectionHistory: QRDetection[] = [];
  private lostFrameCount = 0;
  private maxLostFrames = 10;

  // Calibration de la caméra (à ajuster selon l'appareil)
  private cameraMatrix = new THREE.Matrix3().set(
    800, 0, 320,
    0, 800, 240,
    0, 0, 1
  );

  constructor(config: QRTrackerConfig) {
    super();
    this.config = {
      scanInterval: 100,
      minConfidence: 0.8,
      maxDistance: 10,
      enablePoseEstimation: true,
      debug: false,
      ...config
    };

    this.setupCanvas();
  }

  private setupCanvas(): void {
    if (this.config.canvas) {
      this.canvas = this.config.canvas;
    } else {
      this.canvas = document.createElement('canvas');
      this.canvas.style.display = 'none';
      document.body.appendChild(this.canvas);
    }

    this.context = this.canvas.getContext('2d')!;
  }

  async initialize(): Promise<void> {
    try {
      if (this.config.video) {
        this.video = this.config.video;
      } else {
        throw new Error('Video element is required for QR tracking');
      }

      // Attendre que la vidéo soit prête
      await this.waitForVideoReady();

      // Configurer le canvas
      this.canvas.width = this.video.videoWidth;
      this.canvas.height = this.video.videoHeight;

      this.isInitialized = true;
      this.emit('initialized');

      if (this.config.debug) {
        console.log('QRTracker initialized');
      }
    } catch (error) {
      this.emit('error', error);
      throw error;
    }
  }

  private waitForVideoReady(): Promise<void> {
    return new Promise((resolve, reject) => {
      if (this.video.readyState >= 2) {
        resolve();
        return;
      }

      const onLoadedData = () => {
        this.video.removeEventListener('loadeddata', onLoadedData);
        resolve();
      };

      const onError = () => {
        this.video.removeEventListener('error', onError);
        reject(new Error('Video failed to load'));
      };

      this.video.addEventListener('loadeddata', onLoadedData);
      this.video.addEventListener('error', onError);
    });
  }

  start(): void {
    if (!this.isInitialized) {
      throw new Error('QRTracker must be initialized before starting');
    }

    if (this.isRunning) return;

    this.isRunning = true;
    this.startScanning();
    this.emit('started');

    if (this.config.debug) {
      console.log('QRTracker started');
    }
  }

  stop(): void {
    if (!this.isRunning) return;

    this.isRunning = false;
    this.stopScanning();
    this.emit('stopped');

    if (this.config.debug) {
      console.log('QRTracker stopped');
    }
  }

  private startScanning(): void {
    const scan = () => {
      if (!this.isRunning) return;

      this.scanFrame();
      this.scanIntervalId = window.setTimeout(scan, this.config.scanInterval);
    };

    scan();
  }

  private stopScanning(): void {
    if (this.scanIntervalId) {
      clearTimeout(this.scanIntervalId);
      this.scanIntervalId = null;
    }
  }

  private scanFrame(): void {
    try {
      // Capturer l'image de la vidéo
      this.context.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
      const imageData = this.context.getImageData(0, 0, this.canvas.width, this.canvas.height);

      // Détecter les QR codes
      const qrCode = jsQR(imageData.data, imageData.width, imageData.height, {
        inversionAttempts: 'dontInvert'
      });

      if (qrCode) {
        this.handleQRDetection(qrCode);
      } else {
        this.handleNoDetection();
      }
    } catch (error) {
      if (this.config.debug) {
        console.error('Error scanning frame:', error);
      }
    }
  }

  private handleQRDetection(qrCode: any): void {
    const detection: QRDetection = {
      data: qrCode.data,
      location: qrCode.location,
      confidence: this.calculateConfidence(qrCode),
      timestamp: Date.now()
    };

    // Vérifier la confiance minimale
    if (detection.confidence < this.config.minConfidence!) {
      this.handleNoDetection();
      return;
    }

    // Estimation de pose si activée
    if (this.config.enablePoseEstimation) {
      detection.pose = this.estimatePose(qrCode.location);
      detection.transform = this.createTransformMatrix(detection.pose);
    }

    // Filtrage et stabilisation
    const stabilizedDetection = this.stabilizeDetection(detection);

    // Vérifier si c'est une nouvelle détection ou une mise à jour
    if (!this.lastDetection || this.lastDetection.data !== detection.data) {
      this.emit('qrDetected', stabilizedDetection);
    } else {
      this.emit('qrUpdated', stabilizedDetection);
    }

    this.lastDetection = stabilizedDetection;
    this.lostFrameCount = 0;

    // Ajouter à l'historique
    this.detectionHistory.push(stabilizedDetection);
    if (this.detectionHistory.length > 10) {
      this.detectionHistory.shift();
    }

    if (this.config.debug) {
      this.drawDebugInfo(qrCode);
    }
  }

  private handleNoDetection(): void {
    this.lostFrameCount++;

    if (this.lastDetection && this.lostFrameCount >= this.maxLostFrames) {
      this.emit('qrLost', this.lastDetection);
      this.lastDetection = null;
      this.detectionHistory = [];
    }
  }

  private calculateConfidence(qrCode: any): number {
    // Calculer la confiance basée sur la taille et la qualité du QR code
    const location = qrCode.location;
    
    // Taille du QR code
    const width = Math.abs(location.topRightCorner.x - location.topLeftCorner.x);
    const height = Math.abs(location.bottomLeftCorner.y - location.topLeftCorner.y);
    const area = width * height;
    
    // Normaliser la taille (plus grand = plus confiant)
    const sizeConfidence = Math.min(area / 10000, 1);
    
    // Vérifier la régularité du quadrilatère
    const shapeConfidence = this.calculateShapeConfidence(location);
    
    return (sizeConfidence + shapeConfidence) / 2;
  }

  private calculateShapeConfidence(location: any): number {
    // Calculer si le QR code forme un quadrilatère régulier
    const corners = [
      location.topLeftCorner,
      location.topRightCorner,
      location.bottomRightCorner,
      location.bottomLeftCorner
    ];

    // Calculer les longueurs des côtés
    const sides = [];
    for (let i = 0; i < 4; i++) {
      const current = corners[i];
      const next = corners[(i + 1) % 4];
      const length = Math.sqrt(
        Math.pow(next.x - current.x, 2) + Math.pow(next.y - current.y, 2)
      );
      sides.push(length);
    }

    // Calculer la variance des longueurs (plus faible = plus régulier)
    const mean = sides.reduce((a, b) => a + b) / sides.length;
    const variance = sides.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / sides.length;
    
    return Math.max(0, 1 - variance / (mean * mean));
  }

  private estimatePose(location: any): {
    position: THREE.Vector3;
    rotation: THREE.Euler;
    scale: THREE.Vector3;
  } {
    // Points 2D du QR code détecté
    const imagePoints = [
      [location.topLeftCorner.x, location.topLeftCorner.y],
      [location.topRightCorner.x, location.topRightCorner.y],
      [location.bottomRightCorner.x, location.bottomRightCorner.y],
      [location.bottomLeftCorner.x, location.bottomLeftCorner.y]
    ];

    // Points 3D du QR code dans l'espace monde (carré de 1x1)
    const worldPoints = [
      [-0.5, 0.5, 0],
      [0.5, 0.5, 0],
      [0.5, -0.5, 0],
      [-0.5, -0.5, 0]
    ];

    // Estimation de pose simplifiée (PnP solver basique)
    const pose = this.solvePnP(worldPoints, imagePoints);

    return pose;
  }

  private solvePnP(worldPoints: number[][], imagePoints: number[][]): {
    position: THREE.Vector3;
    rotation: THREE.Euler;
    scale: THREE.Vector3;
  } {
    // Implémentation simplifiée du PnP solver
    // Dans une version complète, on utiliserait OpenCV.js
    
    // Calculer la position approximative
    const centerX = imagePoints.reduce((sum, p) => sum + p[0], 0) / 4;
    const centerY = imagePoints.reduce((sum, p) => sum + p[1], 0) / 4;
    
    // Convertir les coordonnées écran en coordonnées monde
    const normalizedX = (centerX - this.canvas.width / 2) / (this.canvas.width / 2);
    const normalizedY = -(centerY - this.canvas.height / 2) / (this.canvas.height / 2);
    
    // Estimer la distance basée sur la taille du QR code
    const qrSize = Math.abs(imagePoints[1][0] - imagePoints[0][0]);
    const distance = Math.max(1, 500 / qrSize); // Formule empirique
    
    const position = new THREE.Vector3(
      normalizedX * distance * 0.5,
      normalizedY * distance * 0.5,
      -distance
    );

    // Estimer la rotation basée sur l'orientation du QR code
    const dx = imagePoints[1][0] - imagePoints[0][0];
    const dy = imagePoints[1][1] - imagePoints[0][1];
    const angle = Math.atan2(dy, dx);
    
    const rotation = new THREE.Euler(0, 0, -angle);
    
    // Estimer l'échelle basée sur la taille
    const scale = new THREE.Vector3(1, 1, 1);
    
    return { position, rotation, scale };
  }

  private createTransformMatrix(pose: {
    position: THREE.Vector3;
    rotation: THREE.Euler;
    scale: THREE.Vector3;
  }): THREE.Matrix4 {
    const matrix = new THREE.Matrix4();
    matrix.compose(pose.position, new THREE.Quaternion().setFromEuler(pose.rotation), pose.scale);
    return matrix;
  }

  private stabilizeDetection(detection: QRDetection): QRDetection {
    if (this.detectionHistory.length === 0) {
      return detection;
    }

    // Moyenner les dernières détections pour stabiliser
    const recentDetections = this.detectionHistory.slice(-3);
    
    if (detection.pose && recentDetections.every(d => d.pose)) {
      // Moyenner les positions
      const avgPosition = new THREE.Vector3();
      const avgRotation = new THREE.Euler();
      
      recentDetections.forEach(d => {
        avgPosition.add(d.pose!.position);
        avgRotation.x += d.pose!.rotation.x;
        avgRotation.y += d.pose!.rotation.y;
        avgRotation.z += d.pose!.rotation.z;
      });
      
      avgPosition.divideScalar(recentDetections.length);
      avgRotation.x /= recentDetections.length;
      avgRotation.y /= recentDetections.length;
      avgRotation.z /= recentDetections.length;
      
      // Interpoler avec la nouvelle détection
      const alpha = 0.7; // Facteur de lissage
      detection.pose.position.lerp(avgPosition, alpha);
      detection.pose.rotation.x = detection.pose.rotation.x * (1 - alpha) + avgRotation.x * alpha;
      detection.pose.rotation.y = detection.pose.rotation.y * (1 - alpha) + avgRotation.y * alpha;
      detection.pose.rotation.z = detection.pose.rotation.z * (1 - alpha) + avgRotation.z * alpha;
      
      // Recalculer la matrice de transformation
      detection.transform = this.createTransformMatrix(detection.pose);
    }

    return detection;
  }

  private drawDebugInfo(qrCode: any): void {
    const location = qrCode.location;
    
    // Dessiner le contour du QR code
    this.context.strokeStyle = '#00ff00';
    this.context.lineWidth = 2;
    this.context.beginPath();
    this.context.moveTo(location.topLeftCorner.x, location.topLeftCorner.y);
    this.context.lineTo(location.topRightCorner.x, location.topRightCorner.y);
    this.context.lineTo(location.bottomRightCorner.x, location.bottomRightCorner.y);
    this.context.lineTo(location.bottomLeftCorner.x, location.bottomLeftCorner.y);
    this.context.closePath();
    this.context.stroke();

    // Afficher les données du QR code
    this.context.fillStyle = '#00ff00';
    this.context.font = '16px Arial';
    this.context.fillText(
      qrCode.data.substring(0, 20) + (qrCode.data.length > 20 ? '...' : ''),
      location.topLeftCorner.x,
      location.topLeftCorner.y - 10
    );
  }

  // Getters
  getLastDetection(): QRDetection | null {
    return this.lastDetection;
  }

  getDetectionHistory(): QRDetection[] {
    return [...this.detectionHistory];
  }

  isInitializedState(): boolean {
    return this.isInitialized;
  }

  isRunningState(): boolean {
    return this.isRunning;
  }

  // Nettoyage
  dispose(): void {
    this.stop();
    
    if (this.canvas && !this.config.canvas) {
      document.body.removeChild(this.canvas);
    }

    this.emit('disposed');
  }
}