#servo_motor.py
import RPi.GPIO as GPIO
import time

SERVO_PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.pwm(SERVO_PIN, 50)
pwm.start(7.5) #0도

try:
    while True:
        value = input('1: 0도, 2: -90도, 3: +90도, 9:EXIT >')
        if value =='1':
            pwm.ChangeDutyCycle(7.5)
        elif value=='2':
            pwm.ChangeDutyCycle(2.5)
        elif value == '3':
            pwm.ChangeDutyCycle(12.5)
        elif value == '9':
            break
finally:
    pwm.stop()
    GPIO.cleanup()
    print("cleanop and exit")