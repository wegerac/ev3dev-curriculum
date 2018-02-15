""" This is the robot controller based off two game modes from the game tron
 including light cycle and Battle tanks """

import mqtt_remote_method_calls as com
import Tron_controller as tron

def main():
    robot = tron.Tron()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()




