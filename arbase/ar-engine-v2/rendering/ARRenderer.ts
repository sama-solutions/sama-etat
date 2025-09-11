/**
 * ARRenderer - Système de rendu AR optimisé
 * Gère le rendu WebGL avec Three.js et les optimisations mobiles
 */

import * as THREE from 'three';
import { EventEmitter } from '../utils/EventEmitter';

export interface ARRendererConfig {
  container: HTMLElement;
  canvas?: HTMLCanvasElement;
  antialias?: boolean;
  alpha?: boolean;
  preserveDrawingBuffer?: boolean;
  powerPreference?: 'default' | 'high-performance' | 'low-power';
  debug?: boolean;
}

export class ARRenderer extends EventEmitter {
  private config: ARRendererConfig;
  private renderer: THREE.WebGLRenderer;
  private container: HTMLElement;
  
  private isInitialized = false;
  private renderStats = {
    frameCount: 0,
    lastFrameTime: 0,
    fps: 0,
    drawCalls: 0,
    triangles: 0
  };

  constructor(config: ARRendererConfig) {
    super();
    this.config = {
      antialias: true,
      alpha: true,
      preserveDrawingBuffer: false,
      powerPreference: 'high-performance',
      debug: false,
      ...config
    };

    this.container = this.config.container;
  }

  async initialize(): Promise<void> {
    try {
      // Créer le renderer WebGL
      this.renderer = new THREE.WebGLRenderer({
        canvas: this.config.canvas,
        antialias: this.config.antialias,
        alpha: this.config.alpha,
        preserveDrawingBuffer: this.config.preserveDrawingBuffer,
        powerPreference: this.config.powerPreference
      });

      // Configuration du renderer
      this.setupRenderer();

      // Ajouter le canvas au container
      if (!this.config.canvas) {
        this.container.appendChild(this.renderer.domElement);
      }

      // Configurer la taille
      this.resize();

      this.isInitialized = true;
      this.emit('initialized');

      if (this.config.debug) {
        console.log('ARRenderer initialized');
        this.logRendererInfo();
      }
    } catch (error) {
      this.emit('error', error);
      throw error;
    }
  }

  private setupRenderer(): void {
    // Configuration de base
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1;

    // Optimisations pour mobile
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    this.renderer.shadowMap.autoUpdate = false;

    // Extensions WebGL
    const gl = this.renderer.getContext();
    const extensions = [
      'OES_vertex_array_object',
      'WEBGL_compressed_texture_s3tc',
      'WEBGL_compressed_texture_etc1',
      'WEBGL_compressed_texture_astc'
    ];

    extensions.forEach(ext => {
      const extension = gl.getExtension(ext);
      if (extension && this.config.debug) {
        console.log(`WebGL extension ${ext} supported`);
      }
    });

    // Configuration pour AR
    this.renderer.xr.enabled = true;
    this.renderer.autoClear = false;
  }

  render(scene: THREE.Scene, camera: THREE.Camera): void {
    if (!this.isInitialized) return;

    // Statistiques de rendu
    this.updateRenderStats();

    // Effacer le buffer
    this.renderer.clear();

    // Rendu de la scène
    this.renderer.render(scene, camera);

    // Debug overlay si activé
    if (this.config.debug) {
      this.renderDebugOverlay();
    }
  }

  resize(): void {
    if (!this.isInitialized) return;

    const width = this.container.clientWidth;
    const height = this.container.clientHeight;

    this.renderer.setSize(width, height);
    this.emit('resize', { width, height });

    if (this.config.debug) {
      console.log(`Renderer resized to ${width}x${height}`);
    }
  }

  private updateRenderStats(): void {
    const now = performance.now();
    this.renderStats.frameCount++;

    if (now - this.renderStats.lastFrameTime >= 1000) {
      this.renderStats.fps = this.renderStats.frameCount;
      this.renderStats.frameCount = 0;
      this.renderStats.lastFrameTime = now;

      // Statistiques WebGL
      const info = this.renderer.info;
      this.renderStats.drawCalls = info.render.calls;
      this.renderStats.triangles = info.render.triangles;

      this.emit('statsUpdate', { ...this.renderStats });
    }
  }

