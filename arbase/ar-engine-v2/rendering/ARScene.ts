/**
 * ARScene - Gestion de la scène AR avec contenu dynamique
 * Gère les objets 3D, animations et interactions
 */

import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';
import { EventEmitter } from '../utils/EventEmitter';
import { ARContent, ARAnimation, ARInteraction } from '../core/AREngine';

export class ARScene extends EventEmitter {
  private scene: THREE.Scene;
  private arGroup: THREE.Group;
  private contentObjects: Map<string, THREE.Object3D> = new Map();
  private animations: Map<string, THREE.AnimationMixer> = new Map();
  private interactions: Map<string, ARInteraction[]> = new Map();
  
  private gltfLoader: GLTFLoader;
  private textureLoader: THREE.TextureLoader;
  private raycaster: THREE.Raycaster;
  private mouse: THREE.Vector2;
  
  private isVisible = false;
  private clock: THREE.Clock;

  constructor() {
    super();
    this.setupScene();
    this.setupLoaders();
    this.setupInteractions();
    this.clock = new THREE.Clock();
  }

  private setupScene(): void {
    this.scene = new THREE.Scene();
    
    // Groupe principal pour le contenu AR
    this.arGroup = new THREE.Group();
    this.arGroup.visible = false;
    this.scene.add(this.arGroup);

    // Éclairage de base
    this.setupLighting();
  }

  private setupLighting(): void {
    // Lumière ambiante
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    this.scene.add(ambientLight);

    // Lumière directionnelle
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(1, 1, 1);
    directionalLight.castShadow = true;
    directionalLight.shadow.mapSize.setScalar(1024);
    directionalLight.shadow.camera.near = 0.1;
    directionalLight.shadow.camera.far = 10;
    directionalLight.shadow.camera.left = -2;
    directionalLight.shadow.camera.right = 2;
    directionalLight.shadow.camera.top = 2;
    directionalLight.shadow.camera.bottom = -2;
    this.scene.add(directionalLight);

    // Lumière hémisphérique pour un éclairage plus naturel
    const hemisphereLight = new THREE.HemisphereLight(0x87ceeb, 0x8b4513, 0.3);
    this.scene.add(hemisphereLight);
  }

  private setupLoaders(): void {
    // Loader GLTF avec compression DRACO
    this.gltfLoader = new GLTFLoader();
    const dracoLoader = new DRACOLoader();
    dracoLoader.setDecoderPath('/draco/');
    this.gltfLoader.setDRACOLoader(dracoLoader);

    // Loader de textures
    this.textureLoader = new THREE.TextureLoader();
  }

  private setupInteractions(): void {
    this.raycaster = new THREE.Raycaster();
    this.mouse = new THREE.Vector2();
  }

  async addContent(content: ARContent): Promise<void> {
    try {
      let object: THREE.Object3D;

      switch (content.type) {
        case 'model':
          object = await this.loadModel(content);
          break;
        case 'text':
          object = this.createText(content);
          break;
        case 'image':
          object = await this.createImage(content);
          break;
        case 'video':
          object = await this.createVideo(content);
          break;
        case 'html':
          object = this.createHTML(content);
          break;
        default:
          throw new Error(`Unsupported content type: ${content.type}`);
      }

      // Appliquer la transformation
      object.position.copy(content.position);
      object.rotation.copy(content.rotation);
      object.scale.copy(content.scale);

      // Générer un ID unique si pas fourni
      const id = content.data.id || this.generateId();
      object.userData.contentId = id;

      // Ajouter à la scène
      this.arGroup.add(object);
      this.contentObjects.set(id, object);

      // Configurer les animations
      if (content.animations) {
        this.setupAnimations(object, content.animations, id);
      }

      // Configurer les interactions
      if (content.interactions) {
        this.interactions.set(id, content.interactions);
        this.setupObjectInteractions(object);
      }

      this.emit('contentAdded', { id, object, content });
    } catch (error) {
      this.emit('error', error);
      throw error;
    }
  }

