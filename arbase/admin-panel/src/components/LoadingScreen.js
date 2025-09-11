import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';

const LoadingScreen = ({ message = 'Chargement...' }) => {
  return (
    <Box
      sx={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        color: 'white',
        zIndex: 9999,
      }}
    >
      <CircularProgress 
        size={60} 
        sx={{ 
          color: 'white',
          mb: 3
        }} 
      />
      <Typography variant="h4" sx={{ mb: 2, fontWeight: 600 }}>
        ARBase Admin Panel
      </Typography>
      <Typography variant="body1" sx={{ opacity: 0.9 }}>
        {message}
      </Typography>
    </Box>
  );
};

export default LoadingScreen;