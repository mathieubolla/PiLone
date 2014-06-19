# -*- coding: utf8 -*-

# uses http://pyserial.sourceforge.net/shortintro.html "pip install pyserial"
# uses http://bottlepy.org/docs/dev/index.html "pip install bottle"

import serial
import time
import sys, getopt
from bottle import route, run, template, static_file

def printColor(serial, pilone, led, color):
	serial.write("{0}{1}{2}\n".format(pilone, led, color))

ser = None

@route('/')
def index():
	return static_file('index.html', sys.path[0], mimetype='text/html')

@route('/<pilone>/<led>/<color>')
def setOne(pilone, led, color):
	printColor(ser, pilone, led, color)
	return template('<b>Coucou, {{pilone}}, {{led}}, {{color}}', pilone=pilone, led=led, color=color)

def lightShow(serial):
	count = 0
	while True:
		for pilone in range(0, 2):
			for led in range(0, 8):
				printColor(serial, pilone, led, "FFFFFF")
				time.sleep(0.1)
				printColor(serial, pilone, led, "000000")
		count += 1
		if count >= 2:
			break

def main(argv):
	global ser
	portNumber = ''
	bindToHost = 'localhost'
	serialPort = ''

	try:
		opts, args = getopt.getopt(argv,"hp:b:s:",["port=","bind=","serial="])
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
	
	print 'portNumber is ', portNumber
	print 'bindToHost is ', bindToHost
	print 'serialPort is ', serialPort

	ser = serial.Serial(serialPort, 57600, timeout=1)

	time.sleep(1.5)
	lightShow(ser)

	run(host=bindToHost, port=portNumber)
	ser.close()

if __name__ == "__main__":
   main(sys.argv[1:])