import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  Chip,
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
  Avatar,
  Tooltip,
  LinearProgress,
} from '@mui/material';
import {
  Add as AddIcon,
  MoreVert as MoreVertIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  FileCopy as CopyIcon,
  Search as SearchIcon,
  FilterList as FilterIcon,
} from '@mui/icons-material';
import axios from 'axios';
import toast from 'react-hot-toast';

const Experiences = () => {
  const navigate = useNavigate();
  const [experiences, setExperiences] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [anchorEl, setAnchorEl] = useState(null);
  const [selectedExperience, setSelectedExperience] = useState(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);

  useEffect(() => {
    fetchExperiences();
  }, []);

  const fetchExperiences = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/experiences');
      setExperiences(response.data.experiences || []);
    } catch (error) {
      console.error('Erreur lors du chargement des expériences:', error);
      toast.error('Erreur lors du chargement des expériences');
      // Données de démonstration en cas d'erreur
      setExperiences([
        {
          _id: '1',
          title: 'Carte de visite CEO',
          description: 'Carte de visite interactive avec informations de contact',
          status: 'published',
          category: 'business_card',
          stats: { scans: 45, views: 67, interactions: 23 },
          updatedAt: new Date().toISOString(),
          creator: { firstName: 'John', lastName: 'Doe' }
        },
        {
          _id: '2',
          title: 'Affiche produit X',
          description: 'Présentation interactive du nouveau produit',
          status: 'draft',
          category: 'poster',
          stats: { scans: 23, views: 34, interactions: 12 },
          updatedAt: new Date().toISOString(),
          creator: { firstName: 'Jane', lastName: 'Smith' }
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleMenuOpen = (event, experience) => {
    setAnchorEl(event.currentTarget);
    setSelectedExperience(experience);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setSelectedExperience(null);
  };

  const handleEdit = () => {
    navigate(`/experiences/${selectedExperience._id}/edit`);
    handleMenuClose();
  };

  const handleDuplicate = async () => {
    try {
      await axios.post(`/api/experiences/${selectedExperience._id}/duplicate`);
      toast.success('Expérience dupliquée avec succès');
      fetchExperiences();
    } catch (error) {
      toast.error('Erreur lors de la duplication');
    }
    handleMenuClose();
  };

  const handleDeleteClick = () => {
    setDeleteDialogOpen(true);
    handleMenuClose();
  };

  const handleDeleteConfirm = async () => {
    try {
      await axios.delete(`/api/experiences/${selectedExperience._id}`);
      toast.success('Expérience supprimée avec succès');
      fetchExperiences();
    } catch (error) {
      toast.error('Erreur lors de la suppression');
    }
    setDeleteDialogOpen(false);
    setSelectedExperience(null);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'published': return 'success';
      case 'draft': return 'warning';
      case 'archived': return 'default';
      default: return 'default';
    }
  };

  const getStatusLabel = (status) => {
    switch (status) {
      case 'published': return 'Publié';
      case 'draft': return 'Brouillon';
      case 'archived': return 'Archivé';
      default: return status;
    }
  };

  const getCategoryLabel = (category) => {
    switch (category) {
      case 'business_card': return 'Carte de visite';
      case 'poster': return 'Affiche';
      case 'product': return 'Produit';
      case 'artwork': return 'Œuvre d\'art';
      default: return 'Autre';
    }
  };

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'business_card': return '💼';
      case 'poster': return '📋';
      case 'product': return '📦';
      case 'artwork': return '🎨';
      default: return '📄';
    }
  };

  const filteredExperiences = experiences.filter(exp => {
    const matchesSearch = exp.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         exp.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || exp.status === statusFilter;
    const matchesCategory = categoryFilter === 'all' || exp.category === categoryFilter;
    
    return matchesSearch && matchesStatus && matchesCategory;
  });

  if (loading) {
    return (
      <Box>
        <Typography variant="h4" sx={{ mb: 3 }}>
          Expériences AR
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
            Expériences AR
          </Typography>
          <Typography variant="body1" sx={{ color: 'text.secondary' }}>
            Gérez vos expériences de réalité augmentée
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => navigate('/experiences/new')}
          sx={{ px: 3, py: 1.5 }}
        >
          Nouvelle expérience
        </Button>
      </Box>

      {/* Filtres et recherche */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                placeholder="Rechercher une expérience..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                InputProps={{
                  startAdornment: <SearchIcon sx={{ color: 'text.secondary', mr: 1 }} />
                }}
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <FormControl fullWidth>
                <InputLabel>Statut</InputLabel>
                <Select
                  value={statusFilter}
                  label="Statut"
                  onChange={(e) => setStatusFilter(e.target.value)}
                >
                  <MenuItem value="all">Tous les statuts</MenuItem>
                  <MenuItem value="published">Publié</MenuItem>
                  <MenuItem value="draft">Brouillon</MenuItem>
                  <MenuItem value="archived">Archivé</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={3}>
              <FormControl fullWidth>
                <InputLabel>Catégorie</InputLabel>
                <Select
                  value={categoryFilter}
                  label="Catégorie"
                  onChange={(e) => setCategoryFilter(e.target.value)}
                >
                  <MenuItem value="all">Toutes les catégories</MenuItem>
                  <MenuItem value="business_card">Carte de visite</MenuItem>
                  <MenuItem value="poster">Affiche</MenuItem>
                  <MenuItem value="product">Produit</MenuItem>
                  <MenuItem value="artwork">Œuvre d'art</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={2}>
              <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                {filteredExperiences.length} expérience(s)
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Liste des expériences */}
      {filteredExperiences.length === 0 ? (
        <Card>
          <CardContent sx={{ textAlign: 'center', py: 8 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>
              Aucune expérience trouvée
            </Typography>
            <Typography variant="body2" sx={{ color: 'text.secondary', mb: 3 }}>
              {searchTerm || statusFilter !== 'all' || categoryFilter !== 'all'
                ? 'Aucune expérience ne correspond à vos critères de recherche.'
                : 'Vous n\'avez pas encore créé d\'expérience AR.'
              }
            </Typography>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => navigate('/experiences/new')}
            >
              Créer votre première expérience
            </Button>
          </CardContent>
        </Card>
      ) : (
        <Grid container spacing={3}>
          {filteredExperiences.map((experience) => (
            <Grid item xs={12} md={6} lg={4} key={experience._id}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardContent sx={{ flexGrow: 1 }}>
                  {/* En-tête de la carte */}
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                    <Avatar sx={{ backgroundColor: 'primary.main', mr: 2 }}>
                      {getCategoryIcon(experience.category)}
                    </Avatar>
                    <Box sx={{ flexGrow: 1 }}>
                      <Typography variant="h6" sx={{ fontWeight: 600, mb: 0.5 }}>
                        {experience.title}
                      </Typography>
                      <Box sx={{ display: 'flex', gap: 1, mb: 1 }}>
                        <Chip
                          label={getStatusLabel(experience.status)}
                          color={getStatusColor(experience.status)}
                          size="small"
                        />
                        <Chip
                          label={getCategoryLabel(experience.category)}
                          variant="outlined"
                          size="small"
                        />
                      </Box>
                    </Box>
                    <IconButton
                      onClick={(e) => handleMenuOpen(e, experience)}
                      size="small"
                    >
                      <MoreVertIcon />
                    </IconButton>
                  </Box>

                  {/* Description */}
                  <Typography variant="body2" sx={{ color: 'text.secondary', mb: 3 }}>
                    {experience.description}
                  </Typography>

                  {/* Statistiques */}
                  <Grid container spacing={2}>
                    <Grid item xs={4}>
                      <Box sx={{ textAlign: 'center' }}>
                        <Typography variant="h6" sx={{ fontWeight: 600, color: 'primary.main' }}>
                          {experience.stats?.scans || 0}
                        </Typography>
                        <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                          Scans
                        </Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={4}>
                      <Box sx={{ textAlign: 'center' }}>
                        <Typography variant="h6" sx={{ fontWeight: 600, color: 'secondary.main' }}>
                          {experience.stats?.views || 0}
                        </Typography>
                        <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                          Vues
                        </Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={4}>
                      <Box sx={{ textAlign: 'center' }}>
                        <Typography variant="h6" sx={{ fontWeight: 600, color: 'success.main' }}>
                          {experience.stats?.interactions || 0}
                        </Typography>
                        <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                          Interactions
                        </Typography>
                      </Box>
                    </Grid>
                  </Grid>
                </CardContent>

                {/* Actions */}
                <Box sx={{ p: 2, pt: 0 }}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<EditIcon />}
                    onClick={() => navigate(`/experiences/${experience._id}/edit`)}
                  >
                    Modifier
                  </Button>
                </Box>
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
        <MenuItem onClick={handleEdit}>
          <EditIcon sx={{ mr: 1 }} />
          Modifier
        </MenuItem>
        <MenuItem onClick={handleDuplicate}>
          <CopyIcon sx={{ mr: 1 }} />
          Dupliquer
        </MenuItem>
        <MenuItem onClick={() => navigate(`/experiences/${selectedExperience?._id}`)}>
          <ViewIcon sx={{ mr: 1 }} />
          Voir les détails
        </MenuItem>
        <MenuItem onClick={handleDeleteClick} sx={{ color: 'error.main' }}>
          <DeleteIcon sx={{ mr: 1 }} />
          Supprimer
        </MenuItem>
      </Menu>

      {/* Dialog de confirmation de suppression */}
      <Dialog
        open={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
      >
        <DialogTitle>
          Supprimer l'expérience
        </DialogTitle>
        <DialogContent>
          <Typography>
            Êtes-vous sûr de vouloir supprimer l'expérience "{selectedExperience?.title}" ?
            Cette action est irréversible.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>
            Annuler
          </Button>
          <Button onClick={handleDeleteConfirm} color="error" variant="contained">
            Supprimer
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Experiences;