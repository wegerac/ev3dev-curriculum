#!/usr/bin/env python3
'''Final project for CSSE120 Winter 2017-18
Uses a robot to "find gems"
Author: Andrew Weger Feb 12-19, 2018
'''

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
        '''Gets the state and speed from the message sent with mqtt
        and calls the function right_forward in the robot controller file.
        If state is True, the motor will run forwards, and if False, the motor will stop.'''
        robo.Snatch3r.right_forward(self.robot, state, speed)

    def right_backward(self, state, speed):
        '''Gets the state and speed from the message sent with mqtt
        and calls the function right_backward in the robot controller file.
        If state is True, the right motor will run backwards, and if False, the motor will stop.'''
        robo.Snatch3r.right_backward(self.robot, state, speed)

    def left_forward(self, state, speed):
        '''Gets the state and speed from the message sent with mqtt
        and calls the function left_forward in the robot controller file.
        If state is True, the motor will run forwards, and if False, the motor will stop.'''
        robo.Snatch3r.left_forward(self.robot, state, speed)

    def left_backward(self, state, speed):
        '''Gets the state and speed from the message sent with mqtt
        and calls the function left_backward in the robot controller file.
        If state is True, the right motor will run backwards, and if False, the motor will stop.'''
        robo.Snatch3r.left_backward(self.robot, state, speed)

    def shutdown(self):
        '''Gets a message from mqtt to call the robots shutdown function.'''
        self.robot.shutdown()

    def find_grail(self):
        '''Finds the "grail", actually the controller in beacon mode, using the seek_beacon
        function in the robot_controller file. When the robot finds the "grail" it sends a
        mqtt message to call the win function on the pc to end the game.'''
        seek = self.robot.seek_beacon()
        if seek == True:
            self.robot.arm_up()
            self.robot.turn_degrees(360, 800)
            ev3.Sound.speak('I found it!')
            ev3.Sound.speak('Ha')
            ev3.Sound.speak('Ha')
            ev3.Sound.speak('I will rule them all!')
            self.mqtt_client.send_message('win')

    def arm_down(self):
        '''Gets the message from the mqtt_client to call the arm_down function in the robots class'''
        self.robot.arm_down()

    def arm_up(self):
        '''Gets the message from the mqtt_client to call the arm_up function in the robots class'''
        self.robot.arm_up()

    def calibrate(self):
        '''Gets the message from the mqtt_client to call the arm_calibration function in the robots class '''
        self.robot.arm_calibration()



def main():
    '''This creates the looping code for the game, and also the delegate and mqtt_client. It will continually run the color sensor
    and if it returns one of the desired values, it will send a mqtt message to the client of what it found.
    When a color is found the robot send a mqtt message to the computer with its "jewl code", 0-sapphire/1-emerald/2-ruby.'''
    print("********************************")
    print("PROGRAM RUNNING")
    print("********************************")


    my_delegate = Ev3Delegate()
    mqtt_client = com.MqttClient(my_delegate)
    my_delegate.mqtt_client = mqtt_client
    mqtt_client.connect_to_pc()

    #my_delegate.robot.arm_calibration()

    btn = ev3.Button()

    beacon = ev3.BeaconSeeker(channel=1)

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

        elif btn.left:
            my_delegate.robot.shutdown()
            break


def found_stone(mqtt, stone_code):
    '''This sends a mqtt message to the client, the computer, which will send the stone code, same as the ones above.'''
    mqtt.send_message('found_item', [stone_code])


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
