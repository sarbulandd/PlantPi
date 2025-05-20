const mongoose = require("mongoose");
const { execSync } = require("child_process");
const SensorData = require("/home/pi/teamproject/SensorData.js");

const mongoURI = "mongodb+srv://Speianu:Porsche2002.@cluster0.jvcke.mongodb.net/Cluster0?retryWrites=true&w=majority";

async function connectDB() {
    await mongoose.connect(mongoURI);
    console.log("✅ Connected to MongoDB");
}

async function seedData() {
    try {
        console.log("\n📡 Reading from DHT11...");
        const dhtOutput = execSync("python3 /home/pi/teamproject/dht11.py").toString();
        console.log("📥 DHT11 Raw Output:", dhtOutput);
        const dhtData = JSON.parse(dhtOutput);

        console.log("🌱 Reading from Soil Sensor...");
        const soilOutput = execSync("python3 /home/pi/teamproject/SoilMoisture.py").toString();
        console.log("📥 Soil Sensor Raw Output:", soilOutput);
        const soilData = JSON.parse(soilOutput);

        const newData = new SensorData({
            temperature: dhtData.temperature_celsius,
            humidity: dhtData.humidity_percent,
            soilMoisture: soilData.moisture_value,
            soilStatus: soilData.moisture_status,
            timestamp: new Date()
        });

        await newData.save();
        console.log("✅ Sensor data inserted into MongoDB");

    } catch (error) {
        console.error("❌ Error during sensor read or DB insert:", error);
    }
}

// === Start Process ===
connectDB().then(() => {
    seedData(); // first call right away
    setInterval(seedData, 5000); // run every 5 seconds
});
