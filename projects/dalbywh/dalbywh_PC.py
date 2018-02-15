"""
The purpose of this project is to create an assisted driving car
It will be able to be controlled with both a GUI and a controller

The GUI will have tabs to switch out the different modes

The GUI will also have an options tab to eliminate certain options

The Speed will be controlled in two ways
    GUI - slider
    Controller - Specific Channel will change motor speeds

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





Authors: William Dalby
"""

import tkinter
from tkinter import ttk
from tkinter import *
import time
import math
import dalbywh_library as robo
import ev3dev as ev3
from tkinter.scrolledtext import ScrolledText
import mqtt_remote_method_calls as com


def main():

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    # establishes frame for GUI

    root = tkinter.Tk()
    root.title('Robot Controller')

    # Establishes Tabs
    notebook = ttk.Notebook(root)

    controller_frame = ttk.Frame(notebook)
    controller_frame.grid()
    options_frame = ttk.Frame(notebook)
    options_frame.grid()

    notebook.add(controller_frame, text="Controller")
    notebook.add(options_frame, text='Options')

    notebook.grid()

    # Drive Motor Speed Slider Label
    speed_scale_label = ttk.Label(options_frame, text='Drive Motor Speed')
    speed_scale_label.grid()

    # Initialize Drive Motor Speed Slider
    speed_scale = Scale(options_frame, from_=0, to=900, orient=HORIZONTAL)
    speed_scale.grid()

    # Initialize IR Sensor Checkbox
    check_button_variable = IntVar()
    check_box = Checkbutton(options_frame, text='IR Sensor',
                            variable=check_button_variable)
    check_box.grid(row = 2, column = 1)

    # Arm motor speed slider label
    arm_speed_label = ttk.Label(options_frame, text='Arm Motor Speed')
    arm_speed_label.grid(row= 0, column = 2)

    # Initialize Arm motor speed slider
    arm_speed_scale = Scale(options_frame, from_=0, to=400, orient=HORIZONTAL)
    arm_speed_scale.grid(row=1, column = 2)

    # Drive Speed Variable
    drive_speed = speed_scale.get()

    # Arm Speed Variable
    arm_speed = arm_speed_scale.get()

    # Forward button
    forward_button = ttk.Button(controller_frame, text='Forward')
    forward_button.grid(row=1, column=1)
    forward_button['command'] = lambda: drive_forward(mqtt_client, TRUE,
                                                      drive_speed)

    # Left Button
    left_button = ttk.Button(controller_frame, text='Left')
    left_button.grid(row=2, column=0)
    left_button['command'] = lambda: turn_left(mqtt_client, TRUE, drive_speed)

    # Right Button
    right_button = ttk.Button(controller_frame, text='Right')
    right_button.grid(row=2, column=2)
    right_button['command'] = lambda: turn_right(mqtt_client, TRUE,
                                                 drive_speed)

    # Brake Button
    brake_button = ttk.Button(controller_frame, text='Brake')
    brake_button.grid(row=2, column=1)
    brake_button['command'] = lambda: brake(mqtt_client)

    # Backwards Button
    backward_button = ttk.Button(controller_frame, text='Backward')
    backward_button.grid(row=3, column=1)
    backward_button['command'] = lambda: drive_backward(mqtt_client, TRUE,
                                                        drive_speed)

    # Quit Button
    quit_button = ttk.Button(controller_frame, text='Quit')
    quit_button.grid(row=4, column=3)
    quit_button['command'] = lambda: shutdown(mqtt_client)

    # Quit Button for Options menu
    second_quit_button = ttk.Button(options_frame, text='Quit')
    second_quit_button.grid(row=3, column=2)
    second_quit_button['command']= lambda:shutdown(mqtt_client)

    # # Initialize option menu
    # variable = StringVar(root)
    # variable.set('ON')
    #
    # menu = OptionMenu(options_frame, variable, "ON", "OFF")
    # menu.grid()

    # Initialize arm calibration button
    arm_calibrate = ttk.Button(options_frame, text='Re-Calibrate arm')
    arm_calibrate.grid(row=3, column=0)
    arm_calibrate['command'] = lambda: calibrate_arm(mqtt_client)

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


def calibrate_arm(mqtt_client):
    mqtt_client.send_message('arm_calibration', [])


def brake(mqtt_client):
    mqtt_client.send_message('right_forward', [False, 0])
    mqtt_client.send_message('left_forward', [False, 0])


def shutdown(mqtt_client):
    mqtt_client.send_message('shutdown', [])


main()
