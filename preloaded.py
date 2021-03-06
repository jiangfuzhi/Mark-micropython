from gpio import *
from modules import ws2812
from maix_motor import Maix_motor
import utime
import time
from camera import *
from object_detection import *

traffic_classes = ["limit_5","limit_80","no_forward","forward","left","right","u_turn","zebra","stop","yield"]
traffic_anchor = (0.57273, 0.677385, 1.87446, 2.06253, 3.33843, 5.47434, 7.88282, 3.52778, 9.77052, 9.16828)
traffic_filename = 0x400000
traffic = ObjectDetection(traffic_filename, traffic_classes, traffic_anchor, 1)

class globalvals:
    state = 0
    i = 0
    result = 0


ws2812_2 = ws2812(fm.board_info.D[13],5,2,3)


def start_handler_0():
    pass
    globalvals.state = 0
    for globalvals.i in range(0, 255 + 1, 5):
        time.sleep(0.02)
        ws2812_2.set_led(0,(0, globalvals.i, 0))
        ws2812_2.display()
        ws2812_2.set_led(1,(0, globalvals.i, 0))
        ws2812_2.display()
    for globalvals.i in range(90, 0 + 1, -3):
        time.sleep(0.02)
        Maix_motor.servo_angle(2, globalvals.i)
        Maix_motor.servo_angle(1, globalvals.i)
    utime.sleep_ms(200)
    for globalvals.i in range(0, 180 + 1, 3):
        time.sleep(0.02)
        Maix_motor.servo_angle(2, globalvals.i)
        Maix_motor.servo_angle(1, globalvals.i)
    utime.sleep_ms(200)
    for globalvals.i in range(180, 90 + 1, -3):
        time.sleep(0.02)
        Maix_motor.servo_angle(2, globalvals.i)
        Maix_motor.servo_angle(1, globalvals.i)
    speaker(3, 2, 1/8)
    speaker(3, 9, 1/8)
    speaker(3, 18, 1/8)
    speaker(3, 9, 1/8)
    speaker(3, 18, 1/8)
    if traffic.is_object("forward", 50):
        globalvals.state = 2
    if Line_Finder(5, 1) and Line_Finder(6, 1):
        globalvals.state = 1
    while True:
        time.sleep(0.02)
        if globalvals.state == 0:
            Maix_motor.motor_run(0, 0, 0)
            if traffic.is_object("forward", 50):
                globalvals.state = 2
            if Line_Finder(5, 1) and Line_Finder(6, 1):
                globalvals.state = 1
        if globalvals.state == 1:
            if Line_Finder(5, 1) and Line_Finder(6, 1):
                Maix_motor.motor_motion(1, 1, 0)
            else:
                if Line_Finder(5, 1):
                    Maix_motor.motor_motion(1, 3, 0)
                if Line_Finder(6, 1):
                    Maix_motor.motor_motion(1, 4, 0)
            if traffic.is_object("stop", 50):
                globalvals.state = 0
        if globalvals.state == 2:
            globalvals.result = traffic.get_detection_results(50)
            if str("left") in str(globalvals.result):
                Maix_motor.motor_motion(1, 4, 0)
            if str("right") in str(globalvals.result):
                Maix_motor.motor_motion(1, 3, 0)
            if str("forward") in str(globalvals.result):
                Maix_motor.motor_motion(1, 1, 0)
            if str("stop") in str(globalvals.result):
                globalvals.state = 0


lcd.display(image.Image('preloaded.jpg'))
time.sleep(1)
start_handler_0()

