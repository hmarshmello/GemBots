const express = require('express');
const serverless = require('serverless-http');
const path = require('path');

const app = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

// Health check endpoint
app.get('/.netlify/functions/server/health', (req, res) => {
  res.json({ status: 'healthy' });
});

// Main handler
app.get('*', async (req, res) => {
  try {
    // Redirect to Render deployment
    const renderUrl = process.env.RENDER_URL || 'https://gembots.onrender.com';
    res.redirect(renderUrl);
  } catch (error) {
    console.error('Server error:', error);
    res.redirect('/error.html?error=' + encodeURIComponent(error.message));
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.redirect('/error.html?error=' + encodeURIComponent(err.message));
});

// Export the serverless handler
const handler = serverless(app);

exports.handler = async (event, context) => {
  // Handle CORS preflight requests
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 204,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
      }
    };
  }

  try {
    // Handle regular requests
    const result = await handler(event, context);
    return {
      ...result,
      headers: {
        ...result.headers,
        'Access-Control-Allow-Origin': '*'
      }
    };
  } catch (error) {
    console.error('Handler error:', error);
    return {
      statusCode: 500,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'text/html'
      },
      body: `
        <script>
          window.location.href = '/error.html?error=${encodeURIComponent(error.message)}';
        </script>
      `
    };
  }
};
