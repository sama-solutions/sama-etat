import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  LinearProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Avatar,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  Visibility as ViewsIcon,
  TouchApp as InteractionsIcon,
  Schedule as TimeIcon,
} from '@mui/icons-material';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area
} from 'recharts';
import axios from 'axios';

// Données de démonstration
const mockDailyData = [
  { date: '2024-01-01', scans: 12, views: 18, interactions: 8 },
  { date: '2024-01-02', scans: 19, views: 25, interactions: 15 },
  { date: '2024-01-03', scans: 8, views: 12, interactions: 6 },
  { date: '2024-01-04', scans: 25, views: 32, interactions: 20 },
  { date: '2024-01-05', scans: 22, views: 28, interactions: 18 },
  { date: '2024-01-06', scans: 30, views: 38, interactions: 25 },
  { date: '2024-01-07', scans: 15, views: 20, interactions: 12 },
];

const mockTopExperiences = [
  {
    id: '1',
    title: 'Carte de visite CEO',
    category: 'business_card',
    scans: 156,
    views: 234,
    interactions: 89,
    engagementRate: 57.1
  },
  {
    id: '2',
    title: 'Affiche produit X',
    category: 'poster',
    scans: 98,
    views: 145,
    interactions: 67,
    engagementRate: 68.4
  },
  {
    id: '3',
    title: 'Présentation 3D',
    category: 'product',
    scans: 76,
    views: 112,
    interactions: 45,
    engagementRate: 59.2
  }
];

const mockDeviceData = [
  { name: 'Mobile', value: 65, color: '#667eea' },
  { name: 'Desktop', value: 25, color: '#764ba2' },
  { name: 'Tablette', value: 10, color: '#f093fb' }
];

