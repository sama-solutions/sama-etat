const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3000;

const server = http.createServer((req, res) => {
  console.log(`📥 Requête: ${req.method} ${req.url}`);
  
  // Headers CORS et cache
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 'no-cache');
  
  if (req.url === '/' || req.url === '/index.html') {
    // Servir la page de test
    const html = `
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎨 Sama Jokoo - Test</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f0f0f3;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            background: #f0f0f3;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 
                8px 8px 16px #d1d1d4,
                -8px -8px 16px #ffffff;
            text-align: center;
            max-width: 500px;
        }
        h1 {
            color: #2d3748;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .status {
            color: #4ecdc4;
            font-weight: bold;
            font-size: 1.2em;
            margin: 20px 0;
        }
        .info {
            color: #718096;
            margin-top: 20px;
        }
        .button {
            background: #f0f0f3;
            border: none;
            border-radius: 12px;
            padding: 12px 24px;
            color: #2d3748;
            font-weight: 600;
            cursor: pointer;
            margin: 10px;
            box-shadow: 
                6px 6px 12px #d1d1d4,
                -6px -6px 12px #ffffff;
            transition: all 0.3s ease;
        }
        .button:hover {
            transform: translateY(-1px);
            box-shadow: 
                8px 8px 16px #d1d1d4,
                -8px -8px 16px #ffffff;
        }
        .button:active {
            transform: translateY(0);
            box-shadow: 
                inset 3px 3px 6px #d1d1d4,
                inset -3px -3px 6px #ffffff;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 Sama Jokoo</h1>
        <div class="status">✅ Serveur Test Fonctionnel</div>
        <div class="info">
            <p><strong>🎉 Succès !</strong> Le serveur fonctionne parfaitement.</p>
            <p><strong>URL:</strong> http://localhost:3000</p>
            <p><strong>Status:</strong> Serveur Node.js actif</p>
            <p><strong>Design:</strong> Neumorphique</p>
        </div>
        <button class="button" onclick="testApp()">🚀 Tester l'Application</button>
        <button class="button" onclick="location.reload()">🔄 Actualiser</button>
    </div>
    
    <script>
        function testApp() {
            alert('🎨 Application Sama Jokoo fonctionnelle !\\n\\n✅ Serveur: OK\\n✅ Design: Neumorphique\\n✅ JavaScript: Actif');
        }
        
        console.log('🎨 Sama Jokoo - Application de test chargée');
        console.log('✅ Serveur Node.js fonctionnel');
        console.log('🎯 Prêt pour le développement');
    </script>
</body>
</html>`;
    
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(html);
    
  } else if (req.url === '/api/test') {
    // API de test
    const response = {
      status: 'success',
      message: 'API Sama Jokoo fonctionnelle',
      timestamp: new Date().toISOString(),
      server: 'Node.js Test Server'
    };
    
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(response, null, 2));
    
  } else {
    // 404
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Page non trouvée');
  }
});

server.listen(PORT, () => {
  console.log('🎨 Serveur de test Sama Jokoo');
  console.log('=' * 30);
  console.log(`✅ Serveur démarré avec succès !`);
  console.log(`📱 URL: http://localhost:${PORT}`);
  console.log(`🎯 Design: Neumorphique`);
  console.log(`🔄 Pour arrêter: Ctrl+C`);
  console.log('');
});

server.on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.log(`❌ Port ${PORT} déjà utilisé`);
    console.log('🔄 Essayez d\'arrêter les autres processus');
  } else {
    console.log(`❌ Erreur serveur: ${err.message}`);
  }
});