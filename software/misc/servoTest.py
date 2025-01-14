import RPi.GPIO as GPIO
import time

servoPin = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPin, GPIO.OUT)

p = GPIO.PWM(servoPin, 50)
p.start(2.5)
try:
	while True:
		p.ChangeDutyCycle(5)
		time.sleep(0.5)
		p.ChangeDutyCycle(12.5)
		time.sleep(0.5)
except KeyboardInterrupt:
	p.stop()
	GPIO.cleanup()
