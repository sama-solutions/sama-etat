import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  IconButton,
  Menu,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  Chip,
  Avatar,
  LinearProgress,
  Paper,
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  MoreVert as MoreVertIcon,
  Delete as DeleteIcon,
  Download as DownloadIcon,
  Edit as EditIcon,
  Search as SearchIcon,
  FilterList as FilterIcon,
  Image as ImageIcon,
  VideoFile as VideoIcon,
  AudioFile as AudioIcon,
  InsertDriveFile as FileIcon,
} from '@mui/icons-material';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import toast from 'react-hot-toast';

const Assets = () => {
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploadDialogOpen, setUploadDialogOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [typeFilter, setTypeFilter] = useState('all');
  const [anchorEl, setAnchorEl] = useState(null);
  const [selectedAsset, setSelectedAsset] = useState(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);

  useEffect(() => {
    fetchAssets();
  }, []);

  const fetchAssets = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/assets');
      setAssets(response.data.assets || []);
    } catch (error) {
      console.error('Erreur lors du chargement des assets:', error);
      toast.error('Erreur lors du chargement des assets');
      // Données de démonstration
      setAssets([
        {
          _id: '1',
          filename: 'logo-3d.glb',
          originalName: 'logo-3d.glb',
          type: 'model3d',
          size: 2048576,
          url: '/uploads/logo-3d.glb',
          createdAt: new Date().toISOString(),
          usageCount: 5
        },
        {
          _id: '2',
          filename: 'background.jpg',
          originalName: 'background.jpg',
          type: 'image',
          size: 1024768,
          url: '/uploads/background.jpg',
          createdAt: new Date().toISOString(),
          usageCount: 12
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const onDrop = async (acceptedFiles) => {
    for (const file of acceptedFiles) {
      try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('category', 'general');

        const response = await axios.post('/api/assets/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        toast.success(`${file.name} uploadé avec succès`);
      } catch (error) {
        console.error('Erreur lors de l\'upload:', error);
        toast.error(`Erreur lors de l'upload de ${file.name}`);
      }
    }
    
    fetchAssets();
    setUploadDialogOpen(false);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.webp', '.gif'],
      'video/*': ['.mp4', '.webm', '.ogg'],
      'audio/*': ['.mp3', '.wav', '.ogg'],
      'model/*': ['.glb', '.gltf', '.obj', '.fbx']
    },
    multiple: true
  });

  const handleMenuOpen = (event, asset) => {
    setAnchorEl(event.currentTarget);
    setSelectedAsset(asset);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setSelectedAsset(null);
  };

  const handleDelete = async () => {
    try {
      await axios.delete(`/api/assets/${selectedAsset._id}`);
      toast.success('Asset supprimé avec succès');
      fetchAssets();
    } catch (error) {
      toast.error('Erreur lors de la suppression');
    }
    setDeleteDialogOpen(false);
    setSelectedAsset(null);
  };

  const handleDownload = () => {
    window.open(selectedAsset.url, '_blank');
    handleMenuClose();
  };

  const getFileIcon = (type) => {
    switch (type) {
      case 'image': return <ImageIcon />;
      case 'video': return <VideoIcon />;
      case 'audio': return <AudioIcon />;
      case 'model3d': return <FileIcon />;
      default: return <FileIcon />;
    }
  };

  const getFileTypeColor = (type) => {
    switch (type) {
      case 'image': return '#4caf50';
      case 'video': return '#2196f3';
      case 'audio': return '#ff9800';
      case 'model3d': return '#9c27b0';
      default: return '#757575';
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const filteredAssets = assets.filter(asset => {
    const matchesSearch = asset.originalName.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType = typeFilter === 'all' || asset.type === typeFilter;
    return matchesSearch && matchesType;
  });

  if (loading) {
    return (
      <Box>
        <Typography variant="h4" sx={{ mb: 3 }}>
          Assets
        </Typography>
        <LinearProgress />
      </Box>
    );
  }

  return (
    <Box>
      {/* En-tête */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
            Assets
          </Typography>
          <Typography variant="body1" sx={{ color: 'text.secondary' }}>
            Gérez vos fichiers multimédias et modèles 3D
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<UploadIcon />}
          onClick={() => setUploadDialogOpen(true)}
          sx={{ px: 3, py: 1.5 }}
        >
          Uploader des fichiers
        </Button>
      </Box>

      {/* Filtres et recherche */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                placeholder="Rechercher un asset..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                InputProps={{
                  startAdornment: <SearchIcon sx={{ color: 'text.secondary', mr: 1 }} />
                }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <FormControl fullWidth>
                <InputLabel>Type de fichier</InputLabel>
                <Select
                  value={typeFilter}
                  label="Type de fichier"
                  onChange={(e) => setTypeFilter(e.target.value)}
                >
                  <MenuItem value="all">Tous les types</MenuItem>
                  <MenuItem value="image">Images</MenuItem>
                  <MenuItem value="video">Vidéos</MenuItem>
                  <MenuItem value="audio">Audio</MenuItem>
                  <MenuItem value="model3d">Modèles 3D</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={2}>
              <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                {filteredAssets.length} asset(s)
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Liste des assets */}
      {filteredAssets.length === 0 ? (
        <Card>
          <CardContent sx={{ textAlign: 'center', py: 8 }}>
            <UploadIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
            <Typography variant="h6" sx={{ mb: 2 }}>
              {searchTerm || typeFilter !== 'all' ? 'Aucun asset trouvé' : 'Aucun asset uploadé'}
            </Typography>
            <Typography variant="body2" sx={{ color: 'text.secondary', mb: 3 }}>
              {searchTerm || typeFilter !== 'all'
                ? 'Aucun asset ne correspond à vos critères de recherche.'
                : 'Uploadez vos premiers fichiers pour commencer.'
              }
            </Typography>
            <Button
              variant="contained"
              startIcon={<UploadIcon />}
              onClick={() => setUploadDialogOpen(true)}
            >
              Uploader des fichiers
            </Button>
          </CardContent>
        </Card>
      ) : (
        <Grid container spacing={3}>
          {filteredAssets.map((asset) => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={asset._id}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardContent sx={{ flexGrow: 1 }}>
                  {/* En-tête de la carte */}
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                    <Avatar 
                      sx={{ 
                        backgroundColor: getFileTypeColor(asset.type),
                        width: 48,
                        height: 48
                      }}
                    >
                      {getFileIcon(asset.type)}
                    </Avatar>
                    <IconButton
                      size="small"
                      onClick={(e) => handleMenuOpen(e, asset)}
                    >
                      <MoreVertIcon />
                    </IconButton>
                  </Box>

                  {/* Informations du fichier */}
                  <Typography 
                    variant="subtitle1" 
                    sx={{ 
                      fontWeight: 600, 
                      mb: 1,
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      whiteSpace: 'nowrap'
                    }}
                    title={asset.originalName}
                  >
                    {asset.originalName}
                  </Typography>

                  <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                    <Chip
                      label={asset.type}
                      size="small"
                      sx={{ 
                        backgroundColor: getFileTypeColor(asset.type),
                        color: 'white',
                        textTransform: 'uppercase',
                        fontSize: '0.7rem'
                      }}
                    />
                  </Box>

                  <Typography variant="body2" sx={{ color: 'text.secondary', mb: 1 }}>
                    Taille: {formatFileSize(asset.size)}
                  </Typography>

                  <Typography variant="body2" sx={{ color: 'text.secondary', mb: 1 }}>
                    Utilisé: {asset.usageCount || 0} fois
                  </Typography>

                  <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                    Créé: {new Date(asset.createdAt).toLocaleDateString()}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Menu contextuel */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={handleDownload}>
          <DownloadIcon sx={{ mr: 1 }} />
          Télécharger
        </MenuItem>
        <MenuItem onClick={() => setDeleteDialogOpen(true)}>
          <DeleteIcon sx={{ mr: 1 }} />
          Supprimer
        </MenuItem>
      </Menu>

      {/* Dialog d'upload */}
      <Dialog
        open={uploadDialogOpen}
        onClose={() => setUploadDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Uploader des fichiers
        </DialogTitle>
        <DialogContent>
          <Paper
            {...getRootProps()}
            sx={{
              p: 4,
              textAlign: 'center',
              border: '2px dashed',
              borderColor: isDragActive ? 'primary.main' : 'grey.300',
              backgroundColor: isDragActive ? 'action.hover' : 'background.paper',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              mt: 2
            }}
          >
            <input {...getInputProps()} />
            <UploadIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
            <Typography variant="h6" sx={{ mb: 1 }}>
              {isDragActive ? 'Déposez les fichiers ici' : 'Glissez-déposez vos fichiers'}
            </Typography>
            <Typography variant="body2" sx={{ color: 'text.secondary', mb: 2 }}>
              ou cliquez pour sélectionner des fichiers
            </Typography>
            <Typography variant="caption" sx={{ color: 'text.secondary' }}>
              Formats supportés: Images (JPG, PNG, WEBP), Vidéos (MP4, WEBM), Audio (MP3, WAV), Modèles 3D (GLB, GLTF)
            </Typography>
          </Paper>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setUploadDialogOpen(false)}>
            Annuler
          </Button>
        </DialogActions>
      </Dialog>

      {/* Dialog de confirmation de suppression */}
      <Dialog
        open={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
      >
        <DialogTitle>
          Supprimer l'asset
        </DialogTitle>
        <DialogContent>
          <Typography>
            Êtes-vous sûr de vouloir supprimer "{selectedAsset?.originalName}" ?
            Cette action est irréversible.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>
            Annuler
          </Button>
          <Button onClick={handleDelete} color="error" variant="contained">
            Supprimer
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Assets;