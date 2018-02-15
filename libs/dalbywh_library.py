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
        """Establishes a left, right, and arm motor. Establishes the sensors
        (touch, ir, and color) sensors. Establishes the pixy camera. Sets
        inches moved to zero. Sets the state of running to be true. This all
        only occurs when the sensors are connected."""
        self.inches_moved = 0
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
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
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        assert self.pixy

    def drive_inches(self, inches_target, speed_deg_per_second):
        """Drives so far in inches at a speed in degrees per second. A
        negative distance will make the robot travel backwards."""
        degrees_per_inch = 90
        motor_turns_needed_in_degrees = inches_target * degrees_per_inch

        self.left_motor.run_to_rel_pos(
            position_sp=motor_turns_needed_in_degrees,
            speed_sp=speed_deg_per_second, stop_action='brake')
        self.right_motor.run_to_rel_pos(
            position_sp=motor_turns_needed_in_degrees,
            speed_sp=speed_deg_per_second, stop_action='brake')
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

        ev3.Sound.beep()

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        """Turns the robot a certain number of degrees LEFT from its
        original orientation IF the degrees to turn value is positive. Will
        turn RIGHT if the degrees to turn is negative. Turns at a speed in
        degrees per second."""
        motor_turns_needed_in_degrees = degrees_to_turn * 5.1
        speedright = turn_speed_sp
        speedleft = turn_speed_sp

        self.left_motor.run_to_rel_pos(position_sp=-1*motor_turns_needed_in_degrees,
                                       speed_sp=speedleft, stop_action='brake')
        self.right_motor.run_to_rel_pos(
            position_sp=motor_turns_needed_in_degrees,
            speed_sp=speedright,
            stop_action='brake')
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

        ev3.Sound.beep()

    def arm_calibration(self):
        """Raises the arm until the touch sensor is pressed and then lowers
        the arm 5100 degrees (the amount to make the arm reset). Upon
        completing this cycle the zero position for the encoders is reset."""
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
        """Raises the arm until the touch sensor is pressed"""
        self.arm_motor.run_to_rel_pos(position_sp=5100, speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop()
        ev3.Sound.beep()

    def arm_down(self):
        """lowers the arm until the encoders are reset to zero."""
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=900)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()

    def right_forward(self, state, speed):
        """Moves the right motor forward upon a button press. The motor moves
        at a speed in degrees per second."""
        if state:
            self.right_motor.run_forever(speed_sp=speed)
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        else:
            self.right_motor.stop()
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)

    def right_backward(self, state, speed):
        """Moves the right motor backward upon a button press. The motor
        moves at a speed in degrees per second"""
        if state:
            self.right_motor.run_forever(speed_sp=-speed)
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
        else:
            self.right_motor.stop()
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)

    def left_forward(self, state, speed):
        """Moves the left motor forward upon a button press. The motor moves
                at a speed in degrees per second."""
        if state:
            self.left_motor.run_forever(speed_sp=speed)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        else:
            self.left_motor.stop()
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)

    def left_backward(self, state, speed):
        """Moves the left motor backward upon a button press. The motor moves
                at a speed in degrees per second."""
        if state:
            self.left_motor.run_forever(speed_sp=-speed)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
        else:
            self.left_motor.stop()
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)

    def stop(self):
        """Stops both of the drive motors by making them brake.
        The robot is not shut down"""
        self.right_motor.stop(stop_action='brake')
        self.left_motor.stop(stop_action='brake')

    def shutdown(self):
        """Stops both of the motors. Sets the robots LEDs to green. Sets the
        running state to false to break the while loop. Prints 'Good Bye' on
        the computer side and the robot speaks 'Good Bye' """
        self.left_motor.stop()
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        self.right_motor.stop()
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        self.running = False
        print('Good Bye')
        ev3.Sound.speak("Good Bye")

    def loop_forever(self):
        """Allows the robot to run so long as self.running is true."""
        while self.running:
            time.sleep(0.01)

    def seek_beacon(self):
        """
        Uses the IR Sensor in BeaconSeeker mode to find the beacon.  If the beacon is found this return True.
        If the beacon is not found and the attempt is cancelled by hitting the touch sensor, return False.

        """

        beacon_sensor = ev3.BeaconSeeker(channel=1)
        forward_speed = 300
        turn_speed = 100

        while not self.touch_sensor.is_pressed:
            current_heading = beacon_sensor.heading
            current_distance = beacon_sensor.distance
            if current_distance == -128:
                print("IR Remote not found. Distance is -128")
                self.stop()
            else:
                if math.fabs(current_heading) < 2:
                    print("On the right heading. Distance: ", current_distance)
                    if current_distance == 0:
                        self.right_forward(True, forward_speed)
                        self.left_forward(True, forward_speed)
                        time.sleep(0.4)
                        self.stop()
                        return True
                    elif current_distance > 0:
                        print("Beacon is in front of the robot.")
                        self.right_forward(True, forward_speed)
                        self.left_forward(True, forward_speed)
                elif math.fabs(current_heading) > 2 and math.fabs(
                                                current_heading) < 10:
                    if current_heading < 0:
                        print("Beacon is on the left.")
                        self.right_forward(True, turn_speed)
                        self.left_backward(True, turn_speed)
                    else:
                        print("Beacon is on the right.")
                        self.right_backward(True, turn_speed)
                        self.left_forward(True, turn_speed)
                elif math.fabs(current_heading) > 10:
                    self.stop()
                    print('Heading too far off.')
            time.sleep(0.01)

        print("Abandon ship!")
        self.stop()
        return False
