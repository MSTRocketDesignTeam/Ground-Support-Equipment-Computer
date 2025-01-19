import gpiod
import time
import tkinter as tk
from tkinter import ttk
import sv_ttk

#Initialize the servo line on GPIO 2 of the Pi. 
chip = gpiod.Chip('gpiochip4')
servoPin = 2
servoLine = chip.get_line(servoPin)
servoLine.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
servoLine.set_value(1) #"Initialize" the pin at high, to account for the fact that some raspberry pi GPIO pins (like pin 2) are set to high upon bootup by the kernel. Adjust logic accordingly, if GPIO pin selections are changed.

pwd = input("Enter password: ")

def openValve():
	servoLine.set_value(0)
	
def closeValve():
	servoLine.set_value(1)


if (pwd == "12345"):
	root = tk.Tk()
	root.geometry('700x700')
	root.resizable(True, True)
	root.title('Cold Flow GUI')
	openValveButton = ttk.Button(root, text = 'Open Valve', command=lambda: openValve())
	closeValveButton = ttk.Button(root, text = 'Close Valve', command=lambda: closeValve())
	openValveButton.pack(ipadx=5, ipady=5, expand=True)
	closeValveButton.pack(ipadx=5, ipady=5, expand=True)
	
	sv_ttk.set_theme("dark")
	root.mainloop()

servoLine.release()
