#ultra_sonic.py
import RPi.GPIO as GPIO
import time

TRIGGER_PIN = 4
ECHO_PIN = 14
LED_PIN = 10

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(TRIGGER_PIN, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIGGER_PIN, GPIO.LOW)

        while GPIO.input(ECHO_PIN) == 0:
            pass
        start = time.time()

        while GPIO.input(ECHO_PIN) == 1:
            pass
        end = time.time()

        duration_time = stop - start

        distance = 17180 * duration_time

        print('Distance : %.1fcm', distance)

        if distance <=20:
            GPIO.OUTPUT(LED_PIN, GPIO.HIGH)
            print("LED ON")
        else :
            GPIO.OUTPUT(LED_PIN, GPIO.LOW)
            print("LED OFF")

        time.sleep(0.1)
finally:
    GPIO.cleanup()
    print("cleanup and exit")