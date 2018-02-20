""" This is the robot controller based off two game modes from the game tron
 including light cycle and Battle tanks """

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
        # robot.tracking()
        n = n + 1
        robot.pixy.mode = "SIG1"
        x = robot.pixy.value(1)
        y = robot.pixy.value(2)
        print("X:", x, "Y:", y)
        #print("X:", robot.x, "Y:", robot.y)
        robot.tracking()
        if robot.color_sensor.color == ev3.ColorSensor.COLOR_BLUE:
            mqtt_client.send_message('home', [robot.x, robot.y])
            ev3.Sound.speak('Found Home')
            robot.stop()
            break

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
        if n % 4 == 0:
            mqtt_client.send_message("map_path", [robot.x, robot.y])
        time.sleep(0.2)


main()
