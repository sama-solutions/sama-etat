/**
 * ARCamera - Gestion de la caméra AR avec support WebXR
 * Gère la caméra de l'appareil et la caméra virtuelle 3D
 */

import * as THREE from 'three';
import { EventEmitter } from '../utils/EventEmitter';

export interface ARCameraConfig {
  video?: HTMLVideoElement;
  enableWebXR?: boolean;
  fov?: number;
  near?: number;
  far?: number;
  facingMode?: 'user' | 'environment';
  resolution?: {
    width: number;
    height: number;
  };
}

export class ARCamera extends EventEmitter {
  private config: ARCameraConfig;
  private camera: THREE.PerspectiveCamera;
  private video: HTMLVideoElement;
  private stream: MediaStream | null = null;
  
  private isInitialized = false;
  private isStarted = false;
  
  // Calibration de la caméra
  private intrinsics = {
    fx: 800, // Focal length X
    fy: 800, // Focal length Y
    cx: 320, // Principal point X
    cy: 240, // Principal point Y
    k1: 0,   // Distortion coefficient
    k2: 0,
    p1: 0,
    p2: 0
  };

  constructor(config: ARCameraConfig) {
    super();
    this.config = {
      fov: 75,
      near: 0.1,
      far: 1000,
      facingMode: 'environment',
      enableWebXR: true,
      ...config
    };

    this.setupCamera();
    this.setupVideo();
  }

  private setupCamera(): void {
    this.camera = new THREE.PerspectiveCamera(
      this.config.fov!,
      window.innerWidth / window.innerHeight,
      this.config.near!,
      this.config.far!
    );

    // Position initiale de la caméra
    this.camera.position.set(0, 0, 0);
    this.camera.lookAt(0, 0, -1);
  }

  private setupVideo(): void {
    if (this.config.video) {
      this.video = this.config.video;
    } else {
      this.video = document.createElement('video');
      this.video.setAttribute('playsinline', '');
      this.video.setAttribute('webkit-playsinline', '');
      this.video.muted = true;
      this.video.style.display = 'none';
      document.body.appendChild(this.video);
    }
  }

  async initialize(): Promise<void> {
    try {
      this.emit('initializing');

      // Initialiser WebXR si supporté et activé
      if (this.config.enableWebXR && this.isWebXRSupported()) {
        await this.initializeWebXR();
      }

      this.isInitialized = true;
      this.emit('initialized');
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

      // Démarrer le flux vidéo de la caméra
      await this.startVideoStream();

      // Calibrer la caméra avec les dimensions vidéo
      this.calibrateCamera();

      this.isStarted = true;
      this.emit('started');
    } catch (error) {
      this.emit('error', error);
      throw error;
    }
  }

  private async startVideoStream(): Promise<void> {
    const constraints: MediaStreamConstraints = {
      video: {
        facingMode: this.config.facingMode,
        width: this.config.resolution?.width || { ideal: 1280 },
        height: this.config.resolution?.height || { ideal: 720 },
        frameRate: { ideal: 30 }
      },
      audio: false
    };

    try {
      this.stream = await navigator.mediaDevices.getUserMedia(constraints);
      this.video.srcObject = this.stream;
      
      return new Promise((resolve, reject) => {
        this.video.onloadedmetadata = () => {
          this.video.play()
            .then(() => {
              this.emit('videoStarted', {
                width: this.video.videoWidth,
                height: this.video.videoHeight
              });
              resolve();
            })
            .catch(reject);
        };
        
        this.video.onerror = () => {
          reject(new Error('Failed to start video'));
        };
      });
    } catch (error) {
      throw new Error(`Failed to access camera: ${error.message}`);
    }
  }

  private calibrateCamera(): void {
    if (!this.video.videoWidth || !this.video.videoHeight) {
      return;
    }

    const videoAspect = this.video.videoWidth / this.video.videoHeight;
    const windowAspect = window.innerWidth / window.innerHeight;

    // Ajuster le FOV basé sur les dimensions de la vidéo
    const fovY = this.config.fov!;
    const fovX = 2 * Math.atan(Math.tan(fovY * Math.PI / 360) * videoAspect) * 180 / Math.PI;

    // Mettre à jour les intrinsèques de la caméra
    this.intrinsics.fx = (this.video.videoWidth / 2) / Math.tan(fovX * Math.PI / 360);
    this.intrinsics.fy = (this.video.videoHeight / 2) / Math.tan(fovY * Math.PI / 360);
    this.intrinsics.cx = this.video.videoWidth / 2;
    this.intrinsics.cy = this.video.videoHeight / 2;

    // Créer la matrice de projection personnalisée
    this.updateProjectionMatrix();

    this.emit('calibrated', this.intrinsics);
  }

  private updateProjectionMatrix(): void {
    const w = this.video.videoWidth;
    const h = this.video.videoHeight;
    const near = this.config.near!;
    const far = this.config.far!;

    // Matrice de projection basée sur les intrinsèques de la caméra
    const fx = this.intrinsics.fx;
    const fy = this.intrinsics.fy;
    const cx = this.intrinsics.cx;
    const cy = this.intrinsics.cy;

    const projectionMatrix = new THREE.Matrix4();
    projectionMatrix.set(
      2 * fx / w, 0, (w - 2 * cx) / w, 0,
      0, 2 * fy / h, (2 * cy - h) / h, 0,
      0, 0, -(far + near) / (far - near), -2 * far * near / (far - near),
      0, 0, -1, 0
    );

    this.camera.projectionMatrix.copy(projectionMatrix);
    this.camera.projectionMatrixInverse.copy(projectionMatrix).invert();
  }

