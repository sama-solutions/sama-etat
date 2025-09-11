#!/usr/bin/env node

/**
 * Script pour détecter l'adresse IP locale de la machine
 * Utilisé pour générer les URLs mobiles automatiquement
 */

const os = require('os');

function getLocalIP() {
  const interfaces = os.networkInterfaces();
  
  // Priorité des interfaces réseau
  const priorities = ['wlan', 'wifi', 'eth', 'en'];
  
  for (const priority of priorities) {
    for (const [name, addresses] of Object.entries(interfaces)) {
      if (name.toLowerCase().includes(priority)) {
        for (const addr of addresses || []) {
          if (addr.family === 'IPv4' && !addr.internal) {
            return addr.address;
          }
        }
      }
    }
  }
  
  // Fallback: première adresse IPv4 non-interne trouvée
  for (const addresses of Object.values(interfaces)) {
    for (const addr of addresses || []) {
      if (addr.family === 'IPv4' && !addr.internal) {
        return addr.address;
      }
    }
  }
  
  return 'localhost';
}

function getAllLocalIPs() {
  const interfaces = os.networkInterfaces();
  const ips = [];
  
  for (const addresses of Object.values(interfaces)) {
    for (const addr of addresses || []) {
      if (addr.family === 'IPv4' && !addr.internal) {
        ips.push(addr.address);
      }
    }
  }
  
  return ips;
}

function generateMobileURLs(port = 3000) {
  const localIP = getLocalIP();
  const allIPs = getAllLocalIPs();
  
  return {
    primary: `http://${localIP}:${port}`,
    scanner: `http://${localIP}:${port}/scanner`,
    api: `http://${localIP}:4000`,
    alternatives: allIPs.map(ip => ({
      ip,
      frontend: `http://${ip}:${port}`,
      scanner: `http://${ip}:${port}/scanner`,
      api: `http://${ip}:4000`
    }))
  };
}

function displayMobileInfo() {
  const urls = generateMobileURLs();
  
  console.log('📱 URLs pour Tests Mobiles');
  console.log('==========================');
  console.log('');
  console.log('🎯 URL Principale:');
  console.log(`   Frontend: ${urls.primary}`);
  console.log(`   Scanner:  ${urls.scanner}`);
  console.log(`   API:      ${urls.api}`);
  console.log('');
  
  if (urls.alternatives.length > 1) {
    console.log('🔄 Alternatives (si la principale ne fonctionne pas):');
    urls.alternatives.forEach((alt, index) => {
      console.log(`   ${index + 1}. IP ${alt.ip}:`);
      console.log(`      Frontend: ${alt.frontend}`);
      console.log(`      Scanner:  ${alt.scanner}`);
    });
    console.log('');
  }
  
  console.log('📋 Instructions:');
  console.log('1. Assurez-vous que votre mobile est sur le même réseau WiFi');
  console.log('2. Ouvrez l\'URL du scanner sur votre mobile');
  console.log('3. Autorisez l\'accès à la caméra');
  console.log('4. Scannez un QR code ARBase');
  console.log('');
  
  return urls;
}

// Si exécuté directement
if (require.main === module) {
  const command = process.argv[2];
  
  switch (command) {
    case 'ip':
      console.log(getLocalIP());
      break;
    case 'all':
      console.log(getAllLocalIPs().join('\n'));
      break;
    case 'urls':
      const port = process.argv[3] || 3000;
      const urls = generateMobileURLs(parseInt(port));
      console.log(JSON.stringify(urls, null, 2));
      break;
    case 'display':
    default:
      displayMobileInfo();
      break;
  }
}

module.exports = {
  getLocalIP,
  getAllLocalIPs,
  generateMobileURLs,
  displayMobileInfo
};