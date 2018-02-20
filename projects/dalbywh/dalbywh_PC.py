"""
The purpose of this project is to create an assisted driving car
It will be able to be controlled with a GUI             CHECK

The GUI will have tabs to switch out the different modes CHECK

The Speed will be controlled in two ways
    GUI - slider

The car will drive
    If it sees a line, it will correct back onto the road while continuing
    forward

    If it sees a wall it will beep
        If the wall gets too close, the robot will stop and say something

The arm can also be adjusted
    It will only move while the button is pressed rather than all the way up or
    down

    the speed can be adjusted in the same way the other motors can

    If arm motor goes past certain spot, IR no longer runs

    Will warn user that this is the case

While the robot runs
    The GUI will draw out the path that the robot moves.
        Probably going to be a simple_turtle


Questions for Class
    Whether doing the line corrections is viable
    Where/how to implement the my delegate class

TODO: MyDelegate with ability to draw
OR  : Make the line tracking work.
DO  : Whichever one makes more sense today




Authors: William Dalby
"""

import tkinter
from tkinter import ttk
from tkinter import *
import math
import mqtt_remote_method_calls as com


def main():
    # establishes frame for GUI

    root = tkinter.Tk()
    root.title('Robot Controller')

    # Establishes Tabs
    notebook = ttk.Notebook(root)

    controller_frame = ttk.Frame(notebook)
    controller_frame.grid()
    map_frame = ttk.Frame(notebook)
    map_frame.grid()

    notebook.add(controller_frame, text="Controller")
    notebook.add(map_frame, text='Map')

    notebook.grid()

    # Drive Motor Speed Slider Label
    speed_scale_label = ttk.Label(controller_frame, text='Drive Motor Speed')
    speed_scale_label.grid(row=0, column=5)

    # Initialize Drive Motor Speed Slider
    speed_scale = Scale(controller_frame, from_=0, to=900, orient=HORIZONTAL)
    speed_scale.grid(row=1, column=5)
    speed_scale.set(450)

    # Forward button
    forward_button = ttk.Button(controller_frame, text='Forward')
    forward_button.grid(row=1, column=1)
    forward_button['command'] = lambda: drive_forward(mqtt_client, TRUE,
                                                      speed_scale.get())

    # Left Button
    left_button = ttk.Button(controller_frame, text='Left')
    left_button.grid(row=2, column=0)
    left_button['command'] = lambda: turn_left(mqtt_client, TRUE,
                                               speed_scale.get())

    # Right Button
    right_button = ttk.Button(controller_frame, text='Right')
    right_button.grid(row=2, column=2)
    right_button['command'] = lambda: turn_right(mqtt_client, TRUE,
                                                 speed_scale.get())
    # Brake Button
    brake_button = ttk.Button(controller_frame, text='Brake')
    brake_button.grid(row=2, column=1)
    brake_button['command'] = lambda: brake(mqtt_client)

    # Backwards Button
    backward_button = ttk.Button(controller_frame, text='Backward')
    backward_button.grid(row=3, column=1)
    backward_button['command'] = lambda: drive_backward(mqtt_client, TRUE,
                                                        speed_scale.get())

    # Quit Button
    quit_button = ttk.Button(controller_frame, text='Quit')
    quit_button.grid(row=4, column=3)
    quit_button['command'] = lambda: shutdown(mqtt_client)

    # Initializes map for robot to draw on
    map_of_robot = Canvas(map_frame, width=500, height=500)
    map_of_robot.grid()

    # I know that this calculation works
    # start_x = 250
    # start_y = 250
    # radius = 8.6
    # angle = 0.951
    # first_x = start_x + radius * math.cos(angle)
    # first_y = start_y + radius * math.sin(angle)
    # second_x = start_x - radius * math.cos(angle)
    # second_y = start_y - radius * math.sin(angle)
    # map_of_robot.create_rectangle(first_x, first_y, second_x, second_y)

    # Makes MyDelegate to receive encoder values from the robot
    class MyDelegate:
        def __init__(self):
            self.right = 0
            self.left = 0

        def draw_map(self, start_x, start_y, angle):
            # map_of_robot.create_line takes 4 args. x, y, x, y
            radius = 30
            second_x = start_x + radius*math.sin(angle)
            second_y = start_y + radius*math.cos(angle)
            map_of_robot.create_line(start_x, start_y, second_x, second_y,
                                     arrow=tkinter.LAST, width=3)

    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()

    root.mainloop()

# Functions for drive commands


def drive_forward(mqtt_client, state, speed):
    mqtt_client.send_message('right_forward', [state, speed])
    mqtt_client.send_message('left_forward', [state, speed])


def drive_backward(mqtt_client, state, speed):
    mqtt_client.send_message('right_backward', [state, speed])
    mqtt_client.send_message('left_backward', [state, speed])


def turn_left(mqtt_client, state, speed):
    mqtt_client.send_message('right_forward', [state, speed])
    mqtt_client.send_message('left_backward', [state, speed])


def turn_right(mqtt_client, state, speed):
    mqtt_client.send_message('right_backward', [state, speed])
    mqtt_client.send_message('left_forward', [state, speed])


def brake(mqtt_client):
    mqtt_client.send_message('right_forward', [False, 0])
    mqtt_client.send_message('left_forward', [False, 0])


def shutdown(mqtt_client):
    mqtt_client.send_message('shutdown', [])


main()
