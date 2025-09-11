const express = require('express');
const cors = require('cors');

const app = express();
const PORT = 4000;

app.use(cors());
app.use(express.json());

app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.get('/api/experiences/public', (req, res) => {
  res.json({
    experiences: [
      {
        id: 'demo1',
        title: 'Demo AR Experience',
        description: 'Une expérience de démonstration',
        category: 'demo'
      }
    ]
  });
});

app.get('/api/experiences/:id', (req, res) => {
  res.json({
    id: req.params.id,
    title: 'Demo Experience',
    description: 'Expérience de test',
    content: []
  });
});

app.listen(PORT, () => {
  console.log(`Backend démarré sur http://localhost:${PORT}`);
});
