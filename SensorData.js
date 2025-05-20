const mongoose = require('mongoose');

const sensorSchema = new mongoose.Schema({
  timestamp: { type: String, required: true },
  moisture_value: Number,
  moisture_status: String,
  temperature_celsius: Number,
  humidity_percent: Number
});

module.exports = mongoose.model('SensorData', sensorSchema);
