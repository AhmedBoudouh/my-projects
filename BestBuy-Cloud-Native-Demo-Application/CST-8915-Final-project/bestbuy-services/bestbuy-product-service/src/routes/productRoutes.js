const express = require('express');
const router = express.Router();
const Product = require('../models/product');  

// GET /api/products 
router.get('/', async (req, res) => {
  try {
    const products = await Product.find().lean(); 
    res.json(products);
  } catch (err) {
    console.error("Error fetching products:", err.message);
    res.status(500).json({ message: "Server error" });
  }
});

// GET /api/products/:id 
router.get('/:id', async (req, res) => {
  try {
    const product = await Product.findById(req.params.id).lean();

    if (!product) {
      return res.status(404).json({ message: 'Product not found' });
    }

    res.json(product);
  } catch (err) {
    console.error("Error fetching product:", err.message);
    res.status(500).json({ message: "Server error" });
  }
});

// POST /api/products 
router.post('/', async (req, res) => {
  try {
    const product = await Product.create(req.body);
    res.status(201).json(product);
  } catch (err) {
    console.error("Error creating product:", err.message);
    res.status(400).json({ message: "Invalid product data" });
  }
});

// PUT /api/products/:id  - update a product
router.put('/:id', async (req, res) => {
  try {
    const { id } = req.params;
// Find product by ID and update
    const updated = await Product.findByIdAndUpdate(id, req.body, {
      new: true,         
      runValidators: true 
    });

    if (!updated) {
      return res.status(404).json({ message: 'Product not found' });
    }

    res.json(updated);
  } catch (err) {
    console.error("Error updating product:", err.message);
    res.status(500).json({ message: "Server error while updating product" });
  }
});

// DELETE /api/products/:id  - delete a product
router.delete('/:id', async (req, res) => {
  try {
    const { id } = req.params;

    const deleted = await Product.findByIdAndDelete(id);

    if (!deleted) {
      return res.status(404).json({ message: 'Product not found' });
    }

    // 204 = No Content
    res.status(204).send();
  } catch (err) {
    console.error("Error deleting product:", err.message);
    res.status(500).json({ message: "Server error while deleting product" });
  }
});


module.exports = router;
