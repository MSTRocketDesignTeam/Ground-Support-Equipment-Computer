import tkinter as tk
import tkinter.font as font
import tkinter.ttk as ttk
from datetime import datetime, timezone
import sys


class Custom_Button():
    def __init__(self, parent, text_, action):
        self.normal_color = 'white'
        self.text_color = 'black'
        self.hover_color = '#b0b0b0'
        self.active_color = '#94ff21'
        self._helv20 = font.Font(family='Helvetica', size=20)

        button = tk.Label(parent, text=text_, fg=self.text_color,
                          bg=self.normal_color, font=self._helv20, padx=15, pady=15, relief='raised')
        button.bind(
            '<Enter>', self.enter_action)
        button.bind(
            '<Leave>', self.leave_action)
        button.bind(
            '<Double-Button>', self.double_action)

        button.pack(pady=5)

        self.button = button
        self.enter_flag = False
        self.action = action

    def enter_action(self, event):
        self.enter_flag = True
        self.button.config(bg=self.hover_color)

    def leave_action(self, event):
        self.enter_flag = False
        self.button.config(bg=self.normal_color)

    def double_action(self, event):
        if self.enter_flag:
            self.action()
            self.button.config(bg=self.active_color)

        self.enter_flag = False

    def set_text(self, text_):
        self.button.config(text=text_)


class Custom_Panel():
    def __init__(self, root, row_, column_, text_):
        self.panel = tk.LabelFrame(root, text=text_, bg='black',
                                   fg='white', padx=15, pady=15, relief='groove')
        self.panel.grid(row=row_, column=column_,
                        sticky='nsew', padx=5, pady=5)


