
import ev3dev.ev3 as ev3


class Tron(object):

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
        assert self.pixy
        self.arm_motor.position = 0
        self.pixy = ev3.Sensor(driver_name="pixy-lego")

    def forward(self):
        self.right_motor.run_forever(speed_sp=600)
        self.left_motor.run_forever(speed_sp=600)

    def backward(self):
        self.right_motor.run_forever(speed_sp=-600)
        self.left_motor.run_forever(speed_sp=-600)

    def corner_right(self):
        self.left_motor.run_to_rel_pos(position_sp=-460, speed_sp=600,
                                       stop_action='brake')
        self.right_motor.run_to_rel_pos(position_sp=460, speed_sp=600,
                                        stop_action='brake')

    def corner_left(self):
        self.left_motor.run_to_rel_pos(position_sp=460, speed_sp=600,
                                       stop_action='brake')
        self.right_motor.run_to_rel_pos(position_sp=-460, speed_sp=600,
                                        stop_action='brake')

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
