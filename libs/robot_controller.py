"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    
    # TODO: Implement the Snatch3r class as needed when working the sandox exercises
    # (and delete these comments)
    def __init__(self):
        self.inches_moved = 0
        self.left_motor=ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.running = True
        self.ir_sensor = ev3.InfraredSensor()
        self.color_sensor = ev3.ColorSensor()
        assert self.color_sensor
        assert self.ir_sensor
        assert self.touch_sensor
        self.arm_motor.position = 0

    def drive_inches(self, inches_target, speed_deg_per_second):
        degrees_per_inch = 90
        motor_turns_needed_in_degrees = inches_target * degrees_per_inch

        self.left_motor.run_to_rel_pos(
            position_sp=motor_turns_needed_in_degrees,
                                  speed_sp=
                                  speed_deg_per_second, stop_action='brake')
        self.right_motor.run_to_rel_pos(
            position_sp=motor_turns_needed_in_degrees,
                                   speed_sp=
                                   speed_deg_per_second, stop_action='brake')
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

        ev3.Sound.beep()

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        motor_turns_needed_in_degrees = degrees_to_turn * 5.1
        speedright = turn_speed_sp
        speedleft = turn_speed_sp


        self.left_motor.run_to_rel_pos(
            position_sp= -1*motor_turns_needed_in_degrees,speed_sp=speedleft,
            stop_action='brake')
        self.right_motor.run_to_rel_pos(
            position_sp=motor_turns_needed_in_degrees,
            speed_sp=speedright,
            stop_action='brake')
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

        ev3.Sound.beep()


    def arm_calibration(self):
        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep()
        self.arm_motor.run_to_rel_pos(
            speed_sp=900, position_sp=-5100)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        print('motor is no longer running')
        ev3.Sound.beep()
        self.arm_motor.position = 0

    def arm_up(self):
        self.arm_motor.run_to_rel_pos(position_sp=5100, speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop()
        ev3.Sound.beep()

    def arm_down(self):
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=900)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()

    def right_forward(self, state, speed):
        if state:
            self.right_motor.run_forever(speed_sp=speed)
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        else:
            self.right_motor.stop()
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)

    def right_backward(self, state, speed):
        if state:
            self.right_motor.run_forever(speed_sp=-speed)
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
        else:
            self.right_motor.stop()
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)

    def left_forward(self, state, speed):
        if state:
            self.left_motor.run_forever(speed_sp=speed)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        else:
            self.left_motor.stop()
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)

    def left_backward(self, state, speed):
        if state:
            self.left_motor.run_forever(speed_sp=-speed)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
        else:
            self.left_motor.stop()
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)


    def shutdown(self):
        self.left_motor.stop()
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        self.right_motor.stop()
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        self.running = False
        print('Good Bye')
        ev3.Sound.speak("Good Bye")

    def loop_forever(self):
        while self.running:
            time.sleep(0.01)
