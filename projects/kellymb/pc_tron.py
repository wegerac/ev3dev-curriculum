
import mqtt_remote_method_calls as com
import tkinter
from tkinter import ttk


def main():
    root = tkinter.Tk()
    root.title("Through the Woods")
    window = ttk.Notebook(root)

    control = ttk.Frame(padding=90, relief='raised')
    control.grid()
    window.add(control, text="Controller")

    frame_2 = ttk.Frame(padding=10)
    w = tkinter.Canvas(frame_2, width=400, height=400, background='grey')
    w.grid()
    window.add(frame_2, text="Map")
    window.pack()

    class PersonalReciever(object):
        def __init__(self):
            self.canvas = w

        def map_path(self, x_coordinate, y_coordinate):
            self.canvas.create_oval(x_coordinate-1, y_coordinate-1,
                                    x_coordinate+1, y_coordinate+1,
                                    fill="black")

        def home(self, x_coordinate, y_coordinate):
            self.canvas.create_rectangle(x_coordinate+10, y_coordinate+10,
                                         y_coordinate-10, y_coordinate-10,
                                         fill='blue')

    mqtt_client = com.MqttClient(PersonalReciever())
    mqtt_client.connect_to_ev3()

    start_button = ttk.Button(control, text="START!")
    start_button.grid(row=0, column=0)
    start_button['command'] = lambda: start(mqtt_client)
    root.bind('<o>', lambda event: start(mqtt_client))

    stop_button = ttk.Button(control, text='Stop')
    stop_button.grid(row=0, column=2)
    stop_button['command'] = lambda: stop(mqtt_client)
    root.bind('<p>', lambda event: stop(mqtt_client))

    up_button = ttk.Button(control, text="FORWARD")
    up_button.grid(row=3, column=1)
    up_button['command'] = lambda: forward(mqtt_client)
    root.bind('<Up>', lambda event: forward(mqtt_client))

    left_button = ttk.Button(control, text='LEFT')
    left_button.grid(row=4, column=0)
    left_button['command'] = lambda: left(mqtt_client)
    root.bind('<Left>', lambda event: left(mqtt_client))

    right_button = ttk.Button(control, text='RIGHT')
    right_button.grid(row=4, column=2)
    right_button['command'] = lambda: right(mqtt_client)
    root.bind('<Right>', lambda event: right(mqtt_client))

    down_button = ttk.Button(control, text="BACK")
    down_button.grid(row=5, column=1)
    down_button['command'] = lambda: backward(mqtt_client)
    root.bind('<Down>', lambda event: backward(mqtt_client))

    root.mainloop()


def start(mqtt_client):
    mqtt_client.send_message("start", [])
    print("start")
    mqtt_client.send_message("forward", [])


def forward(mqtt_client):
    mqtt_client.send_message("forward", [])
    print('forward')


def backward(mqtt_client):
    mqtt_client.send_message('turn_around', [])
    print('turn around')
    mqtt_client.send_message("forward", [])


def left(mqtt_client):
    mqtt_client.send_message("corner_left", [])
    print('Left')
    mqtt_client.send_message("forward", [])


def right(mqtt_client):
    mqtt_client.send_message('corner_right', [])
    print('Right')
    mqtt_client.send_message("forward", [])


def stop(mqtt_client):
    mqtt_client.send_message('stop', [])
    print('stop')


main()
