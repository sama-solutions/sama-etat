/**
 * App - Application principale ARBase
 * Point d'entrée avec routing et configuration globale
 */

import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { motion, AnimatePresence } from 'framer-motion';
import { ScannerPage } from './pages/ScannerPage';
import { HomePage } from './pages/HomePage';
import { ExperiencePage } from './pages/ExperiencePage';
import { SettingsPage } from './pages/SettingsPage';
import { useARStore } from './stores/arStore';

function App() {
  const { isInitialized, setIsInitialized } = useARStore();

  useEffect(() => {
    // Initialisation de l'application
    const initApp = async () => {
      try {
        // Enregistrer le service worker pour PWA (optionnel)
        if ('serviceWorker' in navigator && process.env.NODE_ENV === 'production') {
          try {
            await navigator.serviceWorker.register('/sw.js');
            console.log('Service Worker enregistré avec succès');
          } catch (swError) {
            console.warn('Service Worker non disponible:', swError.message);
            // Continuer sans Service Worker
          }
        }

        // Marquer comme initialisé
        setIsInitialized(true);
      } catch (error) {
        console.error('Erreur d\'initialisation:', error);
        // Même en cas d'erreur, initialiser l'app
        setIsInitialized(true);
      }
    };

    initApp();
  }, [setIsInitialized]);

  if (!isInitialized) {
    return <LoadingScreen />;
  }

  return (
    <Router>
      <div className="App">
        <AnimatePresence mode="wait">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/scanner" element={<ScannerPage />} />
            <Route path="/experience/:id" element={<ExperiencePage />} />
            <Route path="/settings" element={<SettingsPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AnimatePresence>

        {/* Toast notifications */}
        <Toaster
          position="top-center"
          toastOptions={{
            duration: 3000,
            style: {
              background: 'rgba(0, 0, 0, 0.8)',
              color: 'white',
              backdropFilter: 'blur(10px)',
              border: '1px solid rgba(255, 255, 255, 0.1)',
            },
            success: {
              iconTheme: {
                primary: '#10B981',
                secondary: 'white',
              },
            },
            error: {
              iconTheme: {
                primary: '#EF4444',
                secondary: 'white',
              },
            },
          }}
        />
      </div>
    </Router>
  );
}

const LoadingScreen: React.FC = () => {
  return (
    <div className="fixed inset-0 bg-black flex items-center justify-center">
      <motion.div
        className="text-center text-white"
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <motion.div
          className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
        />
        <h1 className="text-2xl font-bold mb-2">ARBase</h1>
        <p className="text-white/70">Initialisation...</p>
      </motion.div>
    </div>
  );
};

export default App;