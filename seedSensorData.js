// scripts/seedSensorData.js
const mongoose = require("mongoose");
const { execSync } = require("child_process");
const SensorData = require("/home/pi/teamproject/SensorData.js");

const mongoURI = "mongodb+srv://Speianu:Porsche2002.@cluster0.jvcke.mongodb.net/plant_monitor?retryWrites=true&w=majority";

async function getDHT11Data() {
    try {
        const output = execSync("python3 /home/pi/teamproject/dht11.py").toString();
        const match = output.match(/Temperature:\s*([\d.]+).*?Humidity:\s*([\d.]+)/);
        if (match) {
            return {
                temperature_celsius: parseFloat(match[1]),
                humidity_percent: parseFloat(match[2])
            };
        }
    } catch (err) {
        console.error("❌ Error reading DHT11:", err.message);
    }
    return { temperature_celsius: null, humidity_percent: null };
}

async function getSoilMoistureData() {
    try {
        const output = execSync("python3 /home/pi/teamproject/soilmoisture.py").toString();
        const match = output.match(/Moisture:\s*(\d+).*?Status:\s*(\w+)/i);
        if (match) {
            return {
                moisture_value: parseInt(match[1]),
                moisture_status: match[2].toUpperCase()
            };
        }
    } catch (err) {
        console.error("❌ Error reading soil moisture:", err.message);
    }
    return { moisture_value: null, moisture_status: "UNKNOWN" };
}

async function seedData() {
    await mongoose.connect(mongoURI);
    console.log("✅ Connected to MongoDB");

    const dhtData = await getDHT11Data();
    const soilData = await getSoilMoistureData();

    const document = {
        timestamp: new Date(),
        ...dhtData,
        ...soilData
    };

    await SensorData.insertMany([document]);
    console.log("🌱 Live sensor data inserted!");

    mongoose.disconnect();
}

seedData().catch(err => {
    console.error("❌ Error seeding data:", err);
});
