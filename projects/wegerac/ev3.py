#!/usr/bin/env python3


import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time

class Ev3Delegate(object):
    def __init__(self):
        self.running = True
        self.mqtt_client = None



def main():
    print("********************************")
    print("RUNNING")
    print("********************************")
    my_delegate = Ev3Delegate()
    mqtt_client = com.MqttClient(my_delegate)
    my_delegate.mqtt_client = mqtt_client
    mqtt_client.connect_to_pc()

    btn = ev3.Button()
    btn.on_up = lambda state: send_string(mqtt_client, state)
    while my_delegate.running:
        btn.process()
        time.sleep(0.01)

def send_string(mqtt, state):
    if state:
        mqtt.send_message('string', ['hello'])
        print("got")


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
