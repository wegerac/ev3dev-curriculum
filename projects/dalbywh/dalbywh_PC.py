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
import robot_controller as robo


def make_gui():
    # establishes frame for GUI

    root = tkinter.Tk()
    root.title = 'Robot Controller'
    controller_frame = ttk.Frame(root, padding=5)
    controller_frame.grid()

    # Forward button
    forward_button = ttk.Button(controller_frame, text='Forward')
    forward_button.grid(row=1, column=1)
    # forward_button['Command'] = lambda: go_forward()

    # Left Button
    left_button = ttk.Button(controller_frame, text='Left')
    left_button.grid(row=2, column=0)

    # Right Button
    right_button = ttk.Button(controller_frame, text='Right')
    right_button.grid(row = 2, column = 2)

    # Brake Button
    brake_button = ttk.Button(controller_frame, text='Brake')
    brake_button.grid(row = 2, column = 1)

    # Backwards Button
    backward_button = ttk.Button(controller_frame, text='Backward')
    backward_button.grid(row = 3, column = 1)

    # Initialize option menu
    master = Tk()
    variable = StringVar(master)
    variable.set('one')

    menu = OptionMenu

    root.mainloop()


def main():
    make_gui()


main()
