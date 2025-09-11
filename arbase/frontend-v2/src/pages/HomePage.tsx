/**
 * HomePage - Page d'accueil de l'application ARBase
 * Interface d'entrée avec navigation vers les différentes fonctionnalités
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Camera, 
  QrCode, 
  Zap, 
  Settings, 
  History, 
  Share2,
  Play,
  ArrowRight,
  Smartphone,
  Globe,
  Star
} from 'lucide-react';
import { useARStore, useARStats, useARHistory } from '../stores/arStore';
// import { ARSupport } from '../../ar-engine-v2';
import { toast } from 'react-hot-toast';

export const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const [support, setSupport] = useState({
    webxr: false,
    camera: false,
    webgl: false,
    webworker: false,
    overall: false
  });
  const [isCheckingSupport, setIsCheckingSupport] = useState(true);

  const { stats } = useARStats();
  const { history } = useARHistory();

  useEffect(() => {
    checkSupport();
  }, []);

  const checkSupport = async () => {
    try {
      // Vérification simplifiée du support
      const supportInfo = {
        webxr: 'xr' in navigator,
        camera: await checkCameraSupport(),
        webgl: checkWebGLSupport(),
        webworker: typeof Worker !== 'undefined',
        overall: true
      };
      supportInfo.overall = supportInfo.camera && supportInfo.webgl;
      setSupport(supportInfo);
    } catch (error) {
      console.error('Erreur de vérification du support:', error);
      setSupport({
        webxr: false,
        camera: false,
        webgl: false,
        webworker: false,
        overall: false
      });
    } finally {
      setIsCheckingSupport(false);
    }
  };

  const checkCameraSupport = async (): Promise<boolean> => {
    try {
      const devices = await navigator.mediaDevices.enumerateDevices();
      return devices.some(device => device.kind === 'videoinput');
    } catch {
      return false;
    }
  };

  const checkWebGLSupport = (): boolean => {
    try {
      const canvas = document.createElement('canvas');
      const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
      return !!gl;
    } catch {
      return false;
    }
  };

  const startScanning = () => {
    if (!support.overall) {
      toast.error('Votre appareil ne supporte pas toutes les fonctionnalités AR requises');
      return;
    }
    navigate('/scanner');
  };

  const openSettings = () => {
    navigate('/settings');
  };

  const shareApp = async () => {
    const shareData = {
      title: 'ARBase - Réalité Augmentée',
      text: 'Découvrez des expériences de réalité augmentée incroyables!',
      url: window.location.origin
    };

    if (navigator.share) {
      try {
        await navigator.share(shareData);
      } catch (error) {
        navigator.clipboard.writeText(shareData.url);
        toast.success('Lien copié dans le presse-papiers');
      }
    } else {
      navigator.clipboard.writeText(shareData.url);
      toast.success('Lien copié dans le presse-papiers');
    }
  };

  const recentExperiences = history.slice(0, 3);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-black text-white">
      {/* Header */}
      <header className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600/20 to-purple-600/20" />
        <div className="relative container mx-auto px-6 py-8">
          <div className="flex items-center justify-between">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5 }}
            >
              <h1 className="text-3xl font-bold flex items-center space-x-2">
                <Zap className="text-blue-400" />
                <span>ARBase</span>
              </h1>
              <p className="text-white/70 mt-1">Plateforme de Réalité Augmentée</p>
            </motion.div>

            <motion.button
              onClick={openSettings}
              className="p-3 bg-white/10 backdrop-blur-sm rounded-full hover:bg-white/20 transition-colors"
              whileTap={{ scale: 0.95 }}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
            >
              <Settings size={20} />
            </motion.button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-6 py-12">
        <div className="text-center mb-12">
          <motion.h2
            className="text-5xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            Découvrez la Réalité Augmentée
          </motion.h2>
          <motion.p
            className="text-xl text-white/80 max-w-2xl mx-auto mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            Scannez des QR codes pour révéler des expériences immersives en réalité augmentée. 
            Cartes de visite interactives, produits 3D, et bien plus encore.
          </motion.p>

          {/* Bouton principal */}
          <motion.button
            onClick={startScanning}
            disabled={isCheckingSupport || !support.overall}
            className="group relative px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full font-semibold text-lg hover:from-blue-600 hover:to-purple-600 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <span className="flex items-center space-x-2">
              {isCheckingSupport ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  <span>Vérification...</span>
                </>
              ) : support.overall ? (
                <>
                  <Camera size={20} />
                  <span>Commencer le Scan</span>
                  <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
                </>
              ) : (
                <>
                  <Zap size={20} />
                  <span>Non Compatible</span>
                </>
              )}
            </span>
          </motion.button>

          {/* Indicateurs de support */}
          {!isCheckingSupport && (
            <motion.div
              className="flex items-center justify-center space-x-6 mt-6 text-sm"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.6 }}
            >
              <div className={`flex items-center space-x-1 ${support.camera ? 'text-green-400' : 'text-red-400'}`}>
                <Camera size={16} />
                <span>Caméra</span>
              </div>
              <div className={`flex items-center space-x-1 ${support.webgl ? 'text-green-400' : 'text-red-400'}`}>
                <Globe size={16} />
                <span>WebGL</span>
              </div>
              <div className={`flex items-center space-x-1 ${support.webxr ? 'text-green-400' : 'text-yellow-400'}`}>
                <Zap size={16} />
                <span>WebXR</span>
              </div>
            </motion.div>
          )}
        </div>

        {/* Fonctionnalités */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          <motion.div
            className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 hover:bg-white/15 transition-colors"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.8 }}
          >
            <QrCode size={48} className="text-blue-400 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Scan QR Codes</h3>
            <p className="text-white/70">
              Pointez votre caméra vers un QR code ARBase pour révéler du contenu en réalité augmentée.
            </p>
          </motion.div>

          <motion.div
            className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 hover:bg-white/15 transition-colors"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1.0 }}
          >
            <Smartphone size={48} className="text-purple-400 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Expériences Immersives</h3>
            <p className="text-white/70">
              Découvrez des modèles 3D, des vidéos, des textes interactifs et bien plus encore.
            </p>
          </motion.div>

          <motion.div
            className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 hover:bg-white/15 transition-colors"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1.2 }}
          >
            <Share2 size={48} className="text-green-400 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Partage Facile</h3>
            <p className="text-white/70">
              Partagez vos découvertes et créez vos propres expériences AR facilement.
            </p>
          </motion.div>
        </div>

        {/* Statistiques et historique */}
        <div className="grid md:grid-cols-2 gap-8">
          {/* Statistiques */}
          <motion.div
            className="bg-white/10 backdrop-blur-sm rounded-2xl p-6"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 1.4 }}
          >
            <h3 className="text-xl font-semibold mb-4 flex items-center space-x-2">
              <Star className="text-yellow-400" />
              <span>Vos Statistiques</span>
            </h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-400">{stats.totalScans}</div>
                <div className="text-sm text-white/70">Scans</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-400">{stats.successfulDetections}</div>
                <div className="text-sm text-white/70">Détections</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-400">{stats.totalExperiences}</div>
                <div className="text-sm text-white/70">Expériences</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-orange-400">{Math.round(stats.averageSessionTime)}s</div>
                <div className="text-sm text-white/70">Temps moyen</div>
              </div>
            </div>
          </motion.div>

          {/* Historique récent */}
          <motion.div
            className="bg-white/10 backdrop-blur-sm rounded-2xl p-6"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 1.6 }}
          >
            <h3 className="text-xl font-semibold mb-4 flex items-center space-x-2">
              <History className="text-blue-400" />
              <span>Récemment Vues</span>
            </h3>
            {recentExperiences.length === 0 ? (
              <div className="text-center text-white/60 py-4">
                <p>Aucune expérience récente</p>
                <p className="text-sm mt-1">Commencez par scanner un QR code!</p>
              </div>
            ) : (
              <div className="space-y-3">
                {recentExperiences.map((entry, index) => (
                  <motion.div
                    key={entry.id}
                    className="flex items-center justify-between p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-colors cursor-pointer"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 1.8 + index * 0.1 }}
                    onClick={() => navigate(`/experience/${entry.experience.id}`)}
                  >
                    <div>
                      <div className="font-medium text-sm">{entry.experience.id}</div>
                      <div className="text-xs text-white/60">
                        {new Date(entry.timestamp).toLocaleDateString()}
                      </div>
                    </div>
                    <Play size={16} className="text-white/60" />
                  </motion.div>
                ))}
              </div>
            )}
          </motion.div>
        </div>

        {/* Actions secondaires */}
        <motion.div
          className="flex items-center justify-center space-x-4 mt-12"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 2.0 }}
        >
          <button
            onClick={shareApp}
            className="flex items-center space-x-2 px-6 py-3 bg-white/10 backdrop-blur-sm rounded-full hover:bg-white/20 transition-colors"
          >
            <Share2 size={16} />
            <span>Partager ARBase</span>
          </button>
        </motion.div>
      </section>
    </div>
  );
};