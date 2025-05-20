import RPi.GPIO as GPIO
import json
import time

channel = 21  # GPIO pin where the soil sensor is connected

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

try:
    moisture_status = "DRY" if GPIO.input(channel) == GPIO.HIGH else "MOIST"
    print(json.dumps({
        "moisture_status": moisture_status,
        "moisture_value": 1 if moisture_status == "DRY" else 0  # binary value for example
    }))

finally:
    GPIO.cleanup()