const StatCard = ({ title, value, icon, color, trend, subtitle }) => (
  <Card>
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
                +{trend}% vs période précédente
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

const Analytics = () => {
  const [loading, setLoading] = useState(true);
  const [period, setPeriod] = useState('7d');
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchAnalytics();
  }, [period]);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      // const response = await axios.get(`/api/analytics/dashboard?period=${period}`);
      // setStats(response.data);
      
      // Simulation avec des données de démonstration
      setTimeout(() => {
        setStats({
          overview: {
            totalScans: 1247,
            totalViews: 1892,
            totalInteractions: 634,
            averageEngagement: 50.8
          }
        });
        setLoading(false);
      }, 1000);
    } catch (error) {
      console.error('Erreur lors du chargement des analytics:', error);
      setLoading(false);
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

  const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit'
    });
  };

  if (loading) {
    return (
      <Box>
        <Typography variant="h4" sx={{ mb: 3 }}>
          Analytics
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
            Analytics
          </Typography>
          <Typography variant="body1" sx={{ color: 'text.secondary' }}>
            Analysez les performances de vos expériences AR
          </Typography>
        </Box>
        <FormControl sx={{ minWidth: 120 }}>
          <InputLabel>Période</InputLabel>
          <Select
            value={period}
            label="Période"
            onChange={(e) => setPeriod(e.target.value)}
          >
            <MenuItem value="7d">7 derniers jours</MenuItem>
            <MenuItem value="30d">30 derniers jours</MenuItem>
            <MenuItem value="90d">90 derniers jours</MenuItem>
            <MenuItem value="1y">1 an</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {/* Statistiques principales */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Scans totaux"
            value={stats?.overview?.totalScans || 0}
            icon={<ViewsIcon />}
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
            title="Interactions"
            value={stats?.overview?.totalInteractions || 0}
            icon={<InteractionsIcon />}
            color="#f093fb"
            trend={15}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Engagement moyen"
            value={`${stats?.overview?.averageEngagement || 0}%`}
            icon={<TrendingUpIcon />}
            color="#4ade80"
            trend={5}
          />
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Graphique d'activité */}
        <Grid item xs={12} lg={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
                Activité quotidienne
              </Typography>
              <ResponsiveContainer width="100%" height={350}>
                <AreaChart data={mockDailyData}>
                  <defs>
                    <linearGradient id="colorScans" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#667eea" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#667eea" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="colorViews" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#764ba2" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#764ba2" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <XAxis 
                    dataKey="date" 
                    tickFormatter={formatDate}
                  />
                  <YAxis />
                  <CartesianGrid strokeDasharray="3 3" />
                  <Tooltip 
                    labelFormatter={(value) => formatDate(value)}
                  />
                  <Area 
                    type="monotone" 
                    dataKey="scans" 
                    stroke="#667eea" 
                    fillOpacity={1} 
                    fill="url(#colorScans)"
                    name="Scans"
                  />
                  <Area 
                    type="monotone" 
                    dataKey="views" 
                    stroke="#764ba2" 
                    fillOpacity={1} 
                    fill="url(#colorViews)"
                    name="Vues"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Répartition par appareil */}
        <Grid item xs={12} lg={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
                Répartition par appareil
              </Typography>
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie
                    data={mockDeviceData}
                    cx="50%"
                    cy="50%"
                    innerRadius={40}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {mockDeviceData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
              <Box sx={{ mt: 2 }}>
                {mockDeviceData.map((item, index) => (
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

        {/* Top expériences */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
                Expériences les plus performantes
              </Typography>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Expérience</TableCell>
                      <TableCell align="center">Catégorie</TableCell>
                      <TableCell align="center">Scans</TableCell>
                      <TableCell align="center">Vues</TableCell>
                      <TableCell align="center">Interactions</TableCell>
                      <TableCell align="center">Taux d'engagement</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {mockTopExperiences.map((experience, index) => (
                      <TableRow key={experience.id}>
                        <TableCell>
                          <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <Avatar sx={{ mr: 2, backgroundColor: 'primary.main' }}>
                              {getCategoryIcon(experience.category)}
                            </Avatar>
                            <Box>
                              <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                                {experience.title}
                              </Typography>
                              <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                                #{index + 1}
                              </Typography>
                            </Box>
                          </Box>
                        </TableCell>
                        <TableCell align="center">
                          <Chip
                            label={experience.category.replace('_', ' ')}
                            size="small"
                            variant="outlined"
                          />
                        </TableCell>
                        <TableCell align="center">
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>
                            {experience.scans}
                          </Typography>
                        </TableCell>
                        <TableCell align="center">
                          <Typography variant="body2">
                            {experience.views}
                          </Typography>
                        </TableCell>
                        <TableCell align="center">
                          <Typography variant="body2">
                            {experience.interactions}
                          </Typography>
                        </TableCell>
                        <TableCell align="center">
                          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                            <Typography variant="body2" sx={{ mr: 1 }}>
                              {experience.engagementRate}%
                            </Typography>
                            <LinearProgress
                              variant="determinate"
                              value={experience.engagementRate}
                              sx={{ width: 60, height: 6, borderRadius: 3 }}
                            />
                          </Box>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Graphique des interactions */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
                Interactions par jour
              </Typography>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={mockDailyData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" tickFormatter={formatDate} />
                  <YAxis />
                  <Tooltip labelFormatter={(value) => formatDate(value)} />
                  <Bar dataKey="interactions" fill="#f093fb" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Temps d'engagement */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
                Temps d'engagement moyen
              </Typography>
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <Avatar sx={{ 
                  width: 80, 
                  height: 80, 
                  backgroundColor: 'primary.main',
                  mx: 'auto',
                  mb: 2
                }}>
                  <TimeIcon sx={{ fontSize: 40 }} />
                </Avatar>
                <Typography variant="h3" sx={{ fontWeight: 700, color: 'primary.main', mb: 1 }}>
                  2m 34s
                </Typography>
                <Typography variant="body1" sx={{ color: 'text.secondary', mb: 2 }}>
                  Temps moyen par session
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <TrendingUpIcon sx={{ fontSize: 16, color: 'success.main', mr: 0.5 }} />
                  <Typography variant="body2" sx={{ color: 'success.main' }}>
                    +18% vs période précédente
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Analytics;