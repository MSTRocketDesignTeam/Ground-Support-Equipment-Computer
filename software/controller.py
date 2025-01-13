
class Controller():
    '''
    This class handles the bulk of work for the system by packaging low 
    level micropython functions into events that can be triggered by the GUI.
    '''

    def __init__(self, timestamp):

        # Setup controller state map:
        #  0 >>> Nominal / off
        #  1 >>> Caution / on
        #  2 >>> Warning
        # -1 >>> Unknown

        self.state = {
            'fill_valve': -1,
            'ox_valve': -1,
            'fuel_valve': -1,

            'auto_mode': 0,
            'interlocks': 0,

            'arm': 0,
            'igniter_lit': 0,

            'LEC_link_status': -1,
            'LEC_status': -1,
            'GUI_status': -1,

            'fuel_tank_pt': -1,
            'ox_tank_pt': -1,
            'fuel_venturi_pt': -1,
            'ox_venturi_pt': -1,
            'chamber_pt': -1,
            'ox_tc': -1,
            'chamber_tc': -1,

            'error_override_flag': 0,
            'emergency_stop_flag': 0,

            'tank_full': 0,
        }

        self.record = {}

    def estop(self):
        '''
        Runs the emergency stop procedure to safe the entire
        system as quickly as possible.
        '''

        # Insert calls to micropython

        message = 'E-Stop Button Pressed'
        status = 2
        return (message, status)

    def open_fill(self):
        '''
        Attempts to open the fill valve and handles
        the corresponding error code from micropython.
        '''
        message = 'Fill valve opened'
        status = 2

        return (message, status)

    def close_fill(self):
        '''
        Attempts to close the oxidizer valves and handles the
        corresponding error code from micropython.
        '''
        message = 'E-Stop button pressed'
        status = 2
        return (message, status)

    def launch(self):
        message = 'Launch button pressed'
        status = 2

        return (message, status)

    def get_fill_state(self):
        '''Returns the fill state of the oxidizer tank as an ordered tuple.'''
        return (.3, 60)

    def record_state(self):
        pass

    def ignite(self):
        message = 'Ignite button pressed'
        status = 2

        return (message, status)

    def dump(self):
        message = 'Dump button pressed'
        status = 2

        return (message, status)

    def open_mains(self):
        message = 'Mains open button pressed'
        status = 2

        return (message, status)
