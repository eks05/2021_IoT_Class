import RPi.GPIO as GPIO
import time

BUZZER_PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

pwm = GPIO.PWM(BUZZER_PIN, 1)
pwm.start(10)

melody = [391, 391, 440, 440, 391, 391, 329, 391, 391, 329, 329, 294, 391, 391, 440, 440, 391, 391, 329, 391, 329, 293, 329, 262]    
try:
    for i in melody:
        pwm.ChangeFrequency(i)
        if i==melody[8]:
            time.sleep(1)
        elif i == melody[11]:
            time.sleep(2)    
        elif i==melody[18]:
            time.sleep(1)
        elif i == melody[23]:
            time.sleep(2)    
        else:
            time.sleep(0.5)

finally:
    pwm.stop()
    pwm.ChangeDutyCycle(0)
    GPIO.cleanup()
