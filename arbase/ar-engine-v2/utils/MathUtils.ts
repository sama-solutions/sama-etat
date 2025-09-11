/**
 * MathUtils - Utilitaires mathématiques pour l'AR
 */

import * as THREE from 'three';

export class MathUtils {
  /**
   * Convertit une matrice de transformation 4x4 en pose (position, rotation, échelle)
   */
  static matrixToPose(matrix: THREE.Matrix4): {
    position: THREE.Vector3;
    rotation: THREE.Euler;
    scale: THREE.Vector3;
  } {
    const position = new THREE.Vector3();
    const quaternion = new THREE.Quaternion();
    const scale = new THREE.Vector3();
    
    matrix.decompose(position, quaternion, scale);
    
    const rotation = new THREE.Euler().setFromQuaternion(quaternion);
    
    return { position, rotation, scale };
  }

  /**
   * Crée une matrice de transformation à partir d'une pose
   */
  static poseToMatrix(pose: {
    position: THREE.Vector3;
    rotation: THREE.Euler;
    scale: THREE.Vector3;
  }): THREE.Matrix4 {
    const matrix = new THREE.Matrix4();
    const quaternion = new THREE.Quaternion().setFromEuler(pose.rotation);
    matrix.compose(pose.position, quaternion, pose.scale);
    return matrix;
  }

  /**
   * Calcule la distance entre deux points 3D
   */
  static distance3D(a: THREE.Vector3, b: THREE.Vector3): number {
    return a.distanceTo(b);
  }

  /**
   * Calcule la distance entre deux points 2D
   */
  static distance2D(a: THREE.Vector2, b: THREE.Vector2): number {
    return a.distanceTo(b);
  }

  /**
   * Interpole linéairement entre deux valeurs
   */
  static lerp(a: number, b: number, t: number): number {
    return a + (b - a) * t;
  }

  /**
   * Interpole linéairement entre deux vecteurs 3D
   */
  static lerpVector3(a: THREE.Vector3, b: THREE.Vector3, t: number): THREE.Vector3 {
    return new THREE.Vector3().lerpVectors(a, b, t);
  }

  /**
   * Clamp une valeur entre min et max
   */
  static clamp(value: number, min: number, max: number): number {
    return Math.max(min, Math.min(max, value));
  }

  /**
   * Normalise un angle en radians entre -π et π
   */
  static normalizeAngle(angle: number): number {
    while (angle > Math.PI) angle -= 2 * Math.PI;
    while (angle < -Math.PI) angle += 2 * Math.PI;
    return angle;
  }

  /**
   * Convertit des degrés en radians
   */
  static degToRad(degrees: number): number {
    return degrees * Math.PI / 180;
  }

  /**
   * Convertit des radians en degrés
   */
  static radToDeg(radians: number): number {
    return radians * 180 / Math.PI;
  }

  /**
   * Calcule l'angle entre deux vecteurs 3D
   */
  static angleBetweenVectors(a: THREE.Vector3, b: THREE.Vector3): number {
    return a.angleTo(b);
  }

  /**
   * Projette un point 3D sur un plan
   */
  static projectPointOnPlane(point: THREE.Vector3, planeNormal: THREE.Vector3, planePoint: THREE.Vector3): THREE.Vector3 {
    const plane = new THREE.Plane(planeNormal, -planeNormal.dot(planePoint));
    return plane.projectPoint(point, new THREE.Vector3());
  }

  /**
   * Calcule l'intersection entre un rayon et un plan
   */
  static rayPlaneIntersection(ray: THREE.Ray, plane: THREE.Plane): THREE.Vector3 | null {
    const target = new THREE.Vector3();
    const intersection = ray.intersectPlane(plane, target);
    return intersection;
  }

  /**
   * Calcule la matrice de vue à partir d'une position et d'une cible
   */
  static lookAtMatrix(position: THREE.Vector3, target: THREE.Vector3, up: THREE.Vector3 = new THREE.Vector3(0, 1, 0)): THREE.Matrix4 {
    const matrix = new THREE.Matrix4();
    matrix.lookAt(position, target, up);
    return matrix;
  }

  /**
   * Calcule la matrice de projection perspective
   */
  static perspectiveMatrix(fov: number, aspect: number, near: number, far: number): THREE.Matrix4 {
    const matrix = new THREE.Matrix4();
    matrix.makePerspective(-aspect * near * Math.tan(fov / 2), aspect * near * Math.tan(fov / 2), near * Math.tan(fov / 2), -near * Math.tan(fov / 2), near, far);
    return matrix;
  }

  /**
   * Calcule la matrice de projection orthographique
   */
  static orthographicMatrix(left: number, right: number, top: number, bottom: number, near: number, far: number): THREE.Matrix4 {
    const matrix = new THREE.Matrix4();
    matrix.makeOrthographic(left, right, top, bottom, near, far);
    return matrix;
  }