  private renderDebugOverlay(): void {
    // Créer un overlay 2D pour les informations de debug
    const canvas = this.renderer.domElement;
    const ctx = canvas.getContext('2d');
    
    if (!ctx) return;

    // Sauvegarder l'état du contexte
    ctx.save();

    // Configuration du texte
    ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
    ctx.fillRect(10, 10, 200, 100);
    
    ctx.fillStyle = '#00ff00';
    ctx.font = '12px monospace';
    
    // Afficher les statistiques
    const stats = [
      `FPS: ${this.renderStats.fps}`,
      `Draw Calls: ${this.renderStats.drawCalls}`,
      `Triangles: ${this.renderStats.triangles}`,
      `Memory: ${this.getMemoryUsage()}MB`
    ];

    stats.forEach((stat, index) => {
      ctx.fillText(stat, 15, 30 + index * 15);
    });

    // Restaurer l'état du contexte
    ctx.restore();
  }

  private getMemoryUsage(): number {
    const info = this.renderer.info;
    return Math.round(info.memory.geometries + info.memory.textures);
  }

  private logRendererInfo(): void {
    const gl = this.renderer.getContext();
    console.log('WebGL Renderer Info:', {
      vendor: gl.getParameter(gl.VENDOR),
      renderer: gl.getParameter(gl.RENDERER),
      version: gl.getParameter(gl.VERSION),
      shadingLanguageVersion: gl.getParameter(gl.SHADING_LANGUAGE_VERSION),
      maxTextureSize: gl.getParameter(gl.MAX_TEXTURE_SIZE),
      maxVertexAttribs: gl.getParameter(gl.MAX_VERTEX_ATTRIBS),
      maxVaryingVectors: gl.getParameter(gl.MAX_VARYING_VECTORS),
      maxFragmentUniforms: gl.getParameter(gl.MAX_FRAGMENT_UNIFORM_VECTORS),
      maxVertexUniforms: gl.getParameter(gl.MAX_VERTEX_UNIFORM_VECTORS)
    });
  }

  // Optimisations
  enableShadows(enable: boolean = true): void {
    this.renderer.shadowMap.enabled = enable;
    this.renderer.shadowMap.needsUpdate = true;
  }

  setPixelRatio(ratio: number): void {
    this.renderer.setPixelRatio(Math.min(ratio, 2));
  }

  setToneMapping(toneMapping: THREE.ToneMapping, exposure: number = 1): void {
    this.renderer.toneMapping = toneMapping;
    this.renderer.toneMappingExposure = exposure;
  }

  // Capture d'écran
  captureFrame(): string {
    return this.renderer.domElement.toDataURL('image/png');
  }

  // WebXR
  enableXR(): void {
    this.renderer.xr.enabled = true;
  }

  disableXR(): void {
    this.renderer.xr.enabled = false;
  }

  getXRManager(): THREE.WebXRManager {
    return this.renderer.xr;
  }

  // Getters
  getRenderer(): THREE.WebGLRenderer {
    return this.renderer;
  }

  getDomElement(): HTMLCanvasElement {
    return this.renderer.domElement;
  }

  getSize(): { width: number; height: number } {
    const size = new THREE.Vector2();
    this.renderer.getSize(size);
    return { width: size.x, height: size.y };
  }

  getPixelRatio(): number {
    return this.renderer.getPixelRatio();
  }

  getRenderStats(): typeof this.renderStats {
    return { ...this.renderStats };
  }

  isInitializedState(): boolean {
    return this.isInitialized;
  }

  // Nettoyage
  dispose(): void {
    if (this.renderer) {
      this.renderer.dispose();
      
      // Retirer le canvas du DOM si on l'a ajouté
      if (!this.config.canvas && this.renderer.domElement.parentNode) {
        this.renderer.domElement.parentNode.removeChild(this.renderer.domElement);
      }
    }

    this.emit('disposed');
  }
}