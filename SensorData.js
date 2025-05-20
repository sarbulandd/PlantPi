const mongoose = require("mongoose");

const sensorDataSchema = new mongoose.Schema({
    temperature: Number,
    humidity: Number,
    soilMoisture: Number,
    soilMoistureStatus: String,
    timestamp: Date
});

module.exports = mongoose.model("SensorData", sensorDataSchema);