  /**
   * Vérifie si un point est à l'intérieur d'un triangle 2D
   */
  static pointInTriangle2D(point: THREE.Vector2, a: THREE.Vector2, b: THREE.Vector2, c: THREE.Vector2): boolean {
    const v0 = c.clone().sub(a);
    const v1 = b.clone().sub(a);
    const v2 = point.clone().sub(a);

    const dot00 = v0.dot(v0);
    const dot01 = v0.dot(v1);
    const dot02 = v0.dot(v2);
    const dot11 = v1.dot(v1);
    const dot12 = v1.dot(v2);

    const invDenom = 1 / (dot00 * dot11 - dot01 * dot01);
    const u = (dot11 * dot02 - dot01 * dot12) * invDenom;
    const v = (dot00 * dot12 - dot01 * dot02) * invDenom;

    return (u >= 0) && (v >= 0) && (u + v <= 1);
  }

  /**
   * Calcule l'aire d'un triangle 3D
   */
  static triangleArea3D(a: THREE.Vector3, b: THREE.Vector3, c: THREE.Vector3): number {
    const ab = b.clone().sub(a);
    const ac = c.clone().sub(a);
    return ab.cross(ac).length() / 2;
  }

  /**
   * Calcule le centre d'un ensemble de points
   */
  static centroid(points: THREE.Vector3[]): THREE.Vector3 {
    const center = new THREE.Vector3();
    points.forEach(point => center.add(point));
    center.divideScalar(points.length);
    return center;
  }

  /**
   * Calcule la boîte englobante d'un ensemble de points
   */
  static boundingBox(points: THREE.Vector3[]): THREE.Box3 {
    const box = new THREE.Box3();
    points.forEach(point => box.expandByPoint(point));
    return box;
  }

  /**
   * Génère un nombre aléatoire entre min et max
   */
  static random(min: number = 0, max: number = 1): number {
    return Math.random() * (max - min) + min;
  }

  /**
   * Génère un vecteur 3D aléatoire dans une sphère
   */
  static randomVector3InSphere(radius: number = 1): THREE.Vector3 {
    const u = Math.random();
    const v = Math.random();
    const theta = 2 * Math.PI * u;
    const phi = Math.acos(2 * v - 1);
    const r = radius * Math.cbrt(Math.random());

    const x = r * Math.sin(phi) * Math.cos(theta);
    const y = r * Math.sin(phi) * Math.sin(theta);
    const z = r * Math.cos(phi);

    return new THREE.Vector3(x, y, z);
  }

  /**
   * Génère un vecteur 3D aléatoire sur une sphère
   */
  static randomVector3OnSphere(radius: number = 1): THREE.Vector3 {
    const u = Math.random();
    const v = Math.random();
    const theta = 2 * Math.PI * u;
    const phi = Math.acos(2 * v - 1);

    const x = radius * Math.sin(phi) * Math.cos(theta);
    const y = radius * Math.sin(phi) * Math.sin(theta);
    const z = radius * Math.cos(phi);

    return new THREE.Vector3(x, y, z);
  }

  /**
   * Calcule la moyenne mobile d'un tableau de valeurs
   */
  static movingAverage(values: number[], windowSize: number): number[] {
    const result: number[] = [];
    for (let i = 0; i < values.length; i++) {
      const start = Math.max(0, i - windowSize + 1);
      const window = values.slice(start, i + 1);
      const average = window.reduce((sum, val) => sum + val, 0) / window.length;
      result.push(average);
    }
    return result;
  }

  /**
   * Filtre passe-bas simple pour lisser les valeurs
   */
  static lowPassFilter(currentValue: number, newValue: number, alpha: number): number {
    return alpha * newValue + (1 - alpha) * currentValue;
  }

  /**
   * Calcule la dérivée numérique (vitesse de changement)
   */
  static derivative(values: number[], deltaTime: number): number[] {
    const result: number[] = [];
    for (let i = 1; i < values.length; i++) {
      result.push((values[i] - values[i - 1]) / deltaTime);
    }
    return result;
  }

  /**
   * Vérifie si deux nombres sont approximativement égaux
   */
  static approximately(a: number, b: number, epsilon: number = 1e-6): boolean {
    return Math.abs(a - b) < epsilon;
  }

  /**
   * Vérifie si deux vecteurs 3D sont approximativement égaux
   */
  static approximatelyVector3(a: THREE.Vector3, b: THREE.Vector3, epsilon: number = 1e-6): boolean {
    return this.approximately(a.x, b.x, epsilon) &&
           this.approximately(a.y, b.y, epsilon) &&
           this.approximately(a.z, b.z, epsilon);
  }
}