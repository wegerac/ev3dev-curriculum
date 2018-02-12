""" Author: Andrew Weger
    Final Project for CSSE 120

"""

import tkinter as tk
from tkinter import ttk
import mqtt_remote_method_calls as com

def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tk.Tk()
    root.title("Andrew Weger CSSE120 Final Project")

    frame1 = ttk.Frame(root, padding= 20)
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