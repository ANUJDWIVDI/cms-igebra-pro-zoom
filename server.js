const express = require('express');
const app = express();
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const Zoom = require('zoomus')({
    key: 'YOUR_ZOOM_API_KEY',
    secret: 'YOUR_ZOOM_API_SECRET'
});

// Serve static files from the "public" folder
app.use(express.static('public'));

// Body-parser middleware
app.use(bodyParser.json());


mongoose.connect('mongodb+srv://anujd0009:aaaaaa@erp0.qhzju.mongodb.net/<database_name>?retryWrites=true&w=majority&appName=ERP0', {
    useNewUrlParser: true
})
.then(() => console.log("Connected to MongoDB"))
.catch(err => console.error("Could not connect to MongoDB...", err));


// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
