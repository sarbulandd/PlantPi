import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)

try:
	while True:
		sensor_value = GPIO.input(21)
		print("Sensor State", sensor_value)
		time.sleep(1)
except KeyboardInterrupt:
	GPIO.cleanup()
	print("stopping")
	
