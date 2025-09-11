/**
 * ExperiencePage - Page pour afficher une expérience AR spécifique
 */

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Play, Share2, Eye, MousePointer, Clock } from 'lucide-react';
import { useARStore } from '../stores/arStore';

interface Experience {
  id: string;
  title: string;
  description?: string;
  category: string;
  views: number;
  scans: number;
  interactions: number;
  createdAt: string;
  content: any[];
  settings: any;
}

export const ExperiencePage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [experience, setExperience] = useState<Experience | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const { setCurrentExperience } = useARStore();

  useEffect(() => {
    if (id) {
      fetchExperience(id);
    }
  }, [id]);

  const fetchExperience = async (experienceId: string) => {
    try {
      setLoading(true);
      const response = await fetch(`/api/experiences/${experienceId}`);
      
      if (!response.ok) {
        throw new Error('Expérience non trouvée');
      }
      
      const data = await response.json();
      setExperience(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur de chargement');
    } finally {
      setLoading(false);
    }
  };

  const handleStartExperience = () => {
    if (experience) {
      setCurrentExperience(experience);
      navigate('/scanner');
    }
  };

  const handleShare = async () => {
    const shareData = {
      title: experience?.title || 'Expérience AR',
      text: experience?.description || 'Découvrez cette expérience de réalité augmentée',
      url: window.location.href
    };

    if (navigator.share) {
      try {
        await navigator.share(shareData);
      } catch (error) {
        // Fallback
        navigator.clipboard.writeText(shareData.url);
      }
    } else {
      navigator.clipboard.writeText(shareData.url);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <motion.div
          className="text-center text-white"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-4 animate-spin" />
          <p>Chargement de l'expérience...</p>
        </motion.div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <motion.div
          className="text-center text-white p-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1 className="text-2xl font-bold mb-4 text-red-400">Erreur</h1>
          <p className="text-white/70 mb-6">{error}</p>
          <button
            onClick={() => navigate('/')}
            className="px-6 py-3 bg-blue-500 hover:bg-blue-600 rounded-lg transition-colors"
          >
            Retour à l'accueil
          </button>
        </motion.div>
      </div>
    );
  }

  if (!experience) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <motion.div
          className="text-center text-white p-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1 className="text-2xl font-bold mb-4">Expérience non trouvée</h1>
          <p className="text-white/70 mb-6">Cette expérience n'existe pas ou n'est plus disponible.</p>
          <button
            onClick={() => navigate('/')}
            className="px-6 py-3 bg-blue-500 hover:bg-blue-600 rounded-lg transition-colors"
          >
            Retour à l'accueil
          </button>
        </motion.div>
      </div>
    );
  }

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
          
          <h1 className="text-xl font-bold">Expérience AR</h1>
          
          <button
            onClick={handleShare}
            className="p-3 bg-white/10 backdrop-blur-sm rounded-full hover:bg-white/20 transition-colors"
          >
            <Share2 size={20} />
          </button>
        </div>
      </header>

      {/* Contenu principal */}
      <main className="container mx-auto px-6 pb-6">
        <motion.div
          className="max-w-4xl mx-auto"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          {/* Titre et description */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              {experience.title}
            </h1>
            {experience.description && (
              <p className="text-xl text-white/80 max-w-2xl mx-auto">
                {experience.description}
              </p>
            )}
          </div>

          {/* Statistiques */}
          <div className="grid grid-cols-3 gap-4 mb-8">
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 text-center">
              <Eye className="w-8 h-8 mx-auto mb-2 text-blue-400" />
              <div className="text-2xl font-bold">{experience.views}</div>
              <div className="text-sm text-white/70">Vues</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 text-center">
              <Play className="w-8 h-8 mx-auto mb-2 text-green-400" />
              <div className="text-2xl font-bold">{experience.scans}</div>
              <div className="text-sm text-white/70">Scans</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 text-center">
              <MousePointer className="w-8 h-8 mx-auto mb-2 text-purple-400" />
              <div className="text-2xl font-bold">{experience.interactions}</div>
              <div className="text-sm text-white/70">Interactions</div>
            </div>
          </div>

          {/* Informations sur le contenu */}
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 mb-8">
            <h3 className="text-xl font-semibold mb-4">Contenu de l'expérience</h3>
            <div className="grid gap-4">
              {experience.content.map((item, index) => (
                <div key={index} className="flex items-center space-x-3 p-3 bg-white/5 rounded-lg">
                  <div className="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center">
                    <span className="text-blue-400 font-semibold">{index + 1}</span>
                  </div>
                  <div>
                    <div className="font-medium capitalize">{item.type}</div>
                    <div className="text-sm text-white/70">
                      {item.type === 'text' && item.data?.text}
                      {item.type === 'model' && 'Modèle 3D'}
                      {item.type === 'image' && 'Image'}
                      {item.type === 'video' && 'Vidéo'}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Métadonnées */}
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 mb-8">
            <h3 className="text-xl font-semibold mb-4">Informations</h3>
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <div className="text-sm text-white/70">Catégorie</div>
                <div className="font-medium capitalize">{experience.category}</div>
              </div>
              <div>
                <div className="text-sm text-white/70">Créé le</div>
                <div className="font-medium">
                  {new Date(experience.createdAt).toLocaleDateString('fr-FR')}
                </div>
              </div>
            </div>
          </div>

          {/* Bouton d'action principal */}
          <div className="text-center">
            <motion.button
              onClick={handleStartExperience}
              className="group relative px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full font-semibold text-lg hover:from-blue-600 hover:to-purple-600 transition-all duration-300"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <span className="flex items-center space-x-2">
                <Play size={20} />
                <span>Lancer l'Expérience AR</span>
              </span>
            </motion.button>
            
            <p className="text-sm text-white/60 mt-4">
              Vous serez redirigé vers le scanner AR
            </p>
          </div>
        </motion.div>
      </main>
    </div>
  );
};