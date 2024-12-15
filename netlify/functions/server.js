const { builder } = require("@netlify/functions");

const handler = async (event, context) => {
  // CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE'
  };

  // Handle OPTIONS request for CORS
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 204,
      headers
    };
  }

  try {
    // Basic routing
    if (event.path === '/') {
      return {
        statusCode: 200,
        headers: { ...headers, 'Content-Type': 'text/html' },
        body: `
          <!DOCTYPE html>
          <html>
            <head>
              <title>GemBots - Redirecting...</title>
              <meta http-equiv="refresh" content="0;url=https://gembots.vercel.app">
            </head>
            <body>
              <p>Redirecting to main application...</p>
            </body>
          </html>
        `
      };
    }

    // API endpoint for health check
    if (event.path === '/.netlify/functions/server/health') {
      return {
        statusCode: 200,
        headers: { ...headers, 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: 'healthy' })
      };
    }

    // Default response for unhandled routes
    return {
      statusCode: 404,
      headers,
      body: JSON.stringify({ message: 'Not Found' })
    };

  } catch (error) {
    console.error('Error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ message: 'Internal Server Error' })
    };
  }
};

// Export the handler wrapped with builder
exports.handler = builder(handler);
