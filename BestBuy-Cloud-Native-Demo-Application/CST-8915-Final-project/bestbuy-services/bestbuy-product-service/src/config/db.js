// db.js - Database Connection for BestBuy Product Service
const mongose = require('mongoose');
async function connectDB() {
const mongoURI = process.env.MONGO_URI || 'mongodb://localhost:27017/bestbuy';
// Connect to MongoDB
try {
    await mongose.connect(mongoURI);
    console.log('Connected to MongoDB');
} catch (error) {
    console.error('Error connecting to MongoDB:', error);
    process.exit(1);
}
}
module.exports = connectDB;