"""
This is the robot side of the program
Will send Sensor states and that's it, right?
And button states but that's part of sensors so technically...

Authored by: William Dalby
"""
import ev3dev as ev3
import robot_controller as robo
import mqtt_remote_method_calls as com

# doesn't need a delegate as it won't be sending anything


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_pc()
    while not robot.touch_sensor.is_pressed:
        robot.loop_forever()

main()
