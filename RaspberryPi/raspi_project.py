# raspi_project.py
import RPi.GPIO as GPIO
import time
import spidev

buzzer = 17
LED_PIN = 18
Gled_pin= 14
trig = 27
echo = 19

HUM_THRESHOLD = 20

HUM_MAX = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(Gled_pin, GPIO.OUT)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

GPIO.setmode(GPIO.BCM)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 500000

def read_spi_adc(adcChannel):
    adcValue = 0
    buff = spi.xfer2([1,(8+adcChannel)<<4,0])
    adcValue = ((buff[1]&3)<<8)+buff[2]
    return adcValue
def map(value, min_adc, max_adc,min_hum, max_hum):
    adc_range = max_adc-min_adc
    hum_range= max_hum-min_hum
    scale_factor = float(adc_range)/float(hum_range)
    return min_hum+((value-min_adc)/scale_factor)

try:
    
    adcChannel = 0

    while True:
        GPIO.output(Gled_pin, GPIO.HIGH)
        GPIO.output(trig, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(trig, GPIO.LOW)

        while GPIO.input(echo) == 0:
            pass
        start = time.time()

        while GPIO.input(echo) == 1:
            pass
        stop = time.time()

        duration_time = stop - start        #초음파가 들어온시간 - 나간시간(지속시간)

        distance = 17180 * duration_time    #초음파센서 거리구하는 공식

        adcValue = read_spi_adc(adcChannel)
        hum = 100-int(map(adcValue, HUM_MAX,1023,0,100))    # 수분을 구하는 부분
        
        if hum < HUM_THRESHOLD :    # 센서에서 수분이 기준 이하로 측정될 때
            if distance <=30:       # 사용자가 물을 주려고 다가오면 잠시 소리와 LED를 끕니다. 
                print("움직임 감지")
                GPIO.output(buzzer, GPIO.LOW)
                GPIO.output(LED_PIN, GPIO.LOW)
            elif distance>30:
                GPIO.output(Gled_pin, GPIO.LOW)
                GPIO.output(buzzer, GPIO.HIGH)
                GPIO.output(LED_PIN, GPIO.HIGH)
                print("움직임 없음")
                time.sleep(0.1)
        else:
            GPIO.output(buzzer, GPIO.LOW)
            print("enough water")
            time.sleep(60)          # 수분이 기준이상을 충족시키면 60초의 딜레이를 주고, 60초 후 부터 다시 수분측정을 시작합니다. 

finally:
    GPIO.cleanup() #GPIO 핀 상태 초기화