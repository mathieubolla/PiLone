__author__ = 'mathieubolla'

class Strand:
    serial = None

    def __init__(self, serial_parameter):
        self.serial = serial_parameter

    def print_color(self, pilone, led, color1, color2):
        color_spec = "{0}{1}{2}{3}\n".format(pilone, led, color1, color2)
        self.serial.write(color_spec)

    def close(self):
        self.serial.close()