  stop(): void {
    if (!this.isStarted) return;

    this.emit('stopping');

    // Arrêter le flux vidéo
    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop());
      this.stream = null;
    }

    this.video.srcObject = null;

    this.isStarted = false;
    this.emit('stopped');
  }

  // WebXR Support
  private isWebXRSupported(): boolean {
    return 'xr' in navigator;
  }

  private async initializeWebXR(): Promise<void> {
    if (!('xr' in navigator)) {
      throw new Error('WebXR not supported');
    }

    try {
      const isSupported = await (navigator as any).xr.isSessionSupported('immersive-ar');
      if (isSupported) {
        this.emit('webxrSupported');
      } else {
        console.warn('Immersive AR not supported, falling back to camera');
      }
    } catch (error) {
      console.warn('WebXR check failed:', error);
    }
  }

  async startWebXRSession(): Promise<void> {
    if (!this.isWebXRSupported()) {
      throw new Error('WebXR not supported');
    }

    try {
      const session = await (navigator as any).xr.requestSession('immersive-ar', {
        requiredFeatures: ['local', 'hit-test'],
        optionalFeatures: ['dom-overlay', 'light-estimation']
      });

      this.emit('webxrSessionStarted', session);
      return session;
    } catch (error) {
      throw new Error(`Failed to start WebXR session: ${error.message}`);
    }
  }

  // Gestion des événements de redimensionnement
  updateAspectRatio(): void {
    if (!this.camera) return;

    const aspect = window.innerWidth / window.innerHeight;
    this.camera.aspect = aspect;
    this.camera.updateProjectionMatrix();

    this.emit('aspectRatioUpdated', aspect);
  }

  // Conversion de coordonnées
  screenToWorld(screenX: number, screenY: number, depth: number = 1): THREE.Vector3 {
    const vector = new THREE.Vector3();
    
    // Normaliser les coordonnées écran
    vector.x = (screenX / window.innerWidth) * 2 - 1;
    vector.y = -(screenY / window.innerHeight) * 2 + 1;
    vector.z = depth;

    // Projeter dans l'espace monde
    vector.unproject(this.camera);
    
    return vector;
  }

  worldToScreen(worldPosition: THREE.Vector3): THREE.Vector2 {
    const vector = worldPosition.clone();
    vector.project(this.camera);

    // Convertir en coordonnées écran
    const x = (vector.x + 1) * window.innerWidth / 2;
    const y = -(vector.y - 1) * window.innerHeight / 2;

    return new THREE.Vector2(x, y);
  }

  // Raycasting depuis la caméra
  getRayFromCamera(x: number, y: number): THREE.Ray {
    const mouse = new THREE.Vector2();
    mouse.x = (x / window.innerWidth) * 2 - 1;
    mouse.y = -(y / window.innerHeight) * 2 + 1;

    const raycaster = new THREE.Raycaster();
    raycaster.setFromCamera(mouse, this.camera);

    return raycaster.ray;
  }

  // Gestion de la pose de la caméra
  setPose(position: THREE.Vector3, rotation: THREE.Euler): void {
    this.camera.position.copy(position);
    this.camera.rotation.copy(rotation);
    this.camera.updateMatrixWorld();

    this.emit('poseUpdated', { position, rotation });
  }

  getPose(): { position: THREE.Vector3; rotation: THREE.Euler } {
    return {
      position: this.camera.position.clone(),
      rotation: this.camera.rotation.clone()
    };
  }

  // Contrôles de la caméra
  lookAt(target: THREE.Vector3): void {
    this.camera.lookAt(target);
    this.emit('lookAtChanged', target);
  }

  setFOV(fov: number): void {
    this.camera.fov = fov;
    this.camera.updateProjectionMatrix();
    this.emit('fovChanged', fov);
  }

  setClippingPlanes(near: number, far: number): void {
    this.camera.near = near;
    this.camera.far = far;
    this.camera.updateProjectionMatrix();
    this.emit('clippingPlanesChanged', { near, far });
  }

  // Capture d'image depuis la caméra
  captureFrame(): string | null {
    if (!this.video.videoWidth || !this.video.videoHeight) {
      return null;
    }

    const canvas = document.createElement('canvas');
    canvas.width = this.video.videoWidth;
    canvas.height = this.video.videoHeight;
    
    const context = canvas.getContext('2d')!;
    context.drawImage(this.video, 0, 0);
    
    return canvas.toDataURL('image/jpeg', 0.8);
  }

  // Getters
  getCamera(): THREE.PerspectiveCamera {
    return this.camera;
  }

  getVideo(): HTMLVideoElement {
    return this.video;
  }

  getStream(): MediaStream | null {
    return this.stream;
  }

  getIntrinsics(): typeof this.intrinsics {
    return { ...this.intrinsics };
  }

  isInitializedState(): boolean {
    return this.isInitialized;
  }

  isStartedState(): boolean {
    return this.isStarted;
  }

  getVideoResolution(): { width: number; height: number } | null {
    if (!this.video.videoWidth || !this.video.videoHeight) {
      return null;
    }
    
    return {
      width: this.video.videoWidth,
      height: this.video.videoHeight
    };
  }

  // Nettoyage
  dispose(): void {
    this.stop();
    
    // Nettoyer la vidéo si on l'a créée
    if (!this.config.video && this.video.parentNode) {
      this.video.parentNode.removeChild(this.video);
    }

    this.emit('disposed');
  }
}