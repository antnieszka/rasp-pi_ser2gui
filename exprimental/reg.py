import re
from serial import Serial

regex = re.compile("\\w\\w\\w\\ \\dx\\d\\d\\d\\d\\n")

serial_bauds = 9600
serial_port = '/dev/ttyACM0'
serial_pattern = re.compile("\\w\\w\\w\\ \\dx\\d{4}")

ser = Serial(serial_port, serial_bauds)

while 1:
	line = ser.readline()
	match = serial_pattern.findall(line)
	for e in match: print "recieved: " + e
