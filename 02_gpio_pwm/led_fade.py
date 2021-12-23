import RPi.GPIO as GPIO
import time

LED_PIN = 7
GPIO.setmode (GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

#PWM 인스턴스 생성
#주파수설정 : 50Hz
PWM = GPIO.PWM(LED_PIN, 50)
PWM.start(0) # duty cycle 0~100

try:
    for i in range(3):
        #서서히 켜짐   
        for j in range(0, 101, 5): # start, end, step
            PWM.ChangeDutyCycle(j)
            time.sleep(0.1)
        for j in range(100, -1, -5): 
            PWN.ChangeDutyCycle(j)
            time.sleep(0.1)
finally:
    PWM.stop()
    GPIO.cleanup()
    print("cleanup and exit")