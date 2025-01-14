import gpiod
import time
import tkinter as tk
from tkinter import ttk
chip = gpiod.Chip('gpiochip4')
servoPin = 2
servoLine = chip.get_line(servoPin)
servoLine.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)

pwd = input("Enter password: ")

def openValve():
	servoLine.set_value(1)
	
def closeValve():
	servoLine.set_value(0)


if (pwd == "12345"):
	root = tk.Tk()
	root.geometry('700x700')
	root.resizable(True, True)
	root.title('Cold Flow GUI')
	openValveButton = ttk.Button(root, text = 'Open Valve', command=lambda: openValve())
	closeValveButton = ttk.Button(root, text = 'Close Valve', command=lambda: closeValve())
	openValveButton.pack(ipadx=5, ipady=5, expand=True)
	closeValveButton.pack(ipadx=5, ipady=5, expand=True)
	root.mainloop()

servoLine.release()
