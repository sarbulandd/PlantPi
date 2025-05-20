const express = require('express');
const router = express.Router();
const SensorData = require('../models/SensorData');

// POST: Pi sends data
router.post('/', async (req, res) => {
  try {
    const newEntry = new SensorData(req.body);
    await newEntry.save();
    res.status(201).send("✅ Data saved");
  } catch (err) {
    console.error("❌ Save error:", err);
    res.status(500).send("Error saving data");
  }
});

// GET: React Native app fetches data
router.get('/', async (req, res) => {
  try {
    const data = await SensorData.find().sort({ timestamp: -1 }).limit(10);
    res.json(data);
  } catch (err) {
    console.error("❌ Fetch error:", err);
    res.status(500).send("Error fetching data");
  }
});

module.exports = router;
