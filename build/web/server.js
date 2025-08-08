const express = require('express');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = 3003;

// Middleware
app.use(cors());
app.use(express.json());

// Serve HTML files - маршруты должны быть ПЕРЕД статическими файлами
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'admin_new.html'));
});

app.get('/admin', (req, res) => {
  res.sendFile(path.join(__dirname, 'admin_new.html'));
});



// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date(),
    message: 'GTM Admin Panel Web Server'
  });
});

// Статические файлы ПОСЛЕ маршрутов
app.use(express.static(path.join(__dirname)));

// Start server
app.listen(PORT, () => {
  console.log(`🚀 GTM Admin Panel Web Server запущен на порту ${PORT}`);
  console.log(`📊 Доступен по адресу: http://localhost:${PORT}`);
  console.log(`🔧 API Base URL: http://localhost:3001/api`);
  console.log(`🌍 Environment: development`);
  console.log(`⏰ Started at: ${new Date().toISOString()}`);
}); 