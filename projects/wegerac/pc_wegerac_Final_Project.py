""" Author: Andrew Weger Feb 12-19, 2018
    Uses a robot to "find gems"
    Final Project for CSSE 120

"""

import tkinter as tk
from tkinter import ttk
import mqtt_remote_method_calls as com
import random as ran
import time
import sys

class PcDelegate(object):
    '''Creates the delegate for the PC'''
    def __init__(self, root, listbox, grailbtn, label, label2, frame1, frame2, notebook, tab1, tab2):
        self.root = root
        self.listbox = listbox
        self.count = 0
        self.total_money = 0
        self.grail = grailbtn
        self.label = label
        self.history = []
        self.label2 = label2
        self.frame1 = frame1
        self.frame2 = frame2
        self.notebook = notebook
        self.tab1 = tab1
        self.tab2 = tab2

    def found_item(self, jewl_code):
        '''Gets the number from the mqtt message sent from the robot and the different
        values will correspond to different "gems". When one is found the function will
        calculate a price from the calc_price function. It will add that price to a seq of
        prices to let the delete button to delete the last price and update the counter.'''
        if jewl_code == 0:
            price = self.calc_price()
            self.total_money = self.total_money + float(price)
            text = str('You found a sapphire worth, ' + '$' + price)
            self.listbox.insert(0, text)
            self.history.append(float(price))
            self.label['text'] = 'Total money: ' + '$' + str(self.total_money)
            self.label2['text'] = 'Total money: ' + '$' + str(self.total_money)
            print('You found a sapphire worth, ' + price)
            if self.total_money >= 1000:
                self.win()

        elif jewl_code == 1:
            price = self.calc_price()
            text = str('You found a emerald worth, ' + '$' + str(price))
            self.total_money = self.total_money + float(price)
            self.listbox.insert(0, text)
            self.history.append(float(price))
            self.label['text'] = 'Total money: ' + '$' + str(self.total_money)
            self.label2['text'] = 'Total money: ' + '$' + str(self.total_money)
            print('You found a emerald worth, ' + str(price))
            if self.total_money >= 1000:
                self.win()

        elif jewl_code == 2:
            price = self.calc_price()
            text = str('You found a ruby worth, ' + '$' + str(price))
            self.total_money = self.total_money + float(price)
            self.listbox.insert(0, text)
            self.history.append(float(price))
            self.label['text'] = 'Total money: ' + '$' + str(self.total_money)
            self.label2['text'] = 'Total money: ' + '$' + str(self.total_money)
            print('You found a ruby worth, ' + price)
            if self.total_money >= 1000:
                self.win()

    def grail_in_sight(self):
        '''Shows the Find Grail button when
        the mqtt message calls this function '''
        self.grail.grid()

    def calc_price(self):
        '''Calculates the price of the "Gem" found.'''
        dollar = ran.randint(0, 9999)
        cents = ran.randint(0, 99)
        price = str(dollar) + '.' + str(cents)
        return price

    def win(self):
        self.frame1.destroy()
        self.frame2.destroy()
        self.notebook.tab(0, text='CONGRATULATIONS')
        self.notebook.tab(1, text='YOU WIN!')
        win = tk.Label(self.tab1, text='Congrats, you win!')
        win2 = tk.Label(self.tab1, text=('If you snagged the grail, please lower the arm in the now '
                                         '"YOU WIN" tab before closing the window)'))
        win3 = tk.Label(self.tab1, text='The program will close automatically in 60 seconds.')
        win.grid()
        win2.grid()
        win3.grid()
        time.sleep(60)
        self.root.destroy()


