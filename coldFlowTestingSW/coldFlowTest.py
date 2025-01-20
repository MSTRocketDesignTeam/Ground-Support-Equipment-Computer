import gpiod
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sv_ttk

#Initialize the servo line on GPIO 2 of the Pi. 
chip = gpiod.Chip('gpiochip4')
servoPin = 2
servoLine = chip.get_line(servoPin)
servoLine.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
servoLine.set_value(1) #"Initialize" the pin at high, to account for the fact that some raspberry pi GPIO pins (like pin 2) are set to high upon bootup by the kernel. Adjust logic accordingly, if GPIO pin selections are changed.

pwd = ""
while (pwd != "12345"):
	pwd = input("Enter password: ")

def openValve():
	servoLine.set_value(0)
	
def closeValve():
	servoLine.set_value(1)



root = tk.Tk()
root.geometry('700x700')
root.resizable(True, True)
root.title('Cold Flow GUI')

#RDT Logo initialization
rdtLogo = Image.open(r"../assetsAndImages/RDT_LOGO.png")
resizedImage = rdtLogo.resize((500, 150))
rdtImagePhoto = ImageTk.PhotoImage(resizedImage)
rdtLogoLabel = ttk.Label(root, image=rdtImagePhoto)

openValveButton = ttk.Button(root, text = 'Open Valve', command=lambda: openValve())
closeValveButton = ttk.Button(root, text = 'Close Valve', command=lambda: closeValve())


openValveButton.pack(ipadx=5, ipady=5, expand=True)
closeValveButton.pack(ipadx=5, ipady=5, expand=True)
rdtLogoLabel.pack(ipadx=5, ipady=5, expand=True)

sv_ttk.set_theme("dark")
root.mainloop()

servoLine.release() #Clean up
