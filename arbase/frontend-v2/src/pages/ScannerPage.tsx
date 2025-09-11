/**
 * ScannerPage - Page principale du scanner AR
 * Interface complète avec navigation et fonctionnalités avancées
 */

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, 
  History, 
  Info, 
  Share2, 
  Settings,
  Zap,
  Camera,
  QrCode
} from 'lucide-react';
import { ARScanner } from '../components/ar/ARScanner';
import { useARStore, useARHistory, useARStats } from '../stores/arStore';
import { ARExperience } from '../../ar-engine-v2';
import { toast } from 'react-hot-toast';
import { cn } from '../utils/cn';

interface ScannerPageProps {
  onBack?: () => void;
}

export const ScannerPage: React.FC<ScannerPageProps> = ({ onBack }) => {
  const [showInfo, setShowInfo] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [currentExperience, setCurrentExperience] = useState<ARExperience | null>(null);
  
  const { isScanning } = useARStore();
  const { history } = useARHistory();
  const { stats } = useARStats();

  // Gestion des raccourcis clavier
  useEffect(() => {
    const handleKeyPress = (event: KeyboardEvent) => {
      switch (event.key) {
        case 'Escape':
          if (showInfo) setShowInfo(false);
          else if (showHistory) setShowHistory(false);
          else onBack?.();
          break;
        case 'h':
        case 'H':
          if (!isScanning) setShowHistory(!showHistory);
          break;
        case 'i':
        case 'I':
          if (!isScanning) setShowInfo(!showInfo);
          break;
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [showInfo, showHistory, isScanning, onBack]);

  const handleExperienceDetected = (experience: ARExperience) => {
    setCurrentExperience(experience);
    toast.success(`Expérience "${experience.id}" chargée`);
  };

  const handleError = (error: Error) => {
    toast.error(`Erreur: ${error.message}`);
  };

  const shareApp = async () => {
    const shareData = {
      title: 'ARBase Scanner',
      text: 'Découvrez la réalité augmentée avec ARBase!',
      url: window.location.origin
    };

    if (navigator.share) {
      try {
        await navigator.share(shareData);
      } catch (error) {
        // Fallback
        navigator.clipboard.writeText(shareData.url);
        toast.success('Lien copié dans le presse-papiers');
      }
    } else {
      navigator.clipboard.writeText(shareData.url);
      toast.success('Lien copié dans le presse-papiers');
    }
  };

  return (
    <div className="relative w-full h-screen bg-black overflow-hidden">
      {/* Scanner AR principal */}
      <ARScanner
        className="absolute inset-0"
        onExperienceDetected={handleExperienceDetected}
        onError={handleError}
      />

      {/* Navigation supérieure */}
      <div className="absolute top-0 left-0 right-0 z-10 p-4">
        <div className="flex items-center justify-between">
          {/* Bouton retour */}
          {onBack && (
            <motion.button
              onClick={onBack}
              className="p-3 bg-black/50 backdrop-blur-sm rounded-full text-white hover:bg-black/70 transition-colors"
              whileTap={{ scale: 0.95 }}
            >
              <ArrowLeft size={20} />
            </motion.button>
          )}

          {/* Titre */}
          <div className="flex-1 text-center">
            <h1 className="text-white text-lg font-bold">ARBase Scanner</h1>
            {currentExperience && (
              <p className="text-white/70 text-sm">
                {currentExperience.id}
              </p>
            )}
          </div>

          {/* Actions */}
          <div className="flex items-center space-x-2">
            <motion.button
              onClick={() => setShowHistory(!showHistory)}
              className="p-3 bg-black/50 backdrop-blur-sm rounded-full text-white hover:bg-black/70 transition-colors"
              whileTap={{ scale: 0.95 }}
            >
              <History size={20} />
            </motion.button>

            <motion.button
              onClick={() => setShowInfo(!showInfo)}
              className="p-3 bg-black/50 backdrop-blur-sm rounded-full text-white hover:bg-black/70 transition-colors"
              whileTap={{ scale: 0.95 }}
            >
              <Info size={20} />
            </motion.button>
          </div>
        </div>
      </div>

      {/* Instructions de scan */}
      {!isScanning && !currentExperience && (
        <motion.div
          className="absolute inset-0 flex items-center justify-center z-5"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <div className="text-center text-white p-8 bg-black/50 backdrop-blur-sm rounded-2xl mx-4">
            <QrCode size={64} className="mx-auto mb-4 text-blue-400" />
            <h2 className="text-2xl font-bold mb-2">Prêt à scanner</h2>
            <p className="text-white/70 mb-4">
              Pointez votre caméra vers un QR code pour découvrir une expérience AR
            </p>
            <div className="flex items-center justify-center space-x-4 text-sm text-white/60">
              <div className="flex items-center space-x-1">
                <Camera size={16} />
                <span>Caméra</span>
              </div>
              <div className="flex items-center space-x-1">
                <Zap size={16} />
                <span>AR</span>
              </div>
            </div>
          </div>
        </motion.div>
      )}

      {/* Panel d'informations */}
      <AnimatePresence>
        {showInfo && (
          <motion.div
            className="absolute inset-0 z-20 bg-black/90 backdrop-blur-sm"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <div className="h-full overflow-y-auto p-6 text-white">
              <div className="max-w-2xl mx-auto">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold">À propos d'ARBase</h2>
                  <button
                    onClick={() => setShowInfo(false)}
                    className="p-2 hover:bg-white/10 rounded-full transition-colors"
                  >
                    ✕
                  </button>
                </div>

                <div className="space-y-6">
                  <section>
                    <h3 className="text-lg font-semibold mb-3">Comment utiliser</h3>
                    <div className="space-y-2 text-white/80">
                      <p>1. Appuyez sur le bouton de scan pour démarrer la caméra</p>
                      <p>2. Pointez votre appareil vers un QR code ARBase</p>
                      <p>3. Attendez la détection automatique</p>
                      <p>4. Profitez de l'expérience de réalité augmentée!</p>
                    </div>
                  </section>

                  <section>
                    <h3 className="text-lg font-semibold mb-3">Statistiques</h3>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-white/10 rounded-lg p-4">
                        <div className="text-2xl font-bold text-blue-400">
                          {stats.totalScans}
                        </div>
                        <div className="text-sm text-white/70">Scans totaux</div>
                      </div>
                      <div className="bg-white/10 rounded-lg p-4">
                        <div className="text-2xl font-bold text-green-400">
                          {stats.successfulDetections}
                        </div>
                        <div className="text-sm text-white/70">Détections réussies</div>
                      </div>
                      <div className="bg-white/10 rounded-lg p-4">
                        <div className="text-2xl font-bold text-purple-400">
                          {stats.totalExperiences}
                        </div>
                        <div className="text-sm text-white/70">Expériences</div>
                      </div>
                      <div className="bg-white/10 rounded-lg p-4">
                        <div className="text-2xl font-bold text-orange-400">
                          {Math.round(stats.averageSessionTime)}s
                        </div>
                        <div className="text-sm text-white/70">Temps moyen</div>
                      </div>
                    </div>
                  </section>

                  <section>
                    <h3 className="text-lg font-semibold mb-3">Raccourcis clavier</h3>
                    <div className="space-y-2 text-white/80">
                      <div className="flex justify-between">
                        <span>Historique</span>
                        <kbd className="px-2 py-1 bg-white/20 rounded text-xs">H</kbd>
                      </div>
                      <div className="flex justify-between">
                        <span>Informations</span>
                        <kbd className="px-2 py-1 bg-white/20 rounded text-xs">I</kbd>
                      </div>
                      <div className="flex justify-between">
                        <span>Retour</span>
                        <kbd className="px-2 py-1 bg-white/20 rounded text-xs">ESC</kbd>
                      </div>
                    </div>
                  </section>

                  <section>
                    <h3 className="text-lg font-semibold mb-3">Partager</h3>
                    <button
                      onClick={shareApp}
                      className="flex items-center space-x-2 px-4 py-2 bg-blue-500 hover:bg-blue-600 rounded-lg transition-colors"
                    >
                      <Share2 size={16} />
                      <span>Partager ARBase</span>
                    </button>
                  </section>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Panel d'historique */}
      <AnimatePresence>
        {showHistory && (
          <motion.div
            className="absolute right-0 top-0 bottom-0 w-80 bg-black/90 backdrop-blur-sm z-20"
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 20 }}
          >
            <div className="h-full flex flex-col text-white">
              <div className="flex items-center justify-between p-4 border-b border-white/20">
                <h3 className="text-lg font-bold">Historique</h3>
                <button
                  onClick={() => setShowHistory(false)}
                  className="p-2 hover:bg-white/10 rounded-full transition-colors"
                >
                  ✕
                </button>
              </div>

              <div className="flex-1 overflow-y-auto p-4">
                {history.length === 0 ? (
                  <div className="text-center text-white/60 py-8">
                    <History size={48} className="mx-auto mb-4 opacity-50" />
                    <p>Aucune expérience dans l'historique</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {history.map((entry) => (
                      <motion.div
                        key={entry.id}
                        className="bg-white/10 rounded-lg p-3 hover:bg-white/20 transition-colors cursor-pointer"
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        onClick={() => {
                          setCurrentExperience(entry.experience);
                          setShowHistory(false);
                        }}
                      >
                        <div className="font-medium text-sm mb-1">
                          {entry.experience.id}
                        </div>
                        <div className="text-xs text-white/70 mb-2">
                          {new Date(entry.timestamp).toLocaleString()}
                        </div>
                        <div className="flex justify-between text-xs text-white/60">
                          <span>{entry.duration}s</span>
                          <span>{entry.interactions} interactions</span>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Indicateur d'expérience active */}
      <AnimatePresence>
        {currentExperience && (
          <motion.div
            className="absolute bottom-20 left-4 right-4 z-10"
            initial={{ y: 100, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 100, opacity: 0 }}
          >
            <div className="bg-black/70 backdrop-blur-sm rounded-lg p-4 text-white">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium">{currentExperience.id}</h4>
                  <p className="text-sm text-white/70">
                    {currentExperience.content.length} éléments
                  </p>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                  <span className="text-xs">Actif</span>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};