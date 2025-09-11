/**
 * QRWorker - Web Worker pour la détection de QR codes
 * Traitement en arrière-plan pour ne pas bloquer le thread principal
 */

import jsQR from 'jsqr';

interface QRWorkerMessage {
  type: 'scan' | 'configure';
  data: any;
}

interface QRWorkerResponse {
  type: 'result' | 'error' | 'configured';
  data: any;
}

interface QRScanConfig {
  inversionAttempts?: 'dontInvert' | 'onlyInvert' | 'attemptBoth';
  greyScaleWeights?: {
    red: number;
    green: number;
    blue: number;
    useIntegerApproximation?: boolean;
  };
  canOverwriteImage?: boolean;
}

class QRWorkerProcessor {
  private config: QRScanConfig = {
    inversionAttempts: 'dontInvert',
    canOverwriteImage: true
  };

  configure(newConfig: QRScanConfig): void {
    this.config = { ...this.config, ...newConfig };
  }

  scanImageData(imageData: ImageData): any {
    try {
      const result = jsQR(
        imageData.data,
        imageData.width,
        imageData.height,
        this.config
      );

      if (result) {
        return {
          success: true,
          data: result.data,
          location: result.location,
          binaryData: result.binaryData,
          chunks: result.chunks
        };
      } else {
        return {
          success: false,
          data: null
        };
      }
    } catch (error) {
      throw new Error(`QR scanning failed: ${error.message}`);
    }
  }

  // Préprocessing de l'image pour améliorer la détection
  preprocessImage(imageData: ImageData): ImageData {
    const data = new Uint8ClampedArray(imageData.data);
    const width = imageData.width;
    const height = imageData.height;

    // Conversion en niveaux de gris avec pondération optimisée
    for (let i = 0; i < data.length; i += 4) {
      const r = data[i];
      const g = data[i + 1];
      const b = data[i + 2];
      
      // Formule optimisée pour la détection de QR codes
      const gray = Math.round(0.299 * r + 0.587 * g + 0.114 * b);
      
      data[i] = gray;     // R
      data[i + 1] = gray; // G
      data[i + 2] = gray; // B
      // Alpha reste inchangé
    }

    // Amélioration du contraste
    this.enhanceContrast(data);

    return new ImageData(data, width, height);
  }

  private enhanceContrast(data: Uint8ClampedArray): void {
    // Calcul de l'histogramme
    const histogram = new Array(256).fill(0);
    for (let i = 0; i < data.length; i += 4) {
      histogram[data[i]]++;
    }

    // Calcul de la fonction de transformation
    const totalPixels = data.length / 4;
    let sum = 0;
    const lut = new Array(256);
    
    for (let i = 0; i < 256; i++) {
      sum += histogram[i];
      lut[i] = Math.round((sum / totalPixels) * 255);
    }

    // Application de la transformation
    for (let i = 0; i < data.length; i += 4) {
      const newValue = lut[data[i]];
      data[i] = newValue;     // R
      data[i + 1] = newValue; // G
      data[i + 2] = newValue; // B
    }
  }
}

// Instance du processeur
const processor = new QRWorkerProcessor();

// Gestionnaire des messages
self.onmessage = function(e: MessageEvent<QRWorkerMessage>) {
  const {type, data} = e.data;

  try {
    switch (type) {
      case 'configure':
        processor.configure(data);
        self.postMessage({
          type: 'configured',
          data: { success: true }
        } as QRWorkerResponse);
        break;

      case 'scan':
        const {imageData, preprocess = true} = data;
        
        let processedImageData = imageData;
        
        // Préprocessing si demandé
        if (preprocess) {
          processedImageData = processor.preprocessImage(imageData);
        }

        // Scan de l'image
        const result = processor.scanImageData(processedImageData);
        
        self.postMessage({
          type: 'result',
          data: result
        } as QRWorkerResponse);
        break;

      default:
        throw new Error(`Unknown message type: ${type}`);
    }
  } catch (error) {
    self.postMessage({
      type: 'error',
      data: {
        message: error.message,
        stack: error.stack
      }
    } as QRWorkerResponse);
  }
};

// Export pour TypeScript
export {};