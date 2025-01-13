import random


class Test_Command_Wrapper():
    def read_sensors(self):
        pass

    def open_fill_valve(self):
        pass

    def open_ox_valve(self):
        pass

    def open_fuel_valve(self):
        pass

    def close_fill_valve(self):
        pass

    def close_ox_valve(self):
        pass

    def close_fuel_valve(self):
        pass

    def light_igniter(self):
        pass

    def random_error(self, **kwargs):
        probablity = kwargs.get('probability', .5)

        if random.random() > 'probability':
            return 1
