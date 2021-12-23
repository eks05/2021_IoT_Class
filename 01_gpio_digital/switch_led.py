#스위치로 LED 제어하기  
import RPi.GPIO as GPIO

LED_pin = 7
SWITCH_PIN = 12
print('good')

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_pin, GPIO.OUT)
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down= GPIO.PUD_DOWN)

try:
    while True:
        val = GPIO.input(SWITCH_PIN)#누르지 않았을 때 0, 누르면 1
        print(val)
        GPIO.output(LED_pin, val) #GPIO.HIGH = 1
finally:
    GPIO.cleanup()
    print("cleanup and exit")