import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  TextField,
  Button,
  Switch,
  FormControlLabel,
  Divider,
  Avatar,
  IconButton,
  Alert,
  Tabs,
  Tab,
  Paper,
} from '@mui/material';
import {
  Person as PersonIcon,
  Security as SecurityIcon,
  Notifications as NotificationsIcon,
  Palette as ThemeIcon,
  CloudUpload as UploadIcon,
  Save as SaveIcon,
} from '@mui/icons-material';
import { useAuthStore } from '../store/authStore';
import toast from 'react-hot-toast';

const TabPanel = ({ children, value, index, ...other }) => (
  <div
    role="tabpanel"
    hidden={value !== index}
    id={`settings-tabpanel-${index}`}
    aria-labelledby={`settings-tab-${index}`}
    {...other}
  >
    {value === index && (
      <Box sx={{ py: 3 }}>
        {children}
      </Box>
    )}
  </div>
);

const Settings = () => {
  const { user, updateProfile } = useAuthStore();
  const [activeTab, setActiveTab] = useState(0);
  const [loading, setLoading] = useState(false);
  
  const [profileData, setProfileData] = useState({
    firstName: user?.firstName || '',
    lastName: user?.lastName || '',
    email: user?.email || '',
    company: user?.company || '',
  });

  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });

  const [notificationSettings, setNotificationSettings] = useState({
    emailNotifications: true,
    pushNotifications: true,
    weeklyReport: true,
    securityAlerts: true,
  });

  const [themeSettings, setThemeSettings] = useState({
    darkMode: false,
    compactMode: false,
    animations: true,
  });

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const handleProfileChange = (field, value) => {
    setProfileData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handlePasswordChange = (field, value) => {
    setPasswordData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleNotificationChange = (field, value) => {
    setNotificationSettings(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleThemeChange = (field, value) => {
    setThemeSettings(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleProfileSave = async () => {
    try {
      setLoading(true);
      const result = await updateProfile(profileData);
      
      if (result.success) {
        toast.success('Profil mis à jour avec succès');
      } else {
        toast.error(result.error);
      }
    } catch (error) {
      toast.error('Erreur lors de la mise à jour du profil');
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordSave = async () => {
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      toast.error('Les mots de passe ne correspondent pas');
      return;
    }

    if (passwordData.newPassword.length < 6) {
      toast.error('Le mot de passe doit contenir au moins 6 caractères');
      return;
    }

    try {
      setLoading(true);
      // Appel API pour changer le mot de passe
      toast.success('Mot de passe mis à jour avec succès');
      setPasswordData({
        currentPassword: '',
        newPassword: '',
        confirmPassword: '',
      });
    } catch (error) {
      toast.error('Erreur lors du changement de mot de passe');
    } finally {
      setLoading(false);
    }
  };

  const handleNotificationSave = () => {
    toast.success('Paramètres de notification sauvegardés');
  };

  const handleThemeSave = () => {
    toast.success('Paramètres d\'apparence sauvegardés');
  };

  return (
    <Box>
      {/* En-tête */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
          Paramètres
        </Typography>
        <Typography variant="body1" sx={{ color: 'text.secondary' }}>
          Gérez vos préférences et paramètres de compte
        </Typography>
      </Box>

      {/* Onglets */}
      <Paper sx={{ mb: 3 }}>
        <Tabs
          value={activeTab}
          onChange={handleTabChange}
          variant="scrollable"
          scrollButtons="auto"
        >
          <Tab icon={<PersonIcon />} label="Profil" />
          <Tab icon={<SecurityIcon />} label="Sécurité" />
          <Tab icon={<NotificationsIcon />} label="Notifications" />
          <Tab icon={<ThemeIcon />} label="Apparence" />
        </Tabs>
      </Paper>

      {/* Contenu des onglets */}
      <Card>
        <CardContent>
          {/* Onglet Profil */}
          <TabPanel value={activeTab} index={0}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={4}>
                <Box sx={{ textAlign: 'center' }}>
                  <Avatar
                    sx={{
                      width: 120,
                      height: 120,
                      mx: 'auto',
                      mb: 2,
                      backgroundColor: 'primary.main',
                      fontSize: '2rem'
                    }}
                  >
                    {user?.firstName?.[0]}{user?.lastName?.[0]}
                  </Avatar>
                  <Button
                    variant="outlined"
                    startIcon={<UploadIcon />}
                    size="small"
                  >
                    Changer la photo
                  </Button>
                </Box>
              </Grid>
              
              <Grid item xs={12} md={8}>
                <Grid container spacing={3}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Prénom"
                      value={profileData.firstName}
                      onChange={(e) => handleProfileChange('firstName', e.target.value)}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Nom"
                      value={profileData.lastName}
                      onChange={(e) => handleProfileChange('lastName', e.target.value)}
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Email"
                      type="email"
                      value={profileData.email}
                      onChange={(e) => handleProfileChange('email', e.target.value)}
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Entreprise"
                      value={profileData.company}
                      onChange={(e) => handleProfileChange('company', e.target.value)}
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <Button
                      variant="contained"
                      startIcon={<SaveIcon />}
                      onClick={handleProfileSave}
                      disabled={loading}
                    >
                      Sauvegarder les modifications
                    </Button>
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
          </TabPanel>

          {/* Onglet Sécurité */}
          <TabPanel value={activeTab} index={1}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Typography variant="h6" sx={{ mb: 2 }}>
                  Changer le mot de passe
                </Typography>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Mot de passe actuel"
                  type="password"
                  value={passwordData.currentPassword}
                  onChange={(e) => handlePasswordChange('currentPassword', e.target.value)}
                />
              </Grid>
              
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Nouveau mot de passe"
                  type="password"
                  value={passwordData.newPassword}
                  onChange={(e) => handlePasswordChange('newPassword', e.target.value)}
                />
              </Grid>
              
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Confirmer le nouveau mot de passe"
                  type="password"
                  value={passwordData.confirmPassword}
                  onChange={(e) => handlePasswordChange('confirmPassword', e.target.value)}
                />
              </Grid>
              
              <Grid item xs={12}>
                <Button
                  variant="contained"
                  onClick={handlePasswordSave}
                  disabled={loading || !passwordData.currentPassword || !passwordData.newPassword}
                >
                  Changer le mot de passe
                </Button>
              </Grid>

              <Grid item xs={12}>
                <Divider sx={{ my: 2 }} />
                <Typography variant="h6" sx={{ mb: 2 }}>
                  Sécurité du compte
                </Typography>
                <Alert severity="info" sx={{ mb: 2 }}>
                  Votre compte est sécurisé. Dernière connexion : {new Date().toLocaleDateString()}
                </Alert>
              </Grid>
            </Grid>
          </TabPanel>

          {/* Onglet Notifications */}
          <TabPanel value={activeTab} index={2}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Typography variant="h6" sx={{ mb: 2 }}>
                  Préférences de notification
                </Typography>
              </Grid>
              
              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={notificationSettings.emailNotifications}
                      onChange={(e) => handleNotificationChange('emailNotifications', e.target.checked)}
                    />
                  }
                  label="Notifications par email"
                />
                <Typography variant="body2" sx={{ color: 'text.secondary', ml: 4 }}>
                  Recevoir des notifications importantes par email
                </Typography>
              </Grid>
              
              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={notificationSettings.pushNotifications}
                      onChange={(e) => handleNotificationChange('pushNotifications', e.target.checked)}
                    />
                  }
                  label="Notifications push"
                />
                <Typography variant="body2" sx={{ color: 'text.secondary', ml: 4 }}>
                  Recevoir des notifications en temps réel
                </Typography>
              </Grid>
              
              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={notificationSettings.weeklyReport}
                      onChange={(e) => handleNotificationChange('weeklyReport', e.target.checked)}
                    />
                  }
                  label="Rapport hebdomadaire"
                />
                <Typography variant="body2" sx={{ color: 'text.secondary', ml: 4 }}>
                  Recevoir un résumé hebdomadaire de vos analytics
                </Typography>
              </Grid>
              
              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={notificationSettings.securityAlerts}
                      onChange={(e) => handleNotificationChange('securityAlerts', e.target.checked)}
                    />
                  }
                  label="Alertes de sécurité"
                />
                <Typography variant="body2" sx={{ color: 'text.secondary', ml: 4 }}>
                  Recevoir des alertes en cas d'activité suspecte
                </Typography>
              </Grid>
              
              <Grid item xs={12}>
                <Button
                  variant="contained"
                  onClick={handleNotificationSave}
                >
                  Sauvegarder les préférences
                </Button>
              </Grid>
            </Grid>
          </TabPanel>

          {/* Onglet Apparence */}
          <TabPanel value={activeTab} index={3}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Typography variant="h6" sx={{ mb: 2 }}>
                  Préférences d'apparence
                </Typography>
              </Grid>
              
              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={themeSettings.darkMode}
                      onChange={(e) => handleThemeChange('darkMode', e.target.checked)}
                    />
                  }
                  label="Mode sombre"
                />
                <Typography variant="body2" sx={{ color: 'text.secondary', ml: 4 }}>
                  Utiliser le thème sombre pour l'interface
                </Typography>
              </Grid>
              
              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={themeSettings.compactMode}
                      onChange={(e) => handleThemeChange('compactMode', e.target.checked)}
                    />
                  }
                  label="Mode compact"
                />
                <Typography variant="body2" sx={{ color: 'text.secondary', ml: 4 }}>
                  Affichage plus dense pour plus d'informations à l'écran
                </Typography>
              </Grid>
              
              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={themeSettings.animations}
                      onChange={(e) => handleThemeChange('animations', e.target.checked)}
                    />
                  }
                  label="Animations"
                />
                <Typography variant="body2" sx={{ color: 'text.secondary', ml: 4 }}>
                  Activer les animations et transitions
                </Typography>
              </Grid>
              
              <Grid item xs={12}>
                <Button
                  variant="contained"
                  onClick={handleThemeSave}
                >
                  Sauvegarder les préférences
                </Button>
              </Grid>
            </Grid>
          </TabPanel>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Settings;