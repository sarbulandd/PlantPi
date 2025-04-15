import RPi.GPIO as GPIO  #pins on raspberry pi: this library functions can control them
import time

#GPIO setup
GPIO.cleanup()
channel = 21 # what pin sensor is connected to
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)#will expect inputs from this pin

def sensor(channel):
	if GPIO.input(channel) == GPIO.HIGH:#component light is off and soil is too dry (high)
		print("Soil is DRY")
	else:#component light is on as mositure is detected 
		print("soil is moist")
		
		

		
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300) #lets us know when pin is too high or low 
sudoGPIO.add_event_callback(channel, sensor) #assign function to GPIO pin tun funtion on change

try: # to keep the program running
	while True:
		time.sleep(1)

except KeyboardInterrupt: # to stop the program
	print("Stopping")
	GOIO.cleanup()
	