  private async loadModel(content: ARContent): Promise<THREE.Object3D> {
    return new Promise((resolve, reject) => {
      this.gltfLoader.load(
        content.data.url,
        (gltf) => {
          const model = gltf.scene;
          
          // Optimisations pour mobile
          model.traverse((child) => {
            if (child instanceof THREE.Mesh) {
              child.castShadow = true;
              child.receiveShadow = true;
              
              // Optimiser les matériaux
              if (child.material) {
                this.optimizeMaterial(child.material);
              }
            }
          });

          // Animations du modèle
          if (gltf.animations && gltf.animations.length > 0) {
            const mixer = new THREE.AnimationMixer(model);
            gltf.animations.forEach(clip => {
              const action = mixer.clipAction(clip);
              if (content.data.autoPlay !== false) {
                action.play();
              }
            });
            this.animations.set(content.data.id || this.generateId(), mixer);
          }

          resolve(model);
        },
        (progress) => {
          this.emit('loadProgress', {
            type: 'model',
            loaded: progress.loaded,
            total: progress.total
          });
        },
        (error) => {
          reject(error);
        }
      );
    });
  }

  private createText(content: ARContent): THREE.Object3D {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d')!;
    
    // Configuration du canvas
    const fontSize = content.data.fontSize || 64;
    const fontFamily = content.data.fontFamily || 'Arial';
    const color = content.data.color || '#ffffff';
    const backgroundColor = content.data.backgroundColor || 'transparent';
    
    context.font = `${fontSize}px ${fontFamily}`;
    const textMetrics = context.measureText(content.data.text);
    
    canvas.width = Math.ceil(textMetrics.width) + 20;
    canvas.height = fontSize + 20;
    
    // Dessiner le fond
    if (backgroundColor !== 'transparent') {
      context.fillStyle = backgroundColor;
      context.fillRect(0, 0, canvas.width, canvas.height);
    }
    
    // Dessiner le texte
    context.font = `${fontSize}px ${fontFamily}`;
    context.fillStyle = color;
    context.textAlign = 'center';
    context.textBaseline = 'middle';
    context.fillText(content.data.text, canvas.width / 2, canvas.height / 2);
    
    // Créer la texture et le matériau
    const texture = new THREE.CanvasTexture(canvas);
    const material = new THREE.MeshBasicMaterial({
      map: texture,
      transparent: backgroundColor === 'transparent',
      alphaTest: 0.1
    });
    
    // Créer la géométrie
    const geometry = new THREE.PlaneGeometry(
      canvas.width / 100,
      canvas.height / 100
    );
    
    const mesh = new THREE.Mesh(geometry, material);
    mesh.userData.type = 'text';
    
    return mesh;
  }

  private async createImage(content: ARContent): Promise<THREE.Object3D> {
    return new Promise((resolve, reject) => {
      this.textureLoader.load(
        content.data.url,
        (texture) => {
          const material = new THREE.MeshBasicMaterial({
            map: texture,
            transparent: true,
            alphaTest: 0.1
          });
          
          const aspectRatio = texture.image.width / texture.image.height;
          const width = content.data.width || 1;
          const height = width / aspectRatio;
          
          const geometry = new THREE.PlaneGeometry(width, height);
          const mesh = new THREE.Mesh(geometry, material);
          mesh.userData.type = 'image';
          
          resolve(mesh);
        },
        undefined,
        reject
      );
    });
  }

  private async createVideo(content: ARContent): Promise<THREE.Object3D> {
    const video = document.createElement('video');
    video.src = content.data.url;
    video.crossOrigin = 'anonymous';
    video.loop = content.data.loop !== false;
    video.muted = content.data.muted !== false;
    video.playsInline = true;
    
    if (content.data.autoPlay !== false) {
      video.autoplay = true;
    }
    
    const texture = new THREE.VideoTexture(video);
    texture.minFilter = THREE.LinearFilter;
    texture.magFilter = THREE.LinearFilter;
    
    const material = new THREE.MeshBasicMaterial({
      map: texture
    });
    
    const aspectRatio = content.data.aspectRatio || 16/9;
    const width = content.data.width || 1;
    const height = width / aspectRatio;
    
    const geometry = new THREE.PlaneGeometry(width, height);
    const mesh = new THREE.Mesh(geometry, material);
    mesh.userData.type = 'video';
    mesh.userData.video = video;
    
    return mesh;
  }

