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
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.right_motor.position = 0
    robot.left_motor.position = 0
    right_start = 0
    left_start = 0

    x_start = 250
    y_start = 250
    angle_total = math.pi
    while not robot.touch_sensor.is_pressed:
        # TURN THIS INTO AN IF STATEMENT
        # if robot.ir_sensor.proximity > 6 and robot.ir_sensor.proximity \
        #         <= 10:
        #     ev3.Sound.beep()
        #     time.sleep(1)
        #     send_map(mqtt_client, robot.right_motor.position,
        #              robot.left_motor.position)
        # elif robot.ir_sensor.proximity <= 5:
        #     robot.stop()
        #     ev3.Sound.speak('Crash Avoided')
        #     time.sleep(5)
        # send_map(mqtt_client, x_start, y_start, distance, angle)
        # time.sleep(0.01)

        # Rectangle which starts with thinner end at top.
        # so width = 10        w/2 = 5
        # length equals 14     l/2 = 7
        # r = 30
        # theta is found from time that robot turns and speed at which robot
        #  turns
        # theta start is 0.951 radians

        # top right corner    (255, 257)
        # top left corner     (245, 257)
        # bottom right corner (255, 243)
        # bottom left corner  (245, 243)

        right = right_start
        right_new = robot.right_motor.position
        left = left_start
        left_new = robot.left_motor.position

        distance = (right_new-right)/10
        distance_y = (left_new - left)/10

        # ANGLES FOR MATH NEEDS TO BE IN RADIANS
        # Need scale factor for distance

        if (distance > 0 and distance_y < 0) or (distance < 0 and distance_y
            > 0):
            angle = ((right_new-right)/5.14)*(math.pi/180)
        else:
            angle = 0

        angle_total = angle_total + angle
        send_map(mqtt_client, x_start, y_start, distance, angle_total)

        right_start = right_new
        left_start = left_new

        time.sleep(0.01)



    robot.stop()


def send_map(mqtt_client, start_x, start_y, radius, angle):
    mqtt_client.send_message('draw_map', [start_x, start_y, radius, angle])


# idea for line detection
# SO: the idea is that if the color sensor sees a line, the pixy cam kicks in
# if the pixy cam sees the line move from right to left, the robot is
# drifting to the right. If it does the opposite, the robot is drifting to
# the left. So, the robot will correct accordingly. May be a delay in
# between the line detection and correction. Which is dangerous. But it
# could be very small.

main()