def main():
    '''Creates the tkinter GUI for the game'''
    root = tk.Tk()
    root.title("Andrew Weger CSSE120 Final Project")

    notebook = ttk.Notebook(root)

    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)

    frame1 = ttk.Frame(tab1, padding=20)
    frame1.grid(row=0, column=1)

    fbtn = tk.Button(frame1, text="Forward", width=10)
    fbtn.grid(row=1, column=1)
    fbtn['command'] = lambda: drive_forward(mqtt_client, 500, 500)
    root.bind('<Up>', lambda event: drive_forward(mqtt_client, 500, 500))

    bbtn = tk.Button(frame1, text="Backwards", width=10)
    bbtn.grid(row=3, column=1)
    bbtn['command'] = lambda: drive_backward(mqtt_client, 500, 500)
    root.bind('<Down>', lambda event: drive_backward(mqtt_client, 500, 500))

    lbtn = tk.Button(frame1, text="Left", width=10)
    lbtn.grid(row=2, column=0)
    lbtn['command'] = lambda: turn_left(mqtt_client, 400, 400)
    root.bind('<Left>', lambda event: turn_left(mqtt_client, 400, 400))

    rbtn = tk.Button(frame1, text="Right", width=10)
    rbtn.grid(row=2, column=2)
    rbtn['command'] = lambda: turn_right(mqtt_client, 400, 400)
    root.bind('<Right>', lambda event: turn_right(mqtt_client, 400, 400))

    sbtn = tk.Button(frame1, text="Stop", width=10)
    sbtn.grid(row=2, column=1)
    sbtn['command'] = lambda: stop(mqtt_client)
    root.bind('<space>', lambda event: stop(mqtt_client))

    frame2 = ttk.Frame(tab1, padding=20)
    scrollbar = tk.Scrollbar(frame2)
    scrollbar.grid(row=0, column=1, sticky=tk.N + tk.S)

    listbox = tk.Listbox(frame2, bd=0, yscrollcommand=scrollbar.set, width=40, height=10)
    listbox.grid(row=0, column=0)

    scrollbar.config(command=listbox.yview)
    frame2.grid(row=0, column=0)

    grailbtn = tk.Button(frame2, text='Find the Grail', width=12)
    grailbtn['command'] = lambda: find_grail(mqtt_client)

    deletebtn = tk.Button(frame1, text='Delete', width=10)
    deletebtn['command'] = lambda: delete(pc_delegate, listbox, moneylabel1, moneylabel2)
    deletebtn.grid(row=4, column=0)

    quitbtn = tk.Button(frame1, text='Quit', width=10)
    quitbtn['command'] = lambda: quit(mqtt_client)
    quitbtn.grid(row=4, column=2)

    moneylabel1 = tk.Label(frame1, text='Total money: $0.00')
    moneylabel1.grid(row=0, column=1)

    armbtn = tk.Button(tab2, text='Arm Calibration', width=12)
    armbtn['command'] = lambda: calibrate(mqtt_client)
    armbtn.grid(row=1, column=0)

    resetmoneybtn = tk.Button(tab2, text='Reset Money',width=12)
    resetmoneybtn['command'] = lambda: reset_money(pc_delegate)
    resetmoneybtn.grid(row=1, column=2)

    moneylabel2 = tk.Label(tab2, text='Total money: $0.00')
    moneylabel2.grid(row=0, column=1)

    notebook.add(tab1, text='Controller and Listbox')
    notebook.add(tab2, text='Options')

    notebook.grid()

    armup = tk.Button(tab2, text='Arm Up', width=12)
    armup['command'] = lambda: arm_up(mqtt_client)
    armup.grid(row=2, column=0)

    armdown = tk.Button(tab2, text='Arm Down', width=12)
    armdown['command'] = lambda:arm_down(mqtt_client)
    armdown.grid(row=2, column=2)

    pc_delegate = PcDelegate(root, listbox, grailbtn, moneylabel1, moneylabel2, frame1, frame2, notebook, tab1, tab2)
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()

    root.mainloop()


def drive_forward(mqtt_client, left_speed, right_speed):
    '''Takes the given mqtt_client, and speeds to call the driving
    functions that are in the robots delegate class.'''
    mqtt_client.send_message('right_forward', [True, right_speed])
    mqtt_client.send_message('left_forward', [True, left_speed])


def turn_left(mqtt_client, left_speed, right_speed):
    '''Takes the given mqtt_client, and speeds to call the driving
    functions that are in the robots delegate class.'''

    mqtt_client.send_message('right_forward', [True, right_speed])
    mqtt_client.send_message('left_backward', [True, left_speed])


def turn_right(mqtt_client, left_speed, right_speed):
    '''Takes the given mqtt_client, and speeds to call the driving
    functions that are in the robots delegate class.'''

    mqtt_client.send_message('left_forward', [True, left_speed])
    mqtt_client.send_message('right_backward', [True, right_speed])


def stop(mqtt_client):
    '''Takes the given mqtt_client, and speeds to call the driving
    functions that are in the robots delegate class.'''
    mqtt_client.send_message('left_forward', [False, 0])
    mqtt_client.send_message('right_forward', [False, 0])


def drive_backward(mqtt_client, left_speed, right_speed):
    '''Takes the given mqtt_client, and speeds to call the driving
    functions that are in the robots delegate class.'''
    mqtt_client.send_message('right_backward', [True, right_speed])
    mqtt_client.send_message('left_backward', [True, left_speed])


def quit(mqtt_client):
    '''Takes the given mqtt_client and sends a message to call the
    shutdown function in the robots delegate class.'''
    mqtt_client.send_message('shutdown')
    exit()


def find_grail(mqtt_client):
    '''Takes the given mqtt_client and sends a message to call the
    shutdown function in the robots delegate class.'''
    mqtt_client.send_message('find_grail')


def delete(delegate, listbox, label, label2):
    '''Takes the given delegate, updates the total money and the
    history of the prices, and deletes the last listbox entry.'''
    price = delegate.history[len(delegate.history) - 1]
    total = delegate.total_money
    delegate.total_money = total - price
    listbox.delete(0)
    del delegate.history[len(delegate.history) - 1]
    label['text'] = 'Total money: ' + '$' + str(delegate.total_money)
    label2['text'] = 'Total money: ' + '$' + str(delegate.total_money)
    if listbox.size() == 0:
        label['text'] = "Total money: " + '$0.00'
        label2['text'] = "Total money: " + '$0.00'

def calibrate(mqtt_client):
    mqtt_client.send_message('calibrate')

def arm_up(mqtt_client):
    mqtt_client.send_message('arm_up')

def arm_down(mqtt_client):
    mqtt_client.send_message('arm_down')

def reset_money(delegate):
    delegate.total_money = 0
    delegate.history = []
    delegate.label['text'] = 'Total money: $0.00'
    delegate.label2['text'] = 'Total money: $0.00'
    delegate.listbox.delete(0, tk.END)



main()