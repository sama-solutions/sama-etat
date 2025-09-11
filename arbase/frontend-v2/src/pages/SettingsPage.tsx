/**
 * SettingsPage - Page de paramètres de l'application
 */

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  ArrowLeft, 
  Settings, 
  Camera, 
  Volume2, 
  VolumeX, 
  Vibrate, 
  Eye, 
  Download,
  Upload,
  Trash2,
  Info
} from 'lucide-react';
import { useARSettings, useARStats, useARHistory } from '../stores/arStore';
import { toast } from 'react-hot-toast';

export const SettingsPage: React.FC = () => {
  const navigate = useNavigate();
  const { settings, updateSettings } = useARSettings();
  const { stats } = useARStats();
  const { history, clearHistory } = useARHistory();
  
  const [showConfirmClear, setShowConfirmClear] = useState(false);

  const handleSettingChange = (key: string, value: any) => {
    updateSettings({ [key]: value });
    toast.success('Paramètre mis à jour');
  };

  const handleExportData = () => {
    try {
      const data = {
        settings,
        stats,
        history,
        exportDate: new Date().toISOString()
      };
      
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `arbase-data-${new Date().toISOString().split('T')[0]}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      
      toast.success('Données exportées');
    } catch (error) {
      toast.error('Erreur lors de l\'export');
    }
  };

  const handleImportData = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const data = JSON.parse(e.target?.result as string);
        
        if (data.settings) {
          updateSettings(data.settings);
        }
        
        toast.success('Données importées');
      } catch (error) {
        toast.error('Fichier invalide');
      }
    };
    reader.readAsText(file);
  };

  const handleClearHistory = () => {
    clearHistory();
    setShowConfirmClear(false);
    toast.success('Historique effacé');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-black text-white">
      {/* Header */}
      <header className="relative p-6">
        <div className="flex items-center justify-between">
          <button
            onClick={() => navigate(-1)}
            className="p-3 bg-white/10 backdrop-blur-sm rounded-full hover:bg-white/20 transition-colors"
          >
            <ArrowLeft size={20} />
          </button>
          
          <h1 className="text-xl font-bold flex items-center space-x-2">
            <Settings size={20} />
            <span>Paramètres</span>
          </h1>
          
          <div className="w-12" /> {/* Spacer */}
        </div>
      </header>

      {/* Contenu */}
      <main className="container mx-auto px-6 pb-6">
        <motion.div
          className="max-w-2xl mx-auto space-y-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          {/* Paramètres AR */}
          <section className="bg-white/10 backdrop-blur-sm rounded-2xl p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center space-x-2">
              <Camera className="text-blue-400" />
              <span>Paramètres AR</span>
            </h2>
            
            <div className="space-y-4">
              {/* Intervalle de scan */}
              <div>
                <label className="block text-sm font-medium mb-2">
                  Intervalle de scan (ms)
                </label>
                <input
                  type="range"
                  min="50"
                  max="500"
                  step="50"
                  value={settings.scanInterval}
                  onChange={(e) => handleSettingChange('scanInterval', parseInt(e.target.value))}
                  className="w-full"
                />
                <div className="text-sm text-white/70 mt-1">
                  Actuel: {settings.scanInterval}ms
                </div>
              </div>

              {/* Confiance minimale */}
              <div>
                <label className="block text-sm font-medium mb-2">
                  Confiance minimale
                </label>
                <input
                  type="range"
                  min="0.1"
                  max="1"
                  step="0.1"
                  value={settings.minConfidence}
                  onChange={(e) => handleSettingChange('minConfidence', parseFloat(e.target.value))}
                  className="w-full"
                />
                <div className="text-sm text-white/70 mt-1">
                  Actuel: {(settings.minConfidence * 100).toFixed(0)}%
                </div>
              </div>

              {/* Distance maximale */}
              <div>
                <label className="block text-sm font-medium mb-2">
                  Distance maximale (m)
                </label>
                <input
                  type="range"
                  min="1"
                  max="20"
                  step="1"
                  value={settings.maxDistance}
                  onChange={(e) => handleSettingChange('maxDistance', parseInt(e.target.value))}
                  className="w-full"
                />
                <div className="text-sm text-white/70 mt-1">
                  Actuel: {settings.maxDistance}m
                </div>
              </div>

              {/* WebXR */}
              <div className="flex items-center justify-between">
                <div>
                  <div className="font-medium">WebXR</div>
                  <div className="text-sm text-white/70">AR native si disponible</div>
                </div>
                <button
                  onClick={() => handleSettingChange('enableWebXR', !settings.enableWebXR)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    settings.enableWebXR ? 'bg-blue-500' : 'bg-gray-600'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      settings.enableWebXR ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>

              {/* Mode debug */}
              <div className="flex items-center justify-between">
                <div>
                  <div className="font-medium">Mode debug</div>
                  <div className="text-sm text-white/70">Afficher les informations de debug</div>
                </div>
                <button
                  onClick={() => handleSettingChange('debug', !settings.debug)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    settings.debug ? 'bg-blue-500' : 'bg-gray-600'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      settings.debug ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>
            </div>
          </section>

          {/* Paramètres audio et vibration */}
          <section className="bg-white/10 backdrop-blur-sm rounded-2xl p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center space-x-2">
              <Volume2 className="text-green-400" />
              <span>Audio & Vibration</span>
            </h2>
            
            <div className="space-y-4">
              {/* Son */}
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  {settings.soundEnabled ? <Volume2 size={20} /> : <VolumeX size={20} />}
                  <div>
                    <div className="font-medium">Son</div>
                    <div className="text-sm text-white/70">Sons de feedback</div>
                  </div>
                </div>
                <button
                  onClick={() => handleSettingChange('soundEnabled', !settings.soundEnabled)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    settings.soundEnabled ? 'bg-green-500' : 'bg-gray-600'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      settings.soundEnabled ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>

              {/* Vibration */}
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <Vibrate size={20} />
                  <div>
                    <div className="font-medium">Vibration</div>
                    <div className="text-sm text-white/70">Retour haptique</div>
                  </div>
                </div>
                <button
                  onClick={() => handleSettingChange('vibrationEnabled', !settings.vibrationEnabled)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    settings.vibrationEnabled ? 'bg-purple-500' : 'bg-gray-600'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      settings.vibrationEnabled ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>
            </div>
          </section>

          {/* Statistiques */}
          <section className="bg-white/10 backdrop-blur-sm rounded-2xl p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center space-x-2">
              <Eye className="text-yellow-400" />
              <span>Statistiques</span>
            </h2>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-400">{stats.totalScans}</div>
                <div className="text-sm text-white/70">Scans totaux</div>
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
          </section>

          {/* Gestion des données */}
          <section className="bg-white/10 backdrop-blur-sm rounded-2xl p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center space-x-2">
              <Info className="text-cyan-400" />
              <span>Gestion des données</span>
            </h2>
            
            <div className="space-y-4">
              {/* Export */}
              <button
                onClick={handleExportData}
                className="w-full flex items-center justify-center space-x-2 p-3 bg-blue-500/20 hover:bg-blue-500/30 rounded-lg transition-colors"
              >
                <Download size={20} />
                <span>Exporter les données</span>
              </button>

              {/* Import */}
              <label className="w-full flex items-center justify-center space-x-2 p-3 bg-green-500/20 hover:bg-green-500/30 rounded-lg transition-colors cursor-pointer">
                <Upload size={20} />
                <span>Importer les données</span>
                <input
                  type="file"
                  accept=".json"
                  onChange={handleImportData}
                  className="hidden"
                />
              </label>

              {/* Effacer l'historique */}
              <button
                onClick={() => setShowConfirmClear(true)}
                className="w-full flex items-center justify-center space-x-2 p-3 bg-red-500/20 hover:bg-red-500/30 rounded-lg transition-colors"
              >
                <Trash2 size={20} />
                <span>Effacer l'historique ({history.length} éléments)</span>
              </button>
            </div>
          </section>

          {/* Informations sur l'application */}
          <section className="bg-white/10 backdrop-blur-sm rounded-2xl p-6">
            <h2 className="text-xl font-semibold mb-4">À propos</h2>
            <div className="space-y-2 text-sm text-white/70">
              <div>ARBase v2.0.0</div>
              <div>Plateforme de réalité augmentée</div>
              <div>© 2024 ARBase Team</div>
            </div>
          </section>
        </motion.div>
      </main>

      {/* Modal de confirmation */}
      {showConfirmClear && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <motion.div
            className="bg-gray-900 rounded-2xl p-6 max-w-sm mx-4"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
          >
            <h3 className="text-lg font-semibold mb-4">Confirmer la suppression</h3>
            <p className="text-white/70 mb-6">
              Êtes-vous sûr de vouloir effacer tout l'historique ? Cette action est irréversible.
            </p>
            <div className="flex space-x-3">
              <button
                onClick={() => setShowConfirmClear(false)}
                className="flex-1 px-4 py-2 bg-gray-600 hover:bg-gray-700 rounded-lg transition-colors"
              >
                Annuler
              </button>
              <button
                onClick={handleClearHistory}
                className="flex-1 px-4 py-2 bg-red-500 hover:bg-red-600 rounded-lg transition-colors"
              >
                Effacer
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
};