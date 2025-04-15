import adafruit_dht
import board
import time

# Set up the DHT11 sensor on GPIO pin D4
dht_device = adafruit_dht.DHT11(board.D4)

def read_sensor():
    while True:
        try:
            # Attempt to read the temperature and humidity from the sensor
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            
            # Check if the sensor readings are valid
            if temperature is not None and humidity is not None:
                print(f"Temperature: {temperature}°C, Humidity: {humidity}%")
            else:
                print("Failed to retrieve data. Retrying...")
        
        except RuntimeError as e:
            # Handle runtime errors that may occur during sensor reading
            print(f"RuntimeError: {e}. Retrying...")
        
        except Exception as e:
            # Handle other unexpected errors
            print(f"Unexpected error: {e}")
        
        time.sleep(2)  # Delay before retrying the sensor read

if __name__ == "__main__":
    print("Starting DHT11 sensor readings...")
    try:
        read_sensor()
    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        dht_device.exit()  # Make sure to clean up the sensor when done
