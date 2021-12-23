import RPi.GPIO as GPIO

RED_LPIN = 4
RED_SPIN = 17
YEL_LPIN = 23
YEL_SPIN = 27
GRE_LPIN = 24
GRE_SPIN = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_LPIN, GPIO.OUT)
GPIO.setup(YEL_LPIN, GPIO.OUT)
GPIO.setup(GRE_LPIN, GPIO.OUT)
GPIO.setup(RED_SPIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(YEL_SPIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(GRE_SPIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

try:
    while True:
        val_red = GPIO.input(RED_SPIN) #누르지 않았을 때는 0, 눌렀을 떄는 1
        val_yel = GPIO.input(YEL_SPIN)
        val_gre = GPIO.input(GRE_SPIN)

        
        GPIO.output(RED_LPIN, val_red) #GPIO.HIGH = 1
        GPIO.output(YEL_LPIN, val_yel)
        GPIO.output(GRE_LPIN, val_gre)

finally:
    GPIO.cleanup()
    print("cleanup and exit")

# Red_Led = 4
# Yellow_Led = 23
# Green_Led = 24
# red_btn = 17
# yel_btn = 27
# gre_btn = 22