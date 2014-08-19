__author__ = 'Mathieu Bolla'
__copyright__ = 'Copyright 2014, Mathieu Bolla'
__licence__ = 'GPL V3.0'

class Strand:
    serial = None

    def __init__(self, serial_parameter):
        self.serial = serial_parameter

    def check_spec(self, color_spec):
        control_code = 0
        for i in range(0, len(color_spec)):
            control_code ^= ord(color_spec[i])
        return control_code

    def print_color(self, led, color1, color2):
        color_spec = "{:02x}{:}{:}\n".format(led, color1, color2).upper()

        print color_spec

        self.serial.write(color_spec)
        arduino_said = "0x" + self.serial.readline().strip()
        we_say = hex(self.check_spec(color_spec))

        i = 0
        while True:
            i += 1
            if (we_say == arduino_said) | (i > 10):
                break

    def close(self):
        self.serial.close()