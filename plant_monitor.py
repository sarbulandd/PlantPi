import spidev
import time
from datetime import datetime
from pymongo import MongoClient
import board
import adafruit_dht

# === MongoDB Setup ===
MONGO_URI = "mongodb+srv://Speianu:Porsche2002.@cluster0.jvcke.mongodb.net/Cluster0?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["plant_monitor"]
collection = db["sensor_data"]

# === SPI Setup for MCP3008 (Soil Sensor) ===
spi = spidev.SpiDev()
spi.open(0, 0)  # bus 0, CE0
spi.max_speed_hz = 1350000

# === DHT11 Setup ===
dhtDevice = adafruit_dht.DHT11(board.D4)  # GPIO 4

def read_adc(channel):
    if not 0 <= channel <= 7:
        raise ValueError("ADC channel must be 0-7")
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def get_moisture_level(value):
    if value > 800:
        return "DRY"
    elif value < 400:
        return "WET"
    else:
        return "MOIST"

try:
    while True:
        # Read soil moisture
        moisture_value = read_adc(0)
        moisture_status = get_moisture_level(moisture_value)

        # Read DHT11
        try:
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity
        except RuntimeError as error:
            print(f"DHT11 read error: {error.args[0]}")
            temperature = None
            humidity = None

        timestamp = datetime.now()

        print(f"\n{timestamp}")
        print(f"Soil Moisture: {moisture_value} ({moisture_status})")
        print(f"Temperature: {temperature}°C | Humidity: {humidity}%")

        # Document to insert
        document = {
            "timestamp": timestamp,
            "moisture_value": moisture_value,
            "moisture_status": moisture_status,
            "temperature_celsius": temperature,
            "humidity_percent": humidity
        }

        collection.insert_one(document)
        print("Data sent to MongoDB Atlas ✅")

        time.sleep(10)

except KeyboardInterrupt:
    print("Stopping monitoring...")
    spi.close()
    client.close()
