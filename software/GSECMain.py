import tkinter as tk
import tkinter.font as font
import tkinter.ttk as ttk
from datetime import datetime, timezone
import time


class GUI_Window():
    '''
    Sets up the launch GUI
    '''

    def __init__(self):
        root = tk.Tk()

        root.geometry('1200x700')
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
        self.setup_ox_monitor()
        self.setup_console()

        root.grid_columnconfigure(0, minsize=350)
        root.grid_columnconfigure(1, minsize=300)

        root.configure(bg="black")

        self.root.mainloop()

    def setup_modes_panel(self):
        '''Sets up a pannel with buttons for toggling auto launch interlock modes.'''

        modes_panel = tk.LabelFrame(self.root, text="Modes", bg="black",
                                    fg="white", padx=15, pady=15, relief='groove')
        self.control_mode_button = tk.Button(
            modes_panel, text="Control mode: manual", font=self._helv20, command=self.toggle_control_mode, pady=10)
        self.interlocks_button = tk.Button(
            modes_panel, text="Interlocks: off", font=self._helv20, command=self.toggle_interlocks, pady=10)

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

        modes_panel = tk.LabelFrame(self.root, text="Program Termination", bg="black",
                                    fg="white", padx=15, pady=15, relief='groove')
        modes_panel.grid(row=0, column=2)

        control_mode_button = tk.Button(
            modes_panel, text="E-Stop", font=self._helv36, fg="#bb0000", command=self.run_estop)
        interlocks_button = tk.Button(
            modes_panel, text="Exit Program (hard stop)", command=self.run_exit)

        control_mode_button.pack()
        interlocks_button.pack()
        self.set_control_mode = None
        self.set_interlocks = None

        self.go_emergency_stop = None
        self.go_safe_exit = None

    def setup_auto_control_section(self):
        '''
        Provides a button to run the automatic launch sequencer which
        will fire commands to light the igniter and open the main valves.
        '''
        pass

    def setup_manual_control_section(self):
        '''
        Provides buttons for oxidizer dump as well as manual 
        ignition and manual main valve actuation.
        '''
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

    def setup_ox_monitor(self):
        '''
        Displays the oxidizer button to actuate fill
        and estimated fill state.
        '''

        ox_panel = tk.LabelFrame(self.root, text="Nitrous Fill", bg="black",
                                 fg="white", padx=15, pady=15)
        ox_panel.grid(row=1, column=1)

        s = ttk.Style()
        s.configure('TProgressbar', thickness=20)

        fill_open_button = tk.Button(
            ox_panel, text='OPEN Fill Valve', font=self._helv20, pady=10, command=self.run_open_fill)
        fill_close_button = tk.Button(
            ox_panel, text='CLOSE Fill Valve', font=self._helv20, pady=10, command=self.run_close_fill)
        fill_time = tk.Label(
            ox_panel, text='Time to fill:\t\t-- Not Started --')
        progress_label = tk.Label(ox_panel, text='Fill progress:')
        progress = ttk.Progressbar(ox_panel, orient='horizontal',
                                   length=250, mode='determinate')

        fill_open_button.pack(pady=5)
        fill_close_button.pack(pady=5)
        fill_time.pack(pady=5, anchor='w')
        progress_label.pack(anchor='w')
        progress.pack()

        self.ox_progress_bar = progress

    def setup_console(self):
        '''
        Sets up the console for later messages to be logged and 
        the launch sequence to be recorded.
        '''

        console_panel = tk.LabelFrame(self.root, text="Console", bg="black",
                                      fg="white", padx=15, pady=15)
        console_panel.grid(row=1, column=2)

        console = tk.Text(console_panel, width=50, wrap='word')

        console.pack()
        console.configure(state='disabled')

        self.console = console

        self.run_console_log('STARTUP', 0)

        # Your code that checks the expression

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

            self.run_console_log(
                f'Control mode toggled to {
                    ['off', 'on'][self.auto_control_mode]}', 0
            )
            return 0
        except:
            self.run_console_log(
                'WARNING - An unknown issue occurred when attempting to toggle control modes.', 2)
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

            self.run_console_log(
                f'Interlocks toggled to {['off', 'on'][self.interlocks]}', 0
            )
            return 0
        except:
            self.run_console_log(
                'WARNING - An unknown issue occurred when attempting to toggle interlock modes.', 2)
            self.set_GUI_caution(2)
            return 1

    def run_estop(self):
        '''
        Runs the emergency stop procedure to safe the entire 
        system as quickly as possible.
        '''
        self.run_console_log('E-Stop Button Pressed', 2)
        self.console_file.close()

    def run_exit(self):
        '''
        Immediately terminates program operation without running safing procedures
        '''
        self.run_console_log('Program exited', 1)
        self.console_file.close()
        exit()

    def run_console_log(self, text, state):
        '''
        Logs a message to the console and to the corresponding 
        record file for future reference. 

        text - the message to be logged
        state - the message status to be logged:
            0 >>> Standard operation
            1 >>> Caution
            2 >>> Warning
            3 >>> No status
        '''

        date_time = datetime.now(timezone.utc)

        if text == "STARTUP":
            fmt = '%m-%d-%Y, %H:%M:%S UTC : CONSOLE STARTUP\n\n'
            text = 'Missouri S&T Rocket Design Team Ground Control\n\n' \
                '>> Standard Operation\nxx Caution\n!! Warning\n'
            state = 3
            self.console_file = open(date_time.strftime(
                'GSECLOG_%m_%d_%Y_%H_%M_%S'), 'a+')
        else:
            fmt = "%H:%M:%S : "

        state_indicators = ['>> ', 'xx ', '!! ', '']

        str_date_time = date_time.strftime(fmt)

        full_text = state_indicators[state] + str_date_time + text + '\n'
        self.console.configure(state='normal')
        self.console.insert(tk.END, full_text)
        self.console.configure(state='disabled')

        self.console_file.write(full_text)
        self.console.yview_pickplace("end")

    def run_open_fill(self):
        '''
        Attempts to open the fill valve and handles 
        the corresponding error code from micropython.
        '''
        error_code = 0
        self.run_console_log('Fill valve opened', error_code)

    def run_close_fill(self):
        '''
        Attempts to close the oxidizer valves and handles the 
        corresponding error code from micropython.
        '''
        error_code = 0
        self.run_console_log('Fill valve closed', error_code)

    def get_fill_state(self):
        '''Returns the fill state of the oxidizer tank as an ordered tuple.'''
        return (.3, 60)


if __name__ == "__main__":
    GUI = GUI_Window()
