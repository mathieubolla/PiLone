# -*- coding: utf8 -*-

# runs a small webserver on specified port that allows picking a color, and applying to a diode
# open http://[bind]:[port]/ to access control web page
# do not forget to specify serial port for your Raspberry Pi at startup
# uses http://pyserial.sourceforge.net/shortintro.html "pip install pyserial"
# uses http://bottlepy.org/docs/dev/index.html "pip install bottle"

import serial
import time
import sys, getopt
from bottle import route, run, static_file
import strand.Strand

@route('/')
def index():
    return static_file('index.html', sys.path[0], mimetype='text/html')

@route('/<line>/<led>/<color1>/<color2>')
def set_one(line, led, color1, color2):
    ser.print_color(line, led, color1, color2)
    return {'line': line, 'led': led, 'color1': color1, 'color2': color2}

def light_show(serial_line):
    count = 0
    while True:
        for pilone in range(0, 3):
            for led in range(0, 8):
                serial_line.print_color(pilone, led, "FFFFFF", "FFFFFF")
                time.sleep(0.1)
                serial_line.print_color(pilone, led, "000000", "000000")
        count += 1
        if count >= 2:
            break

def main(argv):
    global ser
    portNumber = ''
    bindToHost = 'localhost'
    serialPort = ''

    try:
        opts, args = getopt.getopt(argv, "hp:b:s:", ["port=", "bind=", "serial="])
    except getopt.GetoptError:
        print 'test.py -p <portNumber> -b <bindToHost> -s <serialPort>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-p", "--port"):
            portNumber = arg
        elif opt in ("-b", "--bind"):
            bindToHost = arg
        elif opt in ("-s", "--serial"):
            serialPort = arg

    ser = strand.Strand(serial.Serial(serialPort, 57600, timeout=1))

    time.sleep(2)
    light_show(ser)

    run(host=bindToHost, port=portNumber)
    ser.close()

if __name__ == "__main__":
    main(sys.argv[1:])