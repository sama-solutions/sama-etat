import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Chip,
  LinearProgress,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  ViewInAr as ExperiencesIcon,
  PhotoLibrary as AssetsIcon,
  Visibility as ViewsIcon,
  TouchApp as InteractionsIcon,
  TrendingUp as TrendingUpIcon,
  Add as AddIcon,
  Edit as EditIcon,
  Analytics as AnalyticsIcon,
  People as PeopleIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';
import axios from 'axios';
import { useAuthStore } from '../store/authStore';

// Données de démonstration pour les graphiques
const mockActivityData = [
  { name: 'Lun', scans: 12, interactions: 8 },
  { name: 'Mar', scans: 19, interactions: 15 },
  { name: 'Mer', scans: 8, interactions: 6 },
  { name: 'Jeu', scans: 25, interactions: 20 },
  { name: 'Ven', scans: 22, interactions: 18 },
  { name: 'Sam', scans: 30, interactions: 25 },
  { name: 'Dim', scans: 15, interactions: 12 },
];

const mockCategoryData = [
  { name: 'Cartes de visite', value: 45, color: '#667eea' },
  { name: 'Affiches', value: 30, color: '#764ba2' },
  { name: 'Produits', value: 15, color: '#f093fb' },
  { name: 'Autres', value: 10, color: '#4ade80' },
];

const StatCard = ({ title, value, icon, color, trend, subtitle }) => (
  <Card sx={{ height: '100%' }}>
    <CardContent>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 700, color: color, mb: 1 }}>
            {value}
          </Typography>
          <Typography variant="h6" sx={{ fontWeight: 500, mb: 0.5 }}>
            {title}
          </Typography>
          {subtitle && (
            <Typography variant="body2" sx={{ color: 'text.secondary' }}>
              {subtitle}
            </Typography>
          )}
          {trend && (
            <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
              <TrendingUpIcon sx={{ fontSize: 16, color: 'success.main', mr: 0.5 }} />
              <Typography variant="body2" sx={{ color: 'success.main' }}>
                +{trend}% cette semaine
              </Typography>
            </Box>
          )}
        </Box>
        <Avatar sx={{ backgroundColor: color, width: 56, height: 56 }}>
          {icon}
        </Avatar>
      </Box>
    </CardContent>
  </Card>
);

