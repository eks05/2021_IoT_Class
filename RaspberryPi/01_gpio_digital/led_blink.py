import RPi.GPIO as GPIO
import time

LED_PIN = 4
GPIO.setmode(GPIO.BCM) #GPIO.BCM or GPIO.BOARD
GPIO.setup(LED_PIN, GPIO.OUT)



for i in range (10):
    GPIO.output(LED_PIN, GPIO.HIGH) # 1
    print("LED ON")
    time.sleep(0.5)
    GPIO.output(LED_PIN, GPIO.LOW) #0
    print("LED OFF")
    time.sleep(0.5)

GPIO.cleanup() #GPIO 핀 상태 초기화