""" This control is based off of little red riding hood the robot will be
traveling to grandma's house represented by a blue sheet of paper this
function recieves the commands sent from pc as well as adds secondary
control method using an object which is not the same color as the house or
the front of the ev3 by moving this object around you can direct the robots
travel """

import time
import mqtt_remote_method_calls as com
import Traveler as Trav
import ev3dev.ev3 as ev3


def main():
    robot = Trav.Traveler()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()

    print('Running Traveler:')
    ev3.Sound.speak("Running Traveler").wait()
    n = 0

    while robot.running is True:
        n = n + 1
        robot.pixy.mode = "SIG1"
        x = robot.pixy.value(1)
        y = robot.pixy.value(2)
        print("X:", x, "Y:", y)
        # prints pixy values for tracking adjusting and calibrating
        print("X:", robot.x, "Y:", robot.y)
        # prints the location of the robot being sent to the pc
        robot.tracking()
        if robot.color_sensor.color == ev3.ColorSensor.COLOR_BLUE:
            # ends the program if you find "Grandma's House
            mqtt_client.send_message('home', [robot.x, robot.y])
            ev3.Sound.speak('Found Home')
            robot.stop()
            break
        """if statements below control the direction of the robot using the 
        pixy cam"""
        if x < 150:
            if x != 0:
                robot.corner_right()
                robot.forward()
        elif x > 170:
            robot.corner_left()
            robot.forward()
        if robot.touch_sensor.is_pressed:
            ev3.Sound.speak('Good bye')
            break
        if n % 2 == 0:
            # this statement sends a message to the pc to add a dot to the
            # canvas every .4 seconds
            mqtt_client.send_message("map_path", [robot.x, robot.y])
        time.sleep(0.2)
        # keeps the program from overworking


main()