  private createHTML(content: ARContent): THREE.Object3D {
    // Créer un élément HTML dans un iframe ou canvas
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d')!;
    
    canvas.width = content.data.width || 512;
    canvas.height = content.data.height || 512;
    
    // Rendu HTML simplifié (pour un rendu complet, utiliser html2canvas)
    context.fillStyle = content.data.backgroundColor || '#ffffff';
    context.fillRect(0, 0, canvas.width, canvas.height);
    
    context.fillStyle = content.data.color || '#000000';
    context.font = '16px Arial';
    context.fillText(content.data.html || 'HTML Content', 10, 30);
    
    const texture = new THREE.CanvasTexture(canvas);
    const material = new THREE.MeshBasicMaterial({
      map: texture,
      transparent: true
    });
    
    const geometry = new THREE.PlaneGeometry(
      canvas.width / 256,
      canvas.height / 256
    );
    
    const mesh = new THREE.Mesh(geometry, material);
    mesh.userData.type = 'html';
    
    return mesh;
  }

  private setupAnimations(object: THREE.Object3D, animations: ARAnimation[], contentId: string): void {
    animations.forEach((anim, index) => {
      const animId = `${contentId}_${index}`;
      
      switch (anim.type) {
        case 'rotation':
          this.createRotationAnimation(object, anim, animId);
          break;
        case 'scale':
          this.createScaleAnimation(object, anim, animId);
          break;
        case 'position':
          this.createPositionAnimation(object, anim, animId);
          break;
        case 'opacity':
          this.createOpacityAnimation(object, anim, animId);
          break;
      }
    });
  }

  private createRotationAnimation(object: THREE.Object3D, anim: ARAnimation, animId: string): void {
    // Implémentation simplifiée - dans une version complète, utiliser Tween.js
    const startRotation = object.rotation.clone();
    const targetRotation = new THREE.Euler().fromArray(anim.keyframes[anim.keyframes.length - 1]);
    
    const animate = () => {
      const time = (Date.now() % (anim.duration * 1000)) / (anim.duration * 1000);
      object.rotation.lerpVectors(startRotation, targetRotation, time);
      
      if (anim.loop) {
        requestAnimationFrame(animate);
      }
    };
    
    animate();
  }

  private createScaleAnimation(object: THREE.Object3D, anim: ARAnimation, animId: string): void {
    // Implémentation similaire pour l'échelle
    const startScale = object.scale.clone();
    const targetScale = new THREE.Vector3().fromArray(anim.keyframes[anim.keyframes.length - 1]);
    
    const animate = () => {
      const time = (Date.now() % (anim.duration * 1000)) / (anim.duration * 1000);
      object.scale.lerpVectors(startScale, targetScale, time);
      
      if (anim.loop) {
        requestAnimationFrame(animate);
      }
    };
    
    animate();
  }

  private createPositionAnimation(object: THREE.Object3D, anim: ARAnimation, animId: string): void {
    // Implémentation similaire pour la position
    const startPosition = object.position.clone();
    const targetPosition = new THREE.Vector3().fromArray(anim.keyframes[anim.keyframes.length - 1]);
    
    const animate = () => {
      const time = (Date.now() % (anim.duration * 1000)) / (anim.duration * 1000);
      object.position.lerpVectors(startPosition, targetPosition, time);
      
      if (anim.loop) {
        requestAnimationFrame(animate);
      }
    };
    
    animate();
  }

  private createOpacityAnimation(object: THREE.Object3D, anim: ARAnimation, animId: string): void {
    // Animation d'opacité
    object.traverse((child) => {
      if (child instanceof THREE.Mesh && child.material) {
        const material = child.material as THREE.Material;
        material.transparent = true;
        
        const startOpacity = material.opacity;
        const targetOpacity = anim.keyframes[anim.keyframes.length - 1];
        
        const animate = () => {
          const time = (Date.now() % (anim.duration * 1000)) / (anim.duration * 1000);
          material.opacity = THREE.MathUtils.lerp(startOpacity, targetOpacity, time);
          
          if (anim.loop) {
            requestAnimationFrame(animate);
          }
        };
        
        animate();
      }
    });
  }

  private setupObjectInteractions(object: THREE.Object3D): void {
    // Rendre l'objet interactif
    object.userData.interactive = true;
  }

  private optimizeMaterial(material: THREE.Material | THREE.Material[]): void {
    const materials = Array.isArray(material) ? material : [material];
    
    materials.forEach(mat => {
      if (mat instanceof THREE.MeshStandardMaterial) {
        // Optimisations pour mobile
        mat.envMapIntensity = 0.5;
        mat.roughness = Math.max(mat.roughness, 0.1);
      }
    });
  }

