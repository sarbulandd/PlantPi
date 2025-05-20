const mongoose = require("mongoose");
const { execSync } = require("child_process");
const SensorData = require("/home/pi/teamproject/SensorData.js");

const mongoURI = "mongodb+srv://Speianu:Porsche2002.@cluster0.jvcke.mongodb.net/Cluster0?retryWrites=true&w=majority";

async function seedData() {
    await mongoose.connect(mongoURI);
    console.log("✅ Connected to MongoDB");

    try {
        // === Read from DHT11 sensor ===
        console.log("📡 Reading from DHT11...");
        const dhtOutput = execSync("python3 /home/pi/teamproject/dht11.py").toString();
        console.log("📥 DHT11 Raw Output:", dhtOutput);
        const dhtData = JSON.parse(dhtOutput);

        // === Read from Soil Moisture sensor ===
        console.log("🌱 Reading from Soil Sensor...");
        const soilOutput = execSync("python3 /home/pi/teamproject/SoilMoisture.py").toString();
        console.log("📥 Soil Sensor Raw Output:", soilOutput);
        const soilData = JSON.parse(soilOutput);

        // Create sensor data document
        const document = new SensorData({
            temperature: dhtData.temperature_celsius,
            humidity: dhtData.humidity_percent,
            soilMoisture: soilData.moisture_value,
            soilMoistureStatus: soilData.moisture_status,
            timestamp: new Date()
        });

        console.log("📝 Saving to MongoDB...");
        await document.save();
        console.log("🌱 Real sensor data inserted into MongoDB!");
    } catch (err) {
        console.error("❌ Error during sensor read or DB insert:", err);
    }

    await mongoose.disconnect();
    console.log("🔌 Disconnected from MongoDB");
}

seedData();