const Dashboard = () => {
  const navigate = useNavigate();
  const { user } = useAuthStore();
  const [stats, setStats] = useState(null);
  const [recentExperiences, setRecentExperiences] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // Récupérer les statistiques
        const statsResponse = await axios.get('/api/analytics/dashboard');
        setStats(statsResponse.data);

        // Récupérer les expériences récentes
        const experiencesResponse = await axios.get('/api/experiences?limit=5');
        setRecentExperiences(experiencesResponse.data.experiences || []);
      } catch (error) {
        console.error('Erreur lors du chargement des données:', error);
        // Utiliser des données de démonstration en cas d'erreur
        setStats({
          overview: {
            totalExperiences: 12,
            publishedExperiences: 8,
            totalViews: 1247,
            totalScans: 892,
            totalInteractions: 634
          }
        });
        setRecentExperiences([
          {
            _id: '1',
            title: 'Carte de visite CEO',
            status: 'published',
            category: 'business_card',
            stats: { scans: 45, views: 67 },
            updatedAt: new Date().toISOString()
          },
          {
            _id: '2',
            title: 'Affiche produit X',
            status: 'draft',
            category: 'poster',
            stats: { scans: 23, views: 34 },
            updatedAt: new Date().toISOString()
          }
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

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

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'business_card': return '💼';
      case 'poster': return '📋';
      case 'product': return '📦';
      default: return '📄';
    }
  };

  if (loading) {
    return (
      <Box>
        <Typography variant="h4" sx={{ mb: 3 }}>
          Tableau de bord
        </Typography>
        <LinearProgress />
      </Box>
    );
  }

  return (
    <Box>
      {/* En-tête */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
          Bonjour, {user?.firstName} ! 👋
        </Typography>
        <Typography variant="body1" sx={{ color: 'text.secondary' }}>
          Voici un aperçu de vos expériences de réalité augmentée
        </Typography>
      </Box>

      {/* Statistiques principales */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Expériences"
            value={stats?.overview?.totalExperiences || 0}
            subtitle={`${stats?.overview?.publishedExperiences || 0} publiées`}
            icon={<ExperiencesIcon />}
            color="#667eea"
            trend={12}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Vues totales"
            value={stats?.overview?.totalViews || 0}
            icon={<ViewsIcon />}
            color="#764ba2"
            trend={8}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Scans AR"
            value={stats?.overview?.totalScans || 0}
            icon={<AnalyticsIcon />}
            color="#f093fb"
            trend={15}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Interactions"
            value={stats?.overview?.totalInteractions || 0}
            icon={<InteractionsIcon />}
            color="#4ade80"
            trend={22}
          />
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Graphique d'activité */}
        <Grid item xs={12} lg={8}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Activité de la semaine
                </Typography>
                <Button
                  variant="outlined"
                  size="small"
                  onClick={() => navigate('/analytics')}
                >
                  Voir plus
                </Button>
              </Box>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={mockActivityData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <RechartsTooltip />
                  <Line 
                    type="monotone" 
                    dataKey="scans" 
                    stroke="#667eea" 
                    strokeWidth={3}
                    name="Scans"
                  />
                  <Line 
                    type="monotone" 
                    dataKey="interactions" 
                    stroke="#764ba2" 
                    strokeWidth={3}
                    name="Interactions"
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Répartition par catégorie */}
        <Grid item xs={12} lg={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
                Répartition par catégorie
              </Typography>
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie
                    data={mockCategoryData}
                    cx="50%"
                    cy="50%"
                    innerRadius={40}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {mockCategoryData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <RechartsTooltip />
                </PieChart>
              </ResponsiveContainer>
              <Box sx={{ mt: 2 }}>
                {mockCategoryData.map((item, index) => (
                  <Box key={index} sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <Box
                      sx={{
                        width: 12,
                        height: 12,
                        backgroundColor: item.color,
                        borderRadius: '50%',
                        mr: 1
                      }}
                    />
                    <Typography variant="body2" sx={{ flexGrow: 1 }}>
                      {item.name}
                    </Typography>
                    <Typography variant="body2" sx={{ fontWeight: 600 }}>
                      {item.value}%
                    </Typography>
                  </Box>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Expériences récentes */}
        <Grid item xs={12} lg={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Expériences récentes
                </Typography>
                <Button
                  variant="contained"
                  startIcon={<AddIcon />}
                  onClick={() => navigate('/experiences/new')}
                >
                  Nouvelle
                </Button>
              </Box>
              <List>
                {recentExperiences.map((experience, index) => (
                  <ListItem
                    key={experience._id}
                    sx={{
                      border: '1px solid',
                      borderColor: 'divider',
                      borderRadius: 2,
                      mb: 1,
                      '&:last-child': { mb: 0 }
                    }}
                    secondaryAction={
                      <Tooltip title="Modifier">
                        <IconButton
                          edge="end"
                          onClick={() => navigate(`/experiences/${experience._id}/edit`)}
                        >
                          <EditIcon />
                        </IconButton>
                      </Tooltip>
                    }
                  >
                    <ListItemAvatar>
                      <Avatar sx={{ backgroundColor: 'primary.main' }}>
                        {getCategoryIcon(experience.category)}
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                            {experience.title}
                          </Typography>
                          <Chip
                            label={getStatusLabel(experience.status)}
                            color={getStatusColor(experience.status)}
                            size="small"
                          />
                        </Box>
                      }
                      secondary={
                        <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                          {experience.stats?.scans || 0} scans • {experience.stats?.views || 0} vues
                        </Typography>
                      }
                    />
                  </ListItem>
                ))}
              </List>
              {recentExperiences.length === 0 && (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <Typography variant="body2" sx={{ color: 'text.secondary', mb: 2 }}>
                    Aucune expérience créée
                  </Typography>
                  <Button
                    variant="outlined"
                    startIcon={<AddIcon />}
                    onClick={() => navigate('/experiences/new')}
                  >
                    Créer votre première expérience
                  </Button>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Actions rapides */}
        <Grid item xs={12} lg={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
                Actions rapides
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<ExperiencesIcon />}
                    onClick={() => navigate('/experiences/new')}
                    sx={{ py: 2 }}
                  >
                    Nouvelle expérience
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<AssetsIcon />}
                    onClick={() => navigate('/assets')}
                    sx={{ py: 2 }}
                  >
                    Gérer les assets
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<AnalyticsIcon />}
                    onClick={() => navigate('/analytics')}
                    sx={{ py: 2 }}
                  >
                    Voir analytics
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<PeopleIcon />}
                    onClick={() => navigate('/settings')}
                    sx={{ py: 2 }}
                  >
                    Paramètres
                  </Button>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;