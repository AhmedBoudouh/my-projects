const mongoose = require('mongoose');
// Define the Product schema
const productSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
      trim: true,
    },
    category: {
      type: String,
      required: true,
      trim: true,
    },
    price: {
      type: Number,
      required: true,
      min: 0,
    },
    stock: {
      type: Number,
      default: 0,
      min: 0,
    },
    // Image URL used by store-front
    imageUrl: {
      type: String,
      default: null,
    },
  },
  {
    timestamps: true, // createdAt / updatedAt
  }
);
// Create and export the Product model
const Product = mongoose.model('Product', productSchema);
module.exports = Product;