  private generateId(): string {
    return `content_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  // Gestion des interactions
  handlePointerEvent(event: PointerEvent, camera: THREE.Camera): void {
    // Convertir les coordonnées de l'écran en coordonnées normalisées
    const rect = (event.target as HTMLElement).getBoundingClientRect();
    this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

    // Raycasting
    this.raycaster.setFromCamera(this.mouse, camera);
    const intersects = this.raycaster.intersectObjects(this.arGroup.children, true);

    if (intersects.length > 0) {
      const object = intersects[0].object;
      const contentId = object.userData.contentId;
      
      if (contentId && this.interactions.has(contentId)) {
        const interactions = this.interactions.get(contentId)!;
        this.executeInteractions(interactions, event.type, object);
      }
    }
  }

  private executeInteractions(interactions: ARInteraction[], eventType: string, object: THREE.Object3D): void {
    interactions.forEach(interaction => {
      if (this.matchesEventType(interaction.type, eventType)) {
        this.executeInteraction(interaction, object);
      }
    });
  }

  private matchesEventType(interactionType: string, eventType: string): boolean {
    const mapping: { [key: string]: string[] } = {
      'click': ['click', 'pointerup'],
      'hover': ['pointerenter', 'pointermove'],
      'gaze': ['pointermove'] // Simplifié pour cet exemple
    };

    return mapping[interactionType]?.includes(eventType) || false;
  }

  private executeInteraction(interaction: ARInteraction, object: THREE.Object3D): void {
    switch (interaction.action) {
      case 'url':
        window.open(interaction.data.url, '_blank');
        break;
      case 'animation':
        this.triggerAnimation(object, interaction.data);
        break;
      case 'sound':
        this.playSound(interaction.data.url);
        break;
      case 'custom':
        this.emit('customInteraction', { interaction, object });
        break;
    }
  }

  private triggerAnimation(object: THREE.Object3D, animData: any): void {
    // Déclencher une animation personnalisée
    this.emit('animationTriggered', { object, animData });
  }

  private playSound(url: string): void {
    const audio = new Audio(url);
    audio.play().catch(error => {
      console.warn('Could not play sound:', error);
    });
  }

  // Mise à jour de la scène
  update(timestamp: number): void {
    const deltaTime = this.clock.getDelta();

    // Mettre à jour les animations
    this.animations.forEach(mixer => {
      mixer.update(deltaTime);
    });

    // Mettre à jour les vidéos
    this.contentObjects.forEach(object => {
      if (object.userData.type === 'video' && object.userData.video) {
        const video = object.userData.video as HTMLVideoElement;
        if (video.readyState >= video.HAVE_CURRENT_DATA) {
          (object as THREE.Mesh).material.map.needsUpdate = true;
        }
      }
    });
  }

  // Gestion de la visibilité
  setVisible(visible: boolean): void {
    this.isVisible = visible;
    this.arGroup.visible = visible;
    this.emit('visibilityChanged', visible);
  }

  // Mise à jour du tracking
  updateTracking(transform: THREE.Matrix4): void {
    if (transform) {
      this.arGroup.matrix.copy(transform);
      this.arGroup.matrixAutoUpdate = false;
    }
  }

  // Nettoyage
  clear(): void {
    // Supprimer tous les objets de contenu
    this.contentObjects.forEach((object, id) => {
      this.arGroup.remove(object);
      
      // Nettoyer les ressources
      object.traverse((child) => {
        if (child instanceof THREE.Mesh) {
          child.geometry.dispose();
          if (child.material) {
            if (Array.isArray(child.material)) {
              child.material.forEach(mat => mat.dispose());
            } else {
              child.material.dispose();
            }
          }
        }
      });
    });

    this.contentObjects.clear();
    this.animations.clear();
    this.interactions.clear();

    this.emit('cleared');
  }

  // Getters
  getScene(): THREE.Scene {
    return this.scene;
  }

  getARGroup(): THREE.Group {
    return this.arGroup;
  }

  getContentObject(id: string): THREE.Object3D | undefined {
    return this.contentObjects.get(id);
  }

  isVisibleState(): boolean {
    return this.isVisible;
  }

  // Nettoyage
  dispose(): void {
    this.clear();
    
    // Nettoyer les loaders
    if (this.gltfLoader) {
      // Les loaders Three.js n'ont pas de méthode dispose
    }

    this.emit('disposed');
  }
}