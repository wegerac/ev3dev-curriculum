#!/usr/bin/env python3


import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time

class Ev3Delegate(object):
    def __init__(self):
        self.running = True
        self.mqtt_client = None
        self.robot = robo.Snatch3r()

    def right_forward(self, state, speed):
        robo.Snatch3r.right_forward(self.robot, state, speed)

    def right_backward(self, state, speed):
        robo.Snatch3r.right_backward(self.robot, state, speed)

    def left_forward(self, state, speed):
        robo.Snatch3r.left_forward(self.robot, state, speed)

    def left_backward(self, state, speed):
        robo.Snatch3r.left_backward(self.robot, state, speed)

    def shutdown(self):
        self.robot.shutdown()

    def find_grail(self):
        bool = self.robot.seek_beacon()
        if bool == True:
            self.robot.arm_up()
            self.robot.turn_degrees(360, 800)
            ev3.Sound.speak('I found it!')
            ev3.Sound.speak('Ha')
            ev3.Sound.speak('Ha')
            ev3.Sound.speak('I will rule them all!')



def main():
    print("********************************")
    print("RUNNING")
    print("********************************")


    my_delegate = Ev3Delegate()
    mqtt_client = com.MqttClient(my_delegate)
    my_delegate.mqtt_client = mqtt_client
    mqtt_client.connect_to_pc()

    my_delegate.robot.arm_calibration()

    beacon = ev3.BeaconSeeker(channel= 1)

    while True:

        if my_delegate.robot.color_sensor.color == ev3.ColorSensor.COLOR_BLUE:
                found_stone(mqtt_client, 0)
                time.sleep(4)
                continue

        elif my_delegate.robot.color_sensor.color == ev3.ColorSensor.COLOR_GREEN:
            found_stone(mqtt_client, 1)
            time.sleep(4)
            continue

        elif my_delegate.robot.color_sensor.color == ev3.ColorSensor.COLOR_RED:
            found_stone(mqtt_client, 2)
            time.sleep(4)
            continue

        elif beacon.distance >= 0:
            mqtt_client.send_message('grail_in_sight')
            time.sleep(2)

        elif my_delegate.robot.touch_sensor.is_pressed:
            ev3.Sound.speak('break')
            break



def send_string(mqtt, state):
    if state:
        mqtt.send_message('found_item', [0])
        print("got")

def found_stone(mqtt, stone_code):
    mqtt.send_message('found_item', [stone_code])


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
