
import mqtt_remote_method_calls as com
import tkinter
from tkinter import ttk


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Light Cycle")

    light_cycle = ttk.Frame(root, padding=30, relief='raised')
    light_cycle.grid()

    start_button = ttk.Button(light_cycle, text="START!")
    start_button.grid(row=0, column=0)

    stop_button = ttk.Button(light_cycle, text='Pause')
    stop_button.grid(row=0, column=2)

    up_button = ttk.Button(light_cycle, text='UP')
    up_button.grid(row=1, column=1)

    left_button = ttk.Button(light_cycle, text='LEFT')
    left_button.grid(row=2, column=0)

    right_button = ttk.Button(light_cycle, text='RIGHT')
    right_button.grid(row=2, column=2)

    down_button = ttk.Button(light_cycle, text='DOWN')
    down_button.grid(row=3, column=1)


main()