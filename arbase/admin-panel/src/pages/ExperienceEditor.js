import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  IconButton,
  Stepper,
  Step,
  StepLabel,
  Paper,
  Divider,
  Switch,
  FormControlLabel,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Save as SaveIcon,
  Publish as PublishIcon,
  Preview as PreviewIcon,
  Add as AddIcon,
  Delete as DeleteIcon,
  CloudUpload as UploadIcon,
} from '@mui/icons-material';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import toast from 'react-hot-toast';

const steps = [
  'Informations de base',
  'Image de référence',
  'Contenu AR',
  'Paramètres',
  'Publication'
];

const ExperienceEditor = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEditing = Boolean(id);
  
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [experience, setExperience] = useState({
    title: '',
    description: '',
    category: 'business_card',
    tags: [],
    referenceImage: null,
    arContent: [],
    settings: {
      trackingMode: 'image',
      maxDistance: 10,
      autoStart: true,
      showInstructions: true,
      backgroundColor: 'transparent'
    },
    status: 'draft',
    isPublic: false
  });

  useEffect(() => {
    if (isEditing) {
      fetchExperience();
    }
  }, [id, isEditing]);

  const fetchExperience = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`/api/experiences/${id}`);
      setExperience(response.data.experience);
    } catch (error) {
      console.error('Erreur lors du chargement de l\'expérience:', error);
      toast.error('Erreur lors du chargement de l\'expérience');
      navigate('/experiences');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field, value) => {
    setExperience(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSettingsChange = (field, value) => {
    setExperience(prev => ({
      ...prev,
      settings: {
        ...prev.settings,
        [field]: value
      }
    }));
  };

  const handleSave = async (publish = false) => {
    try {
      setLoading(true);
      
      const data = {
        ...experience,
        status: publish ? 'published' : experience.status
      };

      let response;
      if (isEditing) {
        response = await axios.put(`/api/experiences/${id}`, data);
      } else {
        response = await axios.post('/api/experiences', data);
      }

      toast.success(publish ? 'Expérience publiée avec succès' : 'Expérience sauvegardée');
      
      if (!isEditing) {
        navigate(`/experiences/${response.data.experience._id}/edit`);
      }
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error);
      toast.error('Erreur lors de la sauvegarde');
    } finally {
      setLoading(false);
    }
  };

  const onDrop = async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    try {
      setLoading(true);
      const formData = new FormData();
      formData.append('file', file);
      formData.append('category', 'reference');

      const response = await axios.post('/api/assets/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setExperience(prev => ({
        ...prev,
        referenceImage: {
          url: response.data.asset.url,
          filename: response.data.asset.filename,
          size: response.data.asset.size,
          mimetype: response.data.asset.mimetype
        }
      }));

      toast.success('Image de référence uploadée avec succès');
    } catch (error) {
      console.error('Erreur lors de l\'upload:', error);
      toast.error('Erreur lors de l\'upload de l\'image');
    } finally {
      setLoading(false);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.webp']
    },
    maxFiles: 1
  });

  const addARContent = () => {
    const newContent = {
      id: Date.now(),
      type: 'text',
      content: {
        text: 'Nouveau contenu',
        title: '',
        description: ''
      },
      position: { x: 0, y: 0, z: 0 },
      rotation: { x: 0, y: 0, z: 0 },
      scale: { x: 1, y: 1, z: 1 },
      animation: {
        enabled: false,
        type: 'rotation',
        duration: 2000,
        loop: true
      },
      interaction: {
        enabled: false,
        type: 'click',
        action: 'show_info'
      }
    };

    setExperience(prev => ({
      ...prev,
      arContent: [...prev.arContent, newContent]
    }));
  };

  const removeARContent = (index) => {
    setExperience(prev => ({
      ...prev,
      arContent: prev.arContent.filter((_, i) => i !== index)
    }));
  };

  const updateARContent = (index, field, value) => {
    setExperience(prev => ({
      ...prev,
      arContent: prev.arContent.map((content, i) => 
        i === index ? { ...content, [field]: value } : content
      )
    }));
  };

  const renderStepContent = () => {
    switch (activeStep) {
      case 0:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Titre de l'expérience"
                value={experience.title}
                onChange={(e) => handleInputChange('title', e.target.value)}
                required
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={4}
                label="Description"
                value={experience.description}
                onChange={(e) => handleInputChange('description', e.target.value)}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Catégorie</InputLabel>
                <Select
                  value={experience.category}
                  label="Catégorie"
                  onChange={(e) => handleInputChange('category', e.target.value)}
                >
                  <MenuItem value="business_card">Carte de visite</MenuItem>
                  <MenuItem value="poster">Affiche</MenuItem>
                  <MenuItem value="product">Produit</MenuItem>
                  <MenuItem value="artwork">Œuvre d'art</MenuItem>
                  <MenuItem value="other">Autre</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Tags (séparés par des virgules)"
                value={experience.tags.join(', ')}
                onChange={(e) => handleInputChange('tags', e.target.value.split(',').map(tag => tag.trim()))}
                helperText="Ex: marketing, produit, innovation"
              />
            </Grid>
          </Grid>
        );

      case 1:
        return (
          <Box>
            <Typography variant="h6" sx={{ mb: 3 }}>
              Image de référence
            </Typography>
            <Typography variant="body2" sx={{ mb: 3, color: 'text.secondary' }}>
              Cette image sera utilisée pour détecter et tracker l'objet en réalité augmentée.
            </Typography>
            
            {experience.referenceImage ? (
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <img
                      src={experience.referenceImage.url}
                      alt="Image de référence"
                      style={{
                        width: 100,
                        height: 100,
                        objectFit: 'cover',
                        borderRadius: 8
                      }}
                    />
                    <Box>
                      <Typography variant="subtitle1">
                        {experience.referenceImage.filename}
                      </Typography>
                      <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                        {(experience.referenceImage.size / 1024 / 1024).toFixed(2)} MB
                      </Typography>
                    </Box>
                    <Button
                      variant="outlined"
                      color="error"
                      onClick={() => handleInputChange('referenceImage', null)}
                    >
                      Supprimer
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            ) : (
              <Paper
                {...getRootProps()}
                sx={{
                  p: 4,
                  textAlign: 'center',
                  border: '2px dashed',
                  borderColor: isDragActive ? 'primary.main' : 'grey.300',
                  backgroundColor: isDragActive ? 'action.hover' : 'background.paper',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease'
                }}
              >
                <input {...getInputProps()} />
                <UploadIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
                <Typography variant="h6" sx={{ mb: 1 }}>
                  {isDragActive ? 'Déposez l\'image ici' : 'Glissez-déposez une image'}
                </Typography>
                <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                  ou cliquez pour sélectionner un fichier
                </Typography>
                <Typography variant="caption" sx={{ display: 'block', mt: 2, color: 'text.secondary' }}>
                  Formats acceptés: JPG, PNG, WEBP (max 10MB)
                </Typography>
              </Paper>
            )}
          </Box>
        );

      case 2:
        return (
          <Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
              <Typography variant="h6">
                Contenu AR
              </Typography>
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={addARContent}
              >
                Ajouter du contenu
              </Button>
            </Box>

            {experience.arContent.length === 0 ? (
              <Paper sx={{ p: 4, textAlign: 'center' }}>
                <Typography variant="body1" sx={{ mb: 2 }}>
                  Aucun contenu AR ajouté
                </Typography>
                <Typography variant="body2" sx={{ color: 'text.secondary', mb: 3 }}>
                  Ajoutez du contenu 3D, du texte, des images ou des vidéos qui apparaîtront en réalité augmentée.
                </Typography>
                <Button
                  variant="outlined"
                  startIcon={<AddIcon />}
                  onClick={addARContent}
                >
                  Ajouter votre premier contenu
                </Button>
              </Paper>
            ) : (
              <Grid container spacing={2}>
                {experience.arContent.map((content, index) => (
                  <Grid item xs={12} key={content.id}>
                    <Card>
                      <CardContent>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                          <Typography variant="subtitle1">
                            Contenu {index + 1}
                          </Typography>
                          <IconButton
                            color="error"
                            onClick={() => removeARContent(index)}
                          >
                            <DeleteIcon />
                          </IconButton>
                        </Box>
                        
                        <Grid container spacing={2}>
                          <Grid item xs={12} md={6}>
                            <FormControl fullWidth>
                              <InputLabel>Type de contenu</InputLabel>
                              <Select
                                value={content.type}
                                label="Type de contenu"
                                onChange={(e) => updateARContent(index, 'type', e.target.value)}
                              >
                                <MenuItem value="text">Texte</MenuItem>
                                <MenuItem value="model3d">Modèle 3D</MenuItem>
                                <MenuItem value="image">Image</MenuItem>
                                <MenuItem value="video">Vidéo</MenuItem>
                                <MenuItem value="link">Lien</MenuItem>
                              </Select>
                            </FormControl>
                          </Grid>
                          
                          {content.type === 'text' && (
                            <Grid item xs={12} md={6}>
                              <TextField
                                fullWidth
                                label="Texte à afficher"
                                value={content.content.text}
                                onChange={(e) => updateARContent(index, 'content', {
                                  ...content.content,
                                  text: e.target.value
                                })}
                              />
                            </Grid>
                          )}
                        </Grid>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            )}
          </Box>
        );

      case 3:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Typography variant="h6" sx={{ mb: 2 }}>
                Paramètres de tracking
              </Typography>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Mode de tracking</InputLabel>
                <Select
                  value={experience.settings.trackingMode}
                  label="Mode de tracking"
                  onChange={(e) => handleSettingsChange('trackingMode', e.target.value)}
                >
                  <MenuItem value="image">Reconnaissance d'image</MenuItem>
                  <MenuItem value="marker">Marqueur AR</MenuItem>
                  <MenuItem value="markerless">Sans marqueur</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                type="number"
                label="Distance maximale (mètres)"
                value={experience.settings.maxDistance}
                onChange={(e) => handleSettingsChange('maxDistance', Number(e.target.value))}
              />
            </Grid>

            <Grid item xs={12}>
              <FormControlLabel
                control={
                  <Switch
                    checked={experience.settings.autoStart}
                    onChange={(e) => handleSettingsChange('autoStart', e.target.checked)}
                  />
                }
                label="Démarrage automatique"
              />
            </Grid>

            <Grid item xs={12}>
              <FormControlLabel
                control={
                  <Switch
                    checked={experience.settings.showInstructions}
                    onChange={(e) => handleSettingsChange('showInstructions', e.target.checked)}
                  />
                }
                label="Afficher les instructions"
              />
            </Grid>
          </Grid>
        );

      case 4:
        return (
          <Box>
            <Typography variant="h6" sx={{ mb: 3 }}>
              Publication
            </Typography>
            
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={experience.isPublic}
                      onChange={(e) => handleInputChange('isPublic', e.target.checked)}
                    />
                  }
                  label="Rendre l'expérience publique"
                />
                <Typography variant="body2" sx={{ color: 'text.secondary', mt: 1 }}>
                  Les expériences publiques peuvent être découvertes par d'autres utilisateurs.
                </Typography>
              </Grid>

              <Grid item xs={12}>
                <Paper sx={{ p: 3, backgroundColor: 'background.default' }}>
                  <Typography variant="subtitle1" sx={{ mb: 2 }}>
                    Résumé de l'expérience
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    <strong>Titre:</strong> {experience.title || 'Non défini'}
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    <strong>Catégorie:</strong> {experience.category}
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    <strong>Image de référence:</strong> {experience.referenceImage ? 'Uploadée' : 'Non définie'}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Contenu AR:</strong> {experience.arContent.length} élément(s)
                  </Typography>
                </Paper>
              </Grid>
            </Grid>
          </Box>
        );

      default:
        return null;
    }
  };

  return (
    <Box>
      {/* En-tête */}
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 4 }}>
        <IconButton onClick={() => navigate('/experiences')} sx={{ mr: 2 }}>
          <ArrowBackIcon />
        </IconButton>
        <Box sx={{ flexGrow: 1 }}>
          <Typography variant="h4" sx={{ fontWeight: 700 }}>
            {isEditing ? 'Modifier l\'expérience' : 'Nouvelle expérience'}
          </Typography>
          <Typography variant="body1" sx={{ color: 'text.secondary' }}>
            {isEditing ? experience.title : 'Créez une nouvelle expérience de réalité augmentée'}
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="outlined"
            startIcon={<SaveIcon />}
            onClick={() => handleSave(false)}
            disabled={loading}
          >
            Sauvegarder
          </Button>
          <Button
            variant="contained"
            startIcon={<PublishIcon />}
            onClick={() => handleSave(true)}
            disabled={loading || !experience.title || !experience.referenceImage}
          >
            Publier
          </Button>
        </Box>
      </Box>

      {/* Stepper */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Stepper activeStep={activeStep} alternativeLabel>
            {steps.map((label) => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>
        </CardContent>
      </Card>

      {/* Contenu de l'étape */}
      <Card>
        <CardContent sx={{ p: 4 }}>
          {renderStepContent()}
        </CardContent>
        
        <Divider />
        
        <Box sx={{ p: 3, display: 'flex', justifyContent: 'space-between' }}>
          <Button
            disabled={activeStep === 0}
            onClick={() => setActiveStep(prev => prev - 1)}
          >
            Précédent
          </Button>
          <Button
            variant="contained"
            onClick={() => setActiveStep(prev => prev + 1)}
            disabled={activeStep === steps.length - 1}
          >
            Suivant
          </Button>
        </Box>
      </Card>
    </Box>
  );
};

export default ExperienceEditor;