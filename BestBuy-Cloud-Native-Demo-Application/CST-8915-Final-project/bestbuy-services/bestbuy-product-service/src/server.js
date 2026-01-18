const express = require('express');
const cors = require('cors');
const connectDB = require('./config/db');
const productRoutes = require('./routes/productRoutes'); 
const app = express();
app.use(cors());
app.use(express.json());
app.use("/api/products", productRoutes);
const PORT = process.env.PORT || 4000;
connectDB().then(() => {
    app.listen(PORT, () => {
      console.log(`product-service is listening on port ${PORT}`);
    });
  })
  .catch((error) => {
    console.error('Failed to connect to the database', error);
    process.exit(1); 
    });