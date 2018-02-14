""" Author: Andrew Weger
    Final Project for CSSE 120

"""

import tkinter as tk
from tkinter import ttk
import mqtt_remote_method_calls as com
import random as ran

class PcDelegate(object):
    def __init__(self, label):
        print("")
        self.label = label
        self.count = 0
        self.total_money = 0
    def string(self, string):
        self.label['text'] = (string + str(self.count))
        self.count = self.count + 1

    def found_item(self, jewl_code):
        if jewl_code == 0:
            price = self.calc_price()
            print(price)

    def calc_price(self):
        dollar = ran.randint(0, 9999)
        cents = ran.randint(0, 99)
        price = str(dollar) + '.' + cents
        return price



def main():

    root = tk.Tk()
    root.title("Andrew Weger CSSE120 Final Project")

    frame1 = ttk.Frame(root, padding=20)
    frame1.grid()

    fbtn = tk.Button(frame1, text="Forward", width=10)
    fbtn.grid(row=0, column=1)
    fbtn['command'] = lambda: drive_forward(mqtt_client, 700, 700)
    root.bind('<Up>', lambda event: drive_forward(mqtt_client, 700, 700))

    bbtn = tk.Button(frame1, text="Backwards", width=10)
    bbtn.grid(row=2, column=1)
    bbtn['command'] = lambda: drive_backward(mqtt_client, 700, 700)
    root.bind('<Down>', lambda event: drive_backward(mqtt_client, 700, 700))

    lbtn = tk.Button(frame1, text="Left", width=10)
    lbtn.grid(row=1, column=0)
    lbtn['command'] = lambda: turn_left(mqtt_client, 400, 400)
    root.bind('<Left>', lambda event: turn_left(mqtt_client, 400, 400))

    rbtn = tk.Button(frame1, text="Right", width=10)
    rbtn.grid(row=1, column=2)
    rbtn['command'] = lambda: turn_right(mqtt_client, 400, 400)
    root.bind('<Right>', lambda event: turn_right(mqtt_client, 400, 400))

    sbtn = tk.Button(frame1, text="Stop", width=10)
    sbtn.grid(row=1, column=1)
    sbtn['command'] = lambda: stop(mqtt_client)
    root.bind('<space>', lambda event: stop(mqtt_client))

    button_label = ttk.Label(frame1, text="  Buttom messages from EV3  ")
    button_label.grid(row=2, column=0)

    pc_delegate = PcDelegate(button_label)
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()

    root.mainloop()

def drive_forward(mqtt_client, left_speed, right_speed):
    mqtt_client.send_message('right_forward', [True, right_speed])
    mqtt_client.send_message('left_forward', [True, left_speed])

def turn_left(mqtt_client, left_speed, right_speed):
    mqtt_client.send_message('right_forward', [True, right_speed])
    mqtt_client.send_message('left_backward', [True, left_speed])

def turn_right(mqtt_client, left_speed, right_speed):
    mqtt_client.send_message('right_backward', [True, right_speed])
    mqtt_client.send_message('left_forward', [True, left_speed])

def stop(mqtt_client):
    mqtt_client.send_message('left_forward', [False, 0])
    mqtt_client.send_message('right_forward', [False, 0])

def drive_backward(mqtt_client, left_speed, right_speed):
    mqtt_client.send_message('right_backward', [True, right_speed])
    mqtt_client.send_message('left_backward', [True, left_speed])




main()