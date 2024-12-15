const serverless = require('serverless-http');
const express = require('express');
const { spawn } = require('child_process');
const path = require('path');

// Create express app
const app = express();

// Serve static files
app.use(express.static('public'));

// Proxy all requests to Flask app
app.all('*', (req, res) => {
  const flask = spawn('python', ['api/app.py']);
  
  let data = '';
  
  flask.stdout.on('data', (chunk) => {
    data += chunk;
  });
  
  flask.stderr.on('data', (chunk) => {
    console.error('Flask error:', chunk.toString());
  });
  
  flask.on('close', (code) => {
    if (code !== 0) {
      res.status(500).send('Flask application error');
      return;
    }
    res.send(data);
  });
});

// Export handler for serverless
module.exports.handler = serverless(app);
