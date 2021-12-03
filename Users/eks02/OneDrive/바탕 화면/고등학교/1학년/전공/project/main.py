import RPi.GPIO as GPIO
from flask import Flask, render_template
import time
from flask_cors import CORS
from lcd import drivers
import threading


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
###########################################
TRIG = 23   # 트리거 핀번호
ECHO = 24   # 에코 핀번호

LED_LEFT = 11   # 좌측 LED 핀번호
LED_RIGHT = 10  # 우측 LED 핀번호
display = drivers.Lcd()

##########################################
app = Flask(__name__)
CORS(app)
CORS(app, resources={r'*': {'origins': 'http://192.168.137.6:5000/'}})
#####################################################
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.setup(LED_LEFT, GPIO.OUT)
GPIO.setup(LED_RIGHT, GPIO.OUT)
###################################################

RIGHT_FORWARD = 26
RIGHT_BACKWARD = 19
RIGHT_PWM = 13  # 오른쪽 모터 핀번호

LEFT_FORWARD = 21
LEFT_BACKWARD = 20
LEFT_PWM = 16   # 왼쪽 모터 핀번호


# 오른쪽 모터 PWM 핀번호 출력용으로 설정
GPIO.setup(RIGHT_FORWARD, GPIO.OUT)                  
GPIO.setup(RIGHT_BACKWARD, GPIO.OUT)
GPIO.setup(RIGHT_PWM, GPIO.OUT)
GPIO.output(RIGHT_PWM, 0)
RIGHT_MOTOR = GPIO.PWM(RIGHT_PWM, 100)  # 모터 주파수 100으로 설정
RIGHT_MOTOR.start(0)
RIGHT_MOTOR.ChangeDutyCycle(0)          # 모터 출력값 0으로 초기화

# 왼쪽 모터 PWM 핀번호 출력용으로 설정
GPIO.setup(LEFT_FORWARD,GPIO.OUT)                  
GPIO.setup(LEFT_BACKWARD,GPIO.OUT)
GPIO.setup(LEFT_PWM, GPIO.OUT)
GPIO.output(LEFT_PWM, 0)
LEFT_MOTOR = GPIO.PWM(LEFT_PWM, 100)    # 모터 주파수 100으로 설정
LEFT_MOTOR.start(0)
LEFT_MOTOR.ChangeDutyCycle(0)           # 모터 출력값 0으로 초기화

#전진
def forward():
    rightMotor(1, 0, 80)
    leftMotor(1, 0, 80)


#우회전
def right():
    rightMotor(0, 0, 0)
    leftMotor(1, 0, 80)
    time.sleep(0.3)
    GPIO.output(LED_RIGHT, GPIO.HIGH)
    time.sleep(0.3)
    GPIO.output(LED_RIGHT, GPIO.LOW)

#좌회전
def left():
    rightMotor(1, 0, 80)
    leftMotor(0, 0, 0)
    GPIO.output(LED_LEFT, GPIO.HIGH)
    time.sleep(0.3)
    GPIO.output(LED_LEFT, GPIO.LOW) 

#거리 구하는 함수
def getDistance():
    GPIO.output(TRIG, GPIO.LOW)
    time.sleep(1)

    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    #에코가 꺼졌을 때 펄스시간 시작
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    #에코가 켜졌을 때 펄스시간 끝내기
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    #펄스 지속시간 구하기
    pulse_duration = pulse_end - pulse_start
    #거리 구하기
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

# 우측 모터 제어
def rightMotor(forward, backward, pwm):
    GPIO.output(RIGHT_FORWARD, forward)
    GPIO.output(RIGHT_BACKWARD, backward)
    RIGHT_MOTOR.ChangeDutyCycle(pwm)


# 좌측 모터 제어
def leftMotor(forward, backward, pwm):
    GPIO.output(LEFT_FORWARD, forward)
    GPIO.output(LEFT_BACKWARD, backward)
    LEFT_MOTOR.ChangeDutyCycle(pwm)

#정지
def brake():
    for _ in range(500):
        rightMotor(0, 0, 0)
        leftMotor(0, 0, 0)
        time.sleep(0.01)


#AEB
def AEB():
    rightMotor(0, 0, 0)
    leftMotor(0, 0, 0)
    lcd("stop")

#lcd 출력
def lcd(op):
    if op == "front":
        display.lcd_display_string("Going Front",1)
        return
    elif op == "back":
        display.lcd_display_string("Going  Back",1)
        return
    elif op == "stop":
        display.lcd_display_string("****STOP****",1)
        return
    elif op == 'right':
        display.lcd_display_string("Going Right",1)
        return
    elif op == 'left':
        display.lcd_display_string("Going  Left",1)
        return


@app.route("/")
def action():
    return render_template("index.html")
    

@app.route("/go/<direct>")
def move(direct):
    if direct == "front":
        while direct == "front":
            time.sleep(0.1)
            distance_value = getDistance()
            if distance_value < 40: # 차체가 40cm이내에서 장애물을 감지하면 AEB를 실행한다.
                AEB()
                return "AEB"
                break
            else:
                lcd("front")
                forward()
    if direct == "stop":
        lcd("stop")
        brake()
    if direct == "right":
        right()
        lcd("right")
    if direct == "left":
        left()
        lcd("left")
    return "success"
if __name__ == "__main__":
    app.run(host="0.0.0.0")

GPIO.cleanup()
