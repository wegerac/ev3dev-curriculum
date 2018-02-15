"""
This is the robot side of the program
Will send encoder values to the computer to have the computer draw out the
path of the robot as it moves

Authored by: William Dalby
"""
import ev3dev as ev3
import dalbywh_library as robo
import mqtt_remote_method_calls as com



def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    while not robot.touch_sensor.is_pressed:
        mqtt_client.send_message('draw_on_window', [robot.right_motor_encoder,
                                                    robot.left_motor_encoder])
        robot.loop_forever()


main()
