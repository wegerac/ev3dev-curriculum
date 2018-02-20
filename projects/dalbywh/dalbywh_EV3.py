"""
This is the robot side of the program
Will send encoder values to the computer to have the computer draw out the
path of the robot as it moves

Authored by: William Dalby
"""
import ev3dev.ev3 as ev3
import dalbywh_library as robo
import mqtt_remote_method_calls as com
import time
import math


def main():
    # Makes a robot for a delegate and then starts a connection
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()

    # Initial variable values for calculations and sending
    robot.right_motor.position = 0
    robot.left_motor.position = 0
    right_start = 0
    left_start = 0
    x_start = 250
    y_start = 250
    angle_total = math.pi
    # While loop to keep the robot running
    while not robot.touch_sensor.is_pressed:
        # Strange if statement formatted by the text editor that sets a
        # range of area for the robot to stop or beep
        if not (not (11 < robot.ir_sensor.proximity) or not (
                    20 >= robot.ir_sensor.proximity)):
            # Robot will beep as a warning that the robot is getting close
            # to something
            ev3.Sound.beep()
            time.sleep(1)
        elif robot.ir_sensor.proximity <= 10:
            # Stops the robot if the robot is too close to something
            robot.stop()
            ev3.Sound.speak('Crash Avoided')
            time.sleep(5)

        # Calculation to send map items
        right = right_start
        right_new = robot.right_motor.position
        left = left_start
        left_new = robot.left_motor.position

        distance = (right_new - right) / 10
        distance_y = (left_new - left) / 10

        if (not distance <= 0 and 0 > distance_y) or (not distance >= 0 and 0 < distance_y):
            angle = ((right_new-right)/5.14)*(math.pi/180)
        else:
            angle = 0

        angle_total = angle_total + angle

        # Send command for the computer
        send_map(mqtt_client, x_start, y_start, angle_total)

        right_start = right_new
        left_start = left_new

        time.sleep(0.01)

        # r = 30
        # theta is found from time that robot turns and speed at which robot
        #  turns
        # theta start is 0.951 radians

        # ANGLES FOR MATH NEEDS TO BE IN RADIANS
        # Need scale factor for distance
    robot.shutdown()


# Function to send command to computer delegate
def send_map(mqtt_client, start_x, start_y, angle):
    mqtt_client.send_message('draw_map', [start_x, start_y, angle])


main()
