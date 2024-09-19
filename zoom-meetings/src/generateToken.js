// src/generateToken.js
const jwt = require('jsonwebtoken');
const { CLIENT_ID, CLIENT_SECRET } = require('../config/keys');

// Define the payload for the JWT
const payload = {
  iss: CLIENT_ID,                              // Issuer (Client ID)
  exp: Math.floor(Date.now() / 1000) + (60 * 60), // Token valid for 1 hour
};

// Generate JWT
const token = jwt.sign(payload, CLIENT_SECRET);  // Sign the payload with Client Secret

console.log("Generated JWT:", token);           // Output the generated token
