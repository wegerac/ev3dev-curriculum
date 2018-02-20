
import ev3dev.ev3 as ev3
import time


class Traveler(object):

    def __init__(self):
        """Establishes a left, right, and arm motor. Establishes the sensors
        (touch, ir, and color) sensors. Establishes the pixy camera. Sets
        inches moved to zero. Sets the state of running to be true,
        direction to be up, and tracking to be false. This all
        only occurs when the sensors are connected."""
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.running = True
        self.find = False
        self.ir_sensor = ev3.InfraredSensor()
        self.color_sensor = ev3.ColorSensor()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        assert self.color_sensor
        assert self.ir_sensor
        assert self.touch_sensor
        assert self.pixy
        self.x = 200
        self.y = 200
        self.direction = 'up'

    def start(self):
        """starts  the program by resetting all of the variables and
        starting the motors this is used when resetting the robot to center
        position to restart without restarting the program"""
        self.find = True
        self.right_motor.run_forever(speed_sp=600)
        self.left_motor.run_forever(speed_sp=600)
        self.direction = 'up'
        self.x = 200
        self.y = 200

    def forward(self):
        """Makes the robot move forward at speed of 600 degrees per second"""
        self.right_motor.run_forever(speed_sp=600)
        self.left_motor.run_forever(speed_sp=600)

    def turn_around(self):
        """this function turn off tracking so the robot knows that it is not
        moving and then turn 180 degrees to face the opposite direction before
        returning to tracking its position position of motors were found
        using results from drive motors code and changes the direction state"""
        self.find = False
        self.left_motor.run_to_rel_pos(position_sp=-930, speed_sp=600,
                                       stop_action='brake')
        self.right_motor.run_to_rel_pos(position_sp=930, speed_sp=600,
                                        stop_action='brake')
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        if self.direction == 'up':
            self.direction = 'down'
        elif self.direction == 'right':
            self.direction = 'left'
        elif self.direction == 'down':
            self.direction = 'up'
        elif self.direction == 'left':
            self.direction = 'right'
        time.sleep(1)
        self.find = True

    def corner_left(self):
        """this function turn off tracking so the robot knows that it is not
        moving and then turn 90 degrees left before returning to tracking its
         position position of motors were found using results from drive motors
          code and changes the direction state"""
        self.find = False
        self.left_motor.run_to_rel_pos(position_sp=-470, speed_sp=600,
                                       stop_action='brake')
        self.right_motor.run_to_rel_pos(position_sp=470, speed_sp=600,
                                        stop_action='brake')
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        if self.direction == 'up':
            self.direction = 'right'
        elif self.direction == 'right':
            self.direction = 'down'
        elif self.direction == 'down':
            self.direction = 'left'
        elif self.direction == 'left':
            self.direction = 'up'
        time.sleep(.6)
        self.find = True

    def corner_right(self):
        """this function turn off tracking so the robot knows that it is not
        moving and then turn 90 degrees right before returning to tracking its
         position position of motors were found using results from drive motors
          code and changes the direction state"""
        self.find = False
        self.left_motor.run_to_rel_pos(position_sp=470, speed_sp=600,
                                       stop_action='brake')
        self.right_motor.run_to_rel_pos(position_sp=-470, speed_sp=600,
                                        stop_action='brake')
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        if self.direction == 'up':
            self.direction = 'left'
        elif self.direction == 'left':
            self.direction = 'down'
        elif self.direction == 'down':
            self.direction = 'right'
        elif self.direction == 'right':
            self.direction = 'up'
        time.sleep(.6)
        self.find = True

    def stop(self):
        """Stops both of the drive motors by making them brake.
        The robot is not shut down"""
        self.right_motor.stop(stop_action='brake')
        self.left_motor.stop(stop_action='brake')
        self.find = False

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

    def tracking(self):
        """this predicts the position of the robot and will be called within a
         running loop of the robot based on the direction to which value it
          will change(to be used for graphing)"""
        if self.find is True:
            if self.direction == 'up':
                self.y = self.y - 2
            elif self.direction == 'down':
                self.y = self.y + 2
            elif self.direction == 'right':
                self.x = self.x + 2
            elif self.direction == 'left':
                self.x = self.x - 2

    def shut_down(self):
        """this function will be used to exit the robot loop"""
        self.running = False
