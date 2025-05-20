import adafruit_dht
import board
import json

# Set up the DHT11 sensor on GPIO pin D4
dht_device = adafruit_dht.DHT11(board.D4)

try:
    temperature = dht_device.temperature
    humidity = dht_device.humidity

    if temperature is not None and humidity is not None:
        print(json.dumps({
            "temperature_celsius": temperature,
            "humidity_percent": humidity
        }))
    else:
        print(json.dumps({
            "error": "Failed to retrieve data"
        }))

except Exception as e:
    print(json.dumps({"error": str(e)}))

finally:
    dht_device.exit()
