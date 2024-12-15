const express = require('express');
const serverless = require('serverless-http');
const { spawn } = require('child_process');
const path = require('path');

const app = express();

// Middleware to parse JSON and form data
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files
app.use(express.static('public'));

// Health check endpoint
app.get('/.netlify/functions/server/health', (req, res) => {
  res.json({ status: 'healthy' });
});

// Main handler for all routes
app.all('*', async (req, res) => {
  try {
    // Set CORS headers
    res.set({
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    });

    // Handle OPTIONS request
    if (req.method === 'OPTIONS') {
      return res.status(200).end();
    }

    // Spawn Flask process
    const flask = spawn('python', ['api/app.py'], {
      env: {
        ...process.env,
        FLASK_APP: 'api/app.py',
        FLASK_ENV: 'production'
      }
    });

    let responseData = '';
    let errorData = '';

    flask.stdout.on('data', (data) => {
      responseData += data.toString();
    });

    flask.stderr.on('data', (data) => {
      errorData += data.toString();
      console.error('Flask error:', data.toString());
    });

    flask.on('close', (code) => {
      if (code !== 0) {
        console.error('Flask process exited with code:', code);
        console.error('Error output:', errorData);
        return res.status(500).json({
          error: 'Internal Server Error',
          details: errorData
        });
      }

      try {
        // Try to parse response as JSON
        const jsonResponse = JSON.parse(responseData);
        res.json(jsonResponse);
      } catch (e) {
        // If not JSON, send as HTML
        res.send(responseData);
      }
    });

    // Handle request body if POST
    if (req.method === 'POST' && req.body) {
      flask.stdin.write(JSON.stringify(req.body));
      flask.stdin.end();
    }

  } catch (error) {
    console.error('Server error:', error);
    res.status(500).json({
      error: 'Internal Server Error',
      details: error.message
    });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: 'Internal Server Error',
    details: err.message
  });
});

// Export the serverless handler
module.exports.handler = serverless(app, {
  binary: ['image/*', 'audio/*', 'video/*', 'application/pdf']
});
