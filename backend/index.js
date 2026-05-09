const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
const authRoutes = require('./routes/auth');
const productRoutes = require('./routes/products');
app.use('/api/auth', authRoutes);
app.use('/api/products', productRoutes);

// Health Check Endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'UP', message: 'Backend is running smoothly' });
});

// Basic route
app.get('/', (req, res) => {
  res.send('E-commerce DevSecOps API is running!');
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
