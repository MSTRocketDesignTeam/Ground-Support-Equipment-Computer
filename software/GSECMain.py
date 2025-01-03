import tkinter as tk
import tkinter.font as font


class GUI_Window():
    '''
    Sets up the launch GUI
    '''

    def __init__(self):
        root = tk.Tk()

        root.geometry('1000x700')
        root.resizable(False, False)
        root.title('GSEC GUI')

        self.root = root

        self._helv20 = font.Font(family='Helvetica', size=20)
        self._helv36 = font.Font(family='Helvetica', size=36)
        self._cour12 = font.Font(family="Courier", size=12)

        # Setup basic GUI elements
        self.setup_modes_panel()
        self.setup_caution_panel()
        self.setup_kill_panel()
        self.setup_auto_control_section()
        self.setup_sensor_readouts()

        root.grid_columnconfigure(0, minsize=350)
        root.grid_columnconfigure(1, minsize=300)

        root.configure(bg="black")

        self.root.mainloop()

    def setup_modes_panel(self):
        '''Sets up a pannel with buttons for toggling auto launch interlock modes.'''

        modes_panel = tk.LabelFrame(self.root, text="Modes", bg="black",
                                    fg="white", padx=15, pady=15, relief='groove')
        self.control_mode_button = tk.Button(
            modes_panel, text="Control mode: manual", font=self._helv20, command=self.toggle_control_mode)
        self.interlocks_button = tk.Button(
            modes_panel, text="Interlocks: off", font=self._helv20, command=self.toggle_interlocks)

        self.control_mode_button.pack()
        self.interlocks_button.pack()
        modes_panel.grid(row=0, column=0)

        self.auto_control_mode = 0
        self.interlocks = 0

    def setup_caution_panel(self):
        '''
        Generates a panel with caution circles for cautions
        falling into the category of master, comms, sensors,
        or GUI. Other issues will be reported directly to the
        console.
        '''
        modes_panel = tk.LabelFrame(self.root, text="Warnings", bg="black",
                                    fg="white", padx=15, pady=15)
        modes_panel.grid(row=0, column=1)

        canvas = tk.Canvas(modes_panel, width=200, height=200)

        master_caution = canvas.create_oval(30, 15, 80, 65)
        canvas.create_text(55, 80, text="Master")
        canvas.itemconfig(master_caution, fill="yellow")

        sensor_caution = canvas.create_oval(30, 115, 80, 165)
        canvas.create_text(55, 180, text="Sensors")
        canvas.itemconfig(sensor_caution, fill="green")

        comms_caution = canvas.create_oval(130, 15, 180, 65)
        canvas.create_text(155, 80, text="Comms")
        canvas.itemconfig(comms_caution, fill="green")

        gui_error = canvas.create_oval(130, 115, 180, 165)
        canvas.create_text(155, 180, text="GUI")
        canvas.itemconfig(gui_error, fill="green")

        canvas.pack()

        color_states = ["green", "yellow", "red"]

        self.set_master_caution = lambda state: canvas.itemconfig(
            master_caution, fill=color_states[state])
        self.set_sensor_caution = lambda state: canvas.itemconfig(
            sensor_caution, fill=color_states[state])
        self.set_coms_caution = lambda state: canvas.itemconfig(
            comms_caution, fill=color_states[state])
        self.set_GUI_caution = lambda state: canvas.itemconfig(
            gui_error, fill=color_states[state])

    def setup_kill_panel(self):
        '''
        Provides a button to exit the program and a 
        button to immediately restore the program to a 
        safe operating condition and then exit (E-stop)
        '''

        modes_panel = tk.LabelFrame(self.root, text="Modes", bg="black",
                                    fg="white", padx=15, pady=15, relief='groove')
        modes_panel.grid(row=0, column=2)

        control_mode_button = tk.Button(
            modes_panel, text="E-Stop", font=self._helv36, fg="#bb0000")
        interlocks_button = tk.Button(
            modes_panel, text="Exit Program (hard stop)", command=exit)

        control_mode_button.pack()
        interlocks_button.pack()
        self.set_control_mode = None
        self.set_interlocks = None

        self.go_emergency_stop = None
        self.go_safe_exit = None

    def setup_auto_control_section(self):
        pass

    def setup_sensor_readouts(self):
        '''Displays all sensor readouts in table format.'''

        sensor_panel = tk.LabelFrame(self.root, text="Sensors", bg="black",
                                     fg="white", padx=15, pady=15)
        sensor_panel.grid(row=1, column=0)

        fuel_tank_PT = tk.Label(
            sensor_panel, text="Fuel tank PT         waiting...", font=self._cour12)
        ox_tank_PT = tk.Label(
            sensor_panel, text="Ox tank PT           waiting...", font=self._cour12)
        fuel_venturi_flow_PTs = tk.Label(
            sensor_panel, text="Fuel Venturi PTs     waiting : waiting ", font=self._cour12)
        ox_venturi_flow_PTs = tk.Label(
            sensor_panel, text="Ox Venturi PTs       waiting : waiting ", font=self._cour12)
        chamber_PT = tk.Label(
            sensor_panel, text="Chamber PT           waiting... ", font=self._cour12)
        ox_TC = tk.Label(
            sensor_panel, text="Ox TC                waiting... ", font=self._cour12)
        chamber_TC = tk.Label(
            sensor_panel, text="Chamber TC           waiting... ", font=self._cour12)

        sensor_list = [fuel_tank_PT, ox_tank_PT, fuel_venturi_flow_PTs,
                       ox_venturi_flow_PTs, chamber_PT, ox_TC, chamber_TC]

        for sensor in sensor_list:
            sensor.pack(anchor="w", pady=2)

        sensor_panel.grid(row=1, column=0)

    def toggle_control_mode(self):
        '''
        Toggle the control mode from manual to automatic and vice versa.
        '''
        try:
            if self.auto_control_mode:
                self.auto_control_mode = 0
            else:
                self.auto_control_mode = 1

            self.control_mode_button.config(
                text=f'Control mode: {['manual', 'auto'][self.auto_control_mode]}')
            return 0
        finally:
            print('An unknown issue occurred when attempting to toggle control modes.')
            self.set_GUI_caution(2)
            return 1

    def toggle_interlocks(self):
        '''
        Toggle the interlock mode from manual to automatic and vice versa.
        '''
        try:
            if self.interlocks:
                self.interlocks = 0
            else:
                self.interlocks = 1

            self.interlocks_button.config(
                text=f'Interlocks: {['off', 'on'][self.interlocks]}')
            return 0
        finally:
            print('An unknown issue occurred when attempting to toggle interlock modes.')
            self.set_GUI_caution(2)
            return 1

    def run_estop(self):
        '''
        Runs the emergency stop procedure to safe the entire 
        system as quickly as possible.
        '''
        pass


if __name__ == "__main__":
    GUI = GUI_Window()
