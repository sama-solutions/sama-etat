/**
 * ARScanner - Composant principal du scanner AR
 * Version simplifiée sans dépendance ar-engine-v2
 */

import React, { useRef, useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Camera, QrCode, Zap, Settings, AlertCircle } from 'lucide-react';
import { useARStore } from '../../stores/arStore';
import { toast } from 'react-hot-toast';

interface ARScannerProps {
  className?: string;
  onExperienceDetected?: (experience: any) => void;
  onError?: (error: Error) => void;
}

export const ARScanner: React.FC<ARScannerProps> = ({
  className = '',
  onExperienceDetected,
  onError
}) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isScanning, setIsScanning] = useState(false);
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [scanCount, setScanCount] = useState(0);

  const { settings, updateSettings } = useARStore();

  useEffect(() => {
    checkCameraPermission();
    return () => {
      stopCamera();
    };
  }, []);

  const checkCameraPermission = async () => {
    try {
      // Vérifier si la caméra est disponible
      const devices = await navigator.mediaDevices.enumerateDevices();
      const hasCamera = devices.some(device => device.kind === 'videoinput');
      
      if (!hasCamera) {
        setHasPermission(false);
        onError?.(new Error('Aucune caméra détectée'));
        return;
      }

      setHasPermission(true);
    } catch (error) {
      console.error('Erreur vérification caméra:', error);
      setHasPermission(false);
      onError?.(error as Error);
    }
  };

  const startCamera = async () => {
    if (!videoRef.current) return;

    setIsLoading(true);
    
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { 
          facingMode: 'environment',
          width: { ideal: 1280 },
          height: { ideal: 720 }
        }
      });
      
      videoRef.current.srcObject = stream;
      setHasPermission(true);
      setIsScanning(true);
      
      toast.success('Scanner AR activé');
      
      // Simuler la détection de QR codes
      startQRDetection();
      
    } catch (error) {
      console.error('Erreur caméra:', error);
      setHasPermission(false);
      toast.error('Impossible d\'accéder à la caméra');
      onError?.(new Error('Accès caméra refusé'));
    } finally {
      setIsLoading(false);
    }
  };

  const stopCamera = () => {
    if (videoRef.current?.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      stream.getTracks().forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
    setIsScanning(false);
    toast.success('Scanner arrêté');
  };

  const startQRDetection = () => {
    // Simulation de détection QR (dans une vraie app, utiliser une lib comme jsQR)
    const detectInterval = setInterval(() => {
      if (!isScanning) {
        clearInterval(detectInterval);
        return;
      }

      // Simuler une détection aléatoire
      if (Math.random() > 0.98) { // 2% de chance par frame
        const mockExperience = {
          id: `demo_${Date.now()}`,
          title: 'Expérience AR Demo',
          description: 'Expérience de démonstration détectée',
          qrCode: `demo_qr_${scanCount}`,
          content: [
            {
              type: 'text',
              data: { text: 'Bonjour ARBase!' },
              position: { x: 0, y: 0, z: 0 }
            }
          ]
        };

        setScanCount(prev => prev + 1);
        toast.success(`QR Code détecté! (${scanCount + 1})`);
        onExperienceDetected?.(mockExperience);
      }
    }, settings.scanInterval || 100);
  };

  const toggleScanning = () => {
    if (isScanning) {
      stopCamera();
    } else {
      startCamera();
    }
  };

  if (hasPermission === false) {
    return (
      <div className={`flex items-center justify-center bg-black text-white ${className}`}>
        <div className="text-center p-8">
          <AlertCircle size={64} className="mx-auto mb-4 text-red-400" />
          <h2 className="text-xl font-bold mb-2">Accès caméra requis</h2>
          <p className="text-white/70 mb-4">
            Veuillez autoriser l'accès à la caméra pour utiliser le scanner AR
          </p>
          <button
            onClick={checkCameraPermission}
            className="px-6 py-3 bg-blue-500 hover:bg-blue-600 rounded-lg transition-colors"
          >
            Réessayer
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`relative bg-black overflow-hidden ${className}`}>
      {/* Vidéo de la caméra */}
      <video
        ref={videoRef}
        autoPlay
        playsInline
        muted
        className="w-full h-full object-cover"
        style={{ transform: 'scaleX(-1)' }} // Effet miroir
      />

      {/* Overlay de scan */}
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="relative">
          {/* Cadre de scan principal */}
          <div className="w-64 h-64 border-2 border-white/50 rounded-lg relative">
            {/* Coins animés */}
            <div className="absolute top-0 left-0 w-8 h-8 border-t-4 border-l-4 border-blue-400 rounded-tl-lg" />
            <div className="absolute top-0 right-0 w-8 h-8 border-t-4 border-r-4 border-blue-400 rounded-tr-lg" />
            <div className="absolute bottom-0 left-0 w-8 h-8 border-b-4 border-l-4 border-blue-400 rounded-bl-lg" />
            <div className="absolute bottom-0 right-0 w-8 h-8 border-b-4 border-r-4 border-blue-400 rounded-br-lg" />
            
            {/* Ligne de scan animée */}
            {isScanning && (
              <motion.div
                className="absolute left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-blue-400 to-transparent"
                animate={{ y: [0, 256, 0] }}
                transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
              />
            )}

            {/* Icône centrale */}
            <div className="absolute inset-0 flex items-center justify-center">
              <QrCode 
                size={48} 
                className={`text-white/70 ${isScanning ? 'animate-pulse' : ''}`} 
              />
            </div>
          </div>
          
          {/* Instructions */}
          <div className="absolute -bottom-20 left-1/2 transform -translate-x-1/2 text-center">
            <p className="text-white/70 text-sm mb-2">
              {isScanning 
                ? 'Pointez vers un QR code ARBase' 
                : 'Appuyez pour commencer le scan'
              }
            </p>
            {scanCount > 0 && (
              <p className="text-green-400 text-xs">
                {scanCount} QR code{scanCount > 1 ? 's' : ''} détecté{scanCount > 1 ? 's' : ''}
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Indicateur de statut */}
      <div className="absolute top-4 left-4 flex items-center space-x-2 bg-black/50 backdrop-blur-sm rounded-full px-3 py-2">
        <div className={`w-2 h-2 rounded-full ${
          isScanning ? 'bg-green-400 animate-pulse' : 'bg-red-400'
        }`} />
        <span className="text-white text-sm">
          {isLoading ? 'Initialisation...' : isScanning ? 'Scan actif' : 'Scan arrêté'}
        </span>
      </div>

      {/* Bouton de contrôle principal */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2">
        <motion.button
          onClick={toggleScanning}
          disabled={isLoading || hasPermission === null}
          className={`w-16 h-16 rounded-full flex items-center justify-center text-white transition-all ${
            isScanning 
              ? 'bg-red-500 hover:bg-red-600' 
              : 'bg-blue-500 hover:bg-blue-600'
          } ${(isLoading || hasPermission === null) ? 'opacity-50 cursor-not-allowed' : ''}`}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {isLoading ? (
            <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin" />
          ) : isScanning ? (
            <div className="w-4 h-4 bg-white rounded-sm" />
          ) : (
            <Camera size={24} />
          )}
        </motion.button>
      </div>

      {/* Paramètres rapides */}
      <div className="absolute top-4 right-4">
        <button
          onClick={() => updateSettings({ debug: !settings.debug })}
          className="p-2 bg-black/50 backdrop-blur-sm rounded-full text-white hover:bg-black/70 transition-colors"
        >
          <Settings size={20} />
        </button>
      </div>

      {/* Informations de debug */}
      {settings.debug && (
        <div className="absolute bottom-4 left-4 bg-black/70 backdrop-blur-sm rounded-lg p-3 text-white text-xs font-mono">
          <div>Status: {isScanning ? 'Actif' : 'Inactif'}</div>
          <div>Scans: {scanCount}</div>
          <div>Intervalle: {settings.scanInterval}ms</div>
          <div>Confiance: {settings.minConfidence}</div>
        </div>
      )}

      {/* Message d'aide */}
      {!isScanning && hasPermission && (
        <div className="absolute inset-x-4 bottom-24 text-center">
          <div className="bg-black/50 backdrop-blur-sm rounded-lg p-4 text-white">
            <Zap className="w-6 h-6 mx-auto mb-2 text-blue-400" />
            <p className="text-sm">
              Appuyez sur le bouton pour démarrer le scanner AR
            </p>
            <p className="text-xs text-white/70 mt-1">
              Assurez-vous d'avoir un bon éclairage
            </p>
          </div>
        </div>
      )}
    </div>
  );
};