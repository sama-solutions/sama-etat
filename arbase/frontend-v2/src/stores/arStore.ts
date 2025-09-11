/**
 * ARStore - Gestion d'état global pour l'application AR
 * Utilise Zustand pour une gestion d'état simple et performante
 */

import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { ARExperience } from '../../ar-engine-v2';

interface ARSettings {
  scanInterval: number;
  minConfidence: number;
  maxDistance: number;
  enableWebXR: boolean;
  debug: boolean;
  autoStart: boolean;
  soundEnabled: boolean;
  vibrationEnabled: boolean;
}

interface ARStats {
  totalScans: number;
  successfulDetections: number;
  totalExperiences: number;
  averageSessionTime: number;
  lastScanDate: Date | null;
}

interface ARHistory {
  id: string;
  experience: ARExperience;
  timestamp: Date;
  duration: number;
  interactions: number;
}

interface ARState {
  // État actuel
  currentExperience: ARExperience | null;
  isScanning: boolean;
  isInitialized: boolean;
  
  // Paramètres
  settings: ARSettings;
  
  // Statistiques
  stats: ARStats;
  
  // Historique
  history: ARHistory[];
  
  // Actions
  setCurrentExperience: (experience: ARExperience | null) => void;
  setIsScanning: (scanning: boolean) => void;
  setIsInitialized: (initialized: boolean) => void;
  updateSettings: (newSettings: Partial<ARSettings>) => void;
  updateStats: (newStats: Partial<ARStats>) => void;
  addToHistory: (experience: ARExperience, duration?: number, interactions?: number) => void;
  clearHistory: () => void;
  getExperienceFromHistory: (id: string) => ARHistory | undefined;
  
  // Utilitaires
  resetState: () => void;
  exportData: () => string;
  importData: (data: string) => void;
}

const defaultSettings: ARSettings = {
  scanInterval: 100,
  minConfidence: 0.8,
  maxDistance: 10,
  enableWebXR: true,
  debug: false,
  autoStart: true,
  soundEnabled: true,
  vibrationEnabled: true
};

const defaultStats: ARStats = {
  totalScans: 0,
  successfulDetections: 0,
  totalExperiences: 0,
  averageSessionTime: 0,
  lastScanDate: null
};

export const useARStore = create<ARState>()(
  persist(
    (set, get) => ({
      // État initial
      currentExperience: null,
      isScanning: false,
      isInitialized: false,
      settings: defaultSettings,
      stats: defaultStats,
      history: [],

      // Actions
      setCurrentExperience: (experience) => {
        set({ currentExperience: experience });
        
        if (experience) {
          // Mettre à jour les statistiques
          const currentStats = get().stats;
          set({
            stats: {
              ...currentStats,
              successfulDetections: currentStats.successfulDetections + 1,
              lastScanDate: new Date()
            }
          });
        }
      },

      setIsScanning: (scanning) => {
        set({ isScanning: scanning });
        
        if (scanning) {
          // Incrémenter le compteur de scans
          const currentStats = get().stats;
          set({
            stats: {
              ...currentStats,
              totalScans: currentStats.totalScans + 1
            }
          });
        }
      },

      setIsInitialized: (initialized) => {
        set({ isInitialized: initialized });
      },

      updateSettings: (newSettings) => {
        set((state) => ({
          settings: { ...state.settings, ...newSettings }
        }));
      },

      updateStats: (newStats) => {
        set((state) => ({
          stats: { ...state.stats, ...newStats }
        }));
      },

      addToHistory: (experience, duration = 0, interactions = 0) => {
        const historyEntry: ARHistory = {
          id: `${experience.id}_${Date.now()}`,
          experience,
          timestamp: new Date(),
          duration,
          interactions
        };

        set((state) => {
          const newHistory = [historyEntry, ...state.history].slice(0, 50); // Garder seulement les 50 dernières
          
          // Mettre à jour les statistiques
          const totalExperiences = newHistory.length;
          const averageSessionTime = newHistory.reduce((acc, entry) => acc + entry.duration, 0) / totalExperiences;
          
          return {
            history: newHistory,
            stats: {
              ...state.stats,
              totalExperiences,
              averageSessionTime
            }
          };
        });
      },

      clearHistory: () => {
        set({ history: [] });
      },

      getExperienceFromHistory: (id) => {
        return get().history.find(entry => entry.experience.id === id);
      },

      resetState: () => {
        set({
          currentExperience: null,
          isScanning: false,
          isInitialized: false,
          settings: defaultSettings,
          stats: defaultStats,
          history: []
        });
      },

      exportData: () => {
        const state = get();
        const exportData = {
          settings: state.settings,
          stats: state.stats,
          history: state.history,
          exportDate: new Date().toISOString()
        };
        return JSON.stringify(exportData, null, 2);
      },

      importData: (data) => {
        try {
          const importedData = JSON.parse(data);
          
          set({
            settings: { ...defaultSettings, ...importedData.settings },
            stats: { ...defaultStats, ...importedData.stats },
            history: importedData.history || []
          });
        } catch (error) {
          console.error('Erreur lors de l\'importation des données:', error);
          throw new Error('Format de données invalide');
        }
      }
    }),
    {
      name: 'arbase-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        settings: state.settings,
        stats: state.stats,
        history: state.history
      })
    }
  )
);

// Hooks utilitaires
export const useARSettings = () => {
  const settings = useARStore(state => state.settings);
  const updateSettings = useARStore(state => state.updateSettings);
  return { settings, updateSettings };
};

export const useARStats = () => {
  const stats = useARStore(state => state.stats);
  const updateStats = useARStore(state => state.updateStats);
  return { stats, updateStats };
};

export const useARHistory = () => {
  const history = useARStore(state => state.history);
  const addToHistory = useARStore(state => state.addToHistory);
  const clearHistory = useARStore(state => state.clearHistory);
  const getExperienceFromHistory = useARStore(state => state.getExperienceFromHistory);
  
  return { 
    history, 
    addToHistory, 
    clearHistory, 
    getExperienceFromHistory 
  };
};

// Sélecteurs optimisés
export const useCurrentExperience = () => useARStore(state => state.currentExperience);
export const useIsScanning = () => useARStore(state => state.isScanning);
export const useIsInitialized = () => useARStore(state => state.isInitialized);