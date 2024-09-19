// src/zoomApi.js
const axios = require('axios');
const { BASE_URI } = require('../config/keys');
const generateToken = require('./generateToken');

// Use the token generated in the previous step
const token = generateToken();  // Import generated token

// Function to make a Zoom API request using Axios
const getZoomUsers = async () => {
  try {
    const response = await axios.get(`${BASE_URI}/users`, {
      headers: {
        'Authorization': `Bearer ${token}`,   // Include JWT in the Authorization header
      },
    });
    
    console.log('Zoom API Response:', response.data); // Handle the response data
  } catch (error) {
    console.error('Error making Zoom API request:', error.response.data);
  }
};

getZoomUsers();