class GUI_Window():
    '''
    Sets up the launch GUI
    '''

    def __init__(self):
        root = tk.Tk()

        root.geometry('1200x700')
        # root.resizable(False, False)
        root.title('GSEC GUI')

        self.root = root

        self._helv16 = font.Font(family='Helvetica', size=16)
        self._helv20 = font.Font(family='Helvetica', size=20)
        self._helv36 = font.Font(family='Helvetica', size=36)
        self._cour12 = font.Font(family='Courier', size=12)
        self._cour16 = font.Font(family='Courier', size=16)

        # Setup basic GUI elements
        self.setup_console(0)
        self.setup_caution_panel(0, 1)
        self.setup_sensor_readouts(0, 2)
        self.setup_modes_panel(1, 1)
        self.setup_kill_panel(1, 2)
        self.setup_ox_monitor(2, 0)
        self.setup_auto_control_section(2, 1)
        self.setup_manual_control_section(2, 2)

        root.configure(bg='black')

        self.exit_attempt = False

        self.root.mainloop()

    def setup_modes_panel(self, row_, column_):
        '''Sets up a pannel with buttons for toggling auto launch interlock modes.'''

        mp = Custom_Panel(self.root, row_, column_, 'Modes')

        self.control_mode_button = Custom_Button(
            mp.panel, 'Control mode: manual', self.toggle_control_mode)
        self.interlocks_button = Custom_Button(
            mp.panel, 'Interlocks: off', self.toggle_interlocks)

        self.auto_control_mode = 0
        self.interlocks = 0

    def setup_caution_panel(self, row_, column_):
        '''
        Generates a panel with caution circles for cautions
        falling into the category of master, comms, sensors,
        or GUI. Other issues will be reported directly to the
        console.
        '''
        cp = Custom_Panel(self.root, row_, column_, 'Status Lights')

        canvas = tk.Canvas(cp.panel, width=200, height=200)

        master_caution = canvas.create_oval(30, 15, 80, 65)
        canvas.create_text(55, 80, text='Master')
        canvas.itemconfig(master_caution, fill='green')

        sensors_caution = canvas.create_oval(30, 115, 80, 165)
        canvas.create_text(55, 180, text='Sensors')
        canvas.itemconfig(sensors_caution, fill='green')

        comms_caution = canvas.create_oval(130, 15, 180, 65)
        canvas.create_text(155, 80, text='Comms')
        canvas.itemconfig(comms_caution, fill='green')

        gui_caution = canvas.create_oval(130, 115, 180, 165)
        canvas.create_text(155, 180, text='GUI')
        canvas.itemconfig(gui_caution, fill='green')

        canvas.pack()

        self.caution_panel = {
            'master': master_caution,
            'sensors': sensors_caution,
            'coms': comms_caution,
            'GUI': gui_caution,
            'canvas': canvas
        }

        self.caution_states = {
            'master': 0,
            'sensors': 0,
            'coms': 0,
            'GUI': 0
        }

    def set_caution(self, caution_type, state):

        color_states = ['green', 'yellow', 'red']
        self.caution_states[caution_type] = state

        self.caution_panel['canvas'].itemconfig(
            self.caution_panel[caution_type], fill=color_states[state])

        if state > self.caution_states['master']:
            self.caution_states['master'] = state

            self.caution_panel['canvas'].itemconfig(
                self.caution_panel['master'], fill=color_states[state])

    def setup_kill_panel(self, row_, column_):
        '''
        Provides a button to exit the program and a
        button to immediately restore the program to a
        safe operating condition and then exit (E-stop)
        '''

        mp = Custom_Panel(self.root, row_, column_, 'Program Termination')

        Custom_Button(mp.panel, 'Emergency Stop', self.run_estop)
        Custom_Button(mp.panel, 'Exit Program', self.run_exit)

        self.set_control_mode = None
        self.set_interlocks = None

        self.go_emergency_stop = None
        self.go_safe_exit = None

    def setup_auto_control_section(self, row_, column_):
        '''
        Provides a button to run the automatic launch sequencer which
        will fire commands to light the igniter and open the main valves.
        '''
        ap = Custom_Panel(self.root, row_, column_, 'Automated Controls')

        Custom_Button(ap.panel, 'Start launch sequence', self.run_launch)

    def setup_manual_control_section(self, row_, column_):
        '''
        Provides buttons for oxidizer dump as well as manual
        ignition and manual main valve actuation.
        '''
        mp = Custom_Panel(self.root, row_, column_, 'Manual Controls')

        Custom_Button(mp.panel, 'Igniter', self.run_launch)
        Custom_Button(mp.panel, 'Dump Oxidizer', self.run_launch)
        Custom_Button(mp.panel, 'Open Mains', self.run_launch)

    def setup_sensor_readouts(self, row_, column_):
        '''Displays all sensor readouts in table format.'''

        sp = Custom_Panel(self.root, row_, column_, 'Sensors')

        fuel_tank_PT = tk.Label(
            sp.panel, text='Fuel tank PT         waiting...', font=self._cour12)
        ox_tank_PT = tk.Label(
            sp.panel, text='Ox tank PT           waiting...', font=self._cour12)
        fuel_venturi_flow_PTs = tk.Label(
            sp.panel, text='Fuel Venturi PTs     waiting : waiting ', font=self._cour12)
        ox_venturi_flow_PTs = tk.Label(
            sp.panel, text='Ox Venturi PTs       waiting : waiting ', font=self._cour12)
        chamber_PT = tk.Label(
            sp.panel, text='Chamber PT           waiting... ', font=self._cour12)
        ox_TC = tk.Label(
            sp.panel, text='Ox TC                waiting... ', font=self._cour12)
        chamber_TC = tk.Label(
            sp.panel, text='Chamber TC           waiting... ', font=self._cour12)

        sensor_list = [fuel_tank_PT, ox_tank_PT, fuel_venturi_flow_PTs,
                       ox_venturi_flow_PTs, chamber_PT, ox_TC, chamber_TC]

        for sensor in sensor_list:
            sensor.pack(anchor='w', pady=2)

    def setup_ox_monitor(self, row_, column_):
        '''
        Displays the oxidizer button to actuate fill
        and estimated fill state.
        '''

        op = Custom_Panel(self.root, row_, column_, 'Nitrous Fill')

        s = ttk.Style()
        s.configure('TProgressbar', thickness=20)

        fill_open_button = Custom_Button(
            op.panel, 'Open Fill Valve', self.run_open_fill)
        fill_close_button = Custom_Button(
            op.panel, 'Close Fill Valve', self.run_close_fill)
        fill_time = tk.Label(
            op.panel, text='Time to fill:\t\t-- Not Started --')
        progress_label = tk.Label(op.panel, text='Fill progress:')
        progress = ttk.Progressbar(op.panel, orient='horizontal',
                                   length=250, mode='determinate')

        fill_time.pack(pady=5, anchor='w')
        progress_label.pack(anchor='w')
        progress.pack()

        self.ox_progress_bar = progress

    def setup_console(self, column_):
        '''
        Sets up the console for later messages to be logged and
        the launch sequence to be recorded.
        '''

        cp = Custom_Panel(self.root, 0, column_, 'Console')
        cp.panel.grid(row=0, column=column_, rowspan=2)

        console = tk.Text(cp.panel, width=40, height=20,
                          wrap='word', font=self._cour16)

        console.pack()
        console.configure(state='disabled')

        self.console = console

        self.run_console_log('STARTUP', 0)

    def toggle_control_mode(self):
        '''
        Toggle the control mode from manual to automatic and vice versa.
        '''
        try:
            if self.auto_control_mode:
                self.auto_control_mode = 0
            else:
                self.auto_control_mode = 1

            self.control_mode_button.set_text(
                f'Control mode: {['manual', 'auto'][self.auto_control_mode]}')

            self.run_console_log(
                f'Control mode toggled to {
                    ['off', 'on'][self.auto_control_mode]}', 0
            )
            return 0
        except:
            self.run_console_log(
                'WARNING - An unknown issue occurred when attempting to toggle control modes.', 2)
            self.set_caution('GUI', 2)
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

            self.interlocks_button.set_text(
                f'Interlocks: {['off', 'on'][self.interlocks]}')

            self.run_console_log(
                f'Interlocks toggled to {['off', 'on'][self.interlocks]}', 0
            )
            return 0
        except:
            self.run_console_log(
                'WARNING - An unknown issue occurred when attempting to toggle interlock modes.', 2)
            self.set_caution('GUI', 2)
            return 1

    def run_estop(self):
        '''
        Runs the emergency stop procedure to safe the entire
        system as quickly as possible.
        '''
        self.run_console_log('E-Stop Button Pressed', 2)
        # self.console_file.close()

    def run_exit(self):
        '''
        Immediately terminates program operation without running safing procedures
        '''

        try:
            self.run_console_log('Program exited', 1)
            self.console_file.close()
            self.exit_attempt = True
        except:
            print('error')
            self.run_console_log(
                'An error occured while trying to exit the program. This probably occured because of an error in saving the log file. To proceed anyway, please click this button again.', 2)

        if self.exit_attempt:
            sys.exit(0 if self.exit_attempt == False else 1)
        else:
            self.exit_attempt = True

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

        if text == 'STARTUP':
            fmt = '%m-%d-%Y, %H:%M:%S UTC : CONSOLE STARTUP\n\n'
            text = 'Missouri S&T RDT Ground Control\n\n' \
                '>> Standard Operation\nxx Caution\n!! Warning\n\n' \
                'ALL BUTTONS MUST BE DOUBLE CLICKED\n'
            state = 3
            self.console_file = open(date_time.strftime(
                'GSECLOG_%m_%d_%Y_%H_%M_%S.txt'), 'a+')
        else:
            fmt = '%H:%M:%S : '

        state_indicators = ['>> ', 'xx ', '!! ', '']

        str_date_time = date_time.strftime(fmt)

        full_text = state_indicators[state] + str_date_time + text + '\n'
        self.console.configure(state='normal')
        self.console.insert(tk.END, full_text)
        self.console.configure(state='disabled')

        try:
            self.console_file.write(full_text)
        except:
            self.console.configure(state='normal')
            self.console.insert(
                tk.END, '!! WARNING - The console is no longer logging to the output file. '
                'Please restart the application or manually record events logged to the console.')
            self.console.configure(state='disabled')

            self.set_caution('GUI', 1)

        self.console.yview_pickplace('end')

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

    def run_launch(self):
        pass


if __name__ == '__main__':
    GUI = GUI_Window()
