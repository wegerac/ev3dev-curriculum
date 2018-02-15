""" Author: Andrew Weger Feb 12-19, 2018
    Uses a robot to "find gems"
    Final Project for CSSE 120

"""

import tkinter as tk
from tkinter import ttk
import mqtt_remote_method_calls as com
import random as ran
import time

class PcDelegate(object):
    '''Creates the delegate for the PC'''
    def __init__(self, listbox, grailbtn, label):
        print("")
        self.listbox = listbox
        self.count = 0
        self.total_money = 0
        self.grail = grailbtn
        self.label = label
        self.history = []

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
            print('You found a sapphire worth, ' + price)

        elif jewl_code == 1:
            price = self.calc_price()
            text = str('You found a emerald worth, ' + '$' + str(price))
            self.total_money = self.total_money + float(price)
            self.listbox.insert(0, text)
            self.history.append(float(price))
            self.label['text'] = 'Total money: ' + '$' + str(self.total_money)
            print('You found a emerald worth, ' + str(price))

        elif jewl_code == 2:
            price = self.calc_price()
            text = str('You found a ruby worth, ' + '$' + str(price))
            self.total_money = self.total_money + float(price)
            self.listbox.insert(0, text)
            self.history.append(float(price))
            self.label['text'] = 'Total money: ' + '$' + str(self.total_money)
            print('You found a ruby worth, ' + price)

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


def main():
    '''Creates the tkinter GUI for the game'''
    root = tk.Tk()
    root.title("Andrew Weger CSSE120 Final Project")

    frame1 = ttk.Frame(root, padding=20)
    frame1.grid(row=0, column=1)

    fbtn = tk.Button(frame1, text="Forward", width=10)
    fbtn.grid(row=1, column=1)
    fbtn['command'] = lambda: drive_forward(mqtt_client, 700, 700)
    root.bind('<Up>', lambda event: drive_forward(mqtt_client, 700, 700))

    bbtn = tk.Button(frame1, text="Backwards", width=10)
    bbtn.grid(row=3, column=1)
    bbtn['command'] = lambda: drive_backward(mqtt_client, 700, 700)
    root.bind('<Down>', lambda event: drive_backward(mqtt_client, 700, 700))

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

    frame2 = ttk.Frame(root, padding=20)
    scrollbar = tk.Scrollbar(frame2)
    scrollbar.grid(row=0, column=1, sticky=tk.N + tk.S)

    listbox = tk.Listbox(frame2, bd=0, yscrollcommand=scrollbar.set, width=40, height=10)
    listbox.grid(row=0, column=0)

    scrollbar.config(command=listbox.yview)
    frame2.grid(row=0, column=0)

    grailbtn = tk.Button(frame2, text='Find the Grail', width=12)
    grailbtn['command'] = lambda: find_grail(mqtt_client)

    deletebtn = tk.Button(frame1, text='Delete', width=10)
    deletebtn['command'] = lambda: delete(pc_delegate, listbox, moneylabel)
    deletebtn.grid(row=4, column=0)

    quitbtn = tk.Button(frame1, text='Quit', width=10)
    quitbtn['command'] = lambda: quit(mqtt_client)
    quitbtn.grid(row=4, column=2)

    moneylabel = tk.Label(frame1, text='Total money: $0')
    moneylabel.grid(row=0, column=1)

    pc_delegate = PcDelegate(listbox, grailbtn, moneylabel)
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

    mqtt_client.send_message('right_backward', [True, right_speed])
    mqtt_client.send_message('left_forward', [True, left_speed])


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


def delete(delegate, listbox, label):
    '''Takes the given delegate, updates the total money and the
    history of the prices, and deletes the last listbox entry.'''
    price = delegate.history[len(delegate.history) - 1]
    total = delegate.total_money
    delegate.total_money = total - price
    listbox.delete(0)
    del delegate.history[len(delegate.history) - 1]
    label['text'] = 'Total money: ' + '$' + str(delegate.total_money)
    if listbox.size() == 0:
        label['text'] = "Total money: " + '$0.00'




main()