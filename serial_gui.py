#!/usr/bin/python

from serial import Serial
from Tkinter import *
from time import sleep, time
import re
import tkFont

debug = True
ser_com = True

if debug: print("imports done!")

# serial settings
serial_bauds = 9600
serial_port = '/dev/ttyACM0'
serial_pattern = re.compile("\\w\\w\\w\\ \\dx\\d{4}")

if ser_com:
	ser = Serial(serial_port, serial_bauds)
	if debug: print("binding serial done!")

# Main window
root = Tk()

# intervals between updating variables from serial
time_space = 100

# font for labels
labelFont = tkFont.Font(family = "Georgia", size = 32)

# font for variables in text boxes

# updating method (checks serial for values)
def update_from_serial():
    if debug: print "update - " + str(time())
    
    # get values from serial named 'ser'
    if ser_com:
		line = ser.readline()
		if debug: print 'raw: ' + line
		match = serial_pattern.findall(line)
		if debug:
			for e in match:
				print "recieved: " + e
				
		# update gui values
		for e in match:
			if e[0:3] == 'kam':
				print 'Got KAM with value: ' + e[4:10]
				#kam['text'] = e[4:10]
				kamv.delete(0, END)
				kamv.insert(0, e[4:10])
			elif e[0:3] == 'ham':
				print 'Got HAM with value: ' + e[4:10]
				#ham['text'] = e[4:10]
				hamv.delete(0, END)
				hamv.insert(0, e[4:10])
			elif e[0:3] == 'kwz':
				print 'Got KWZ with value: ' + e[4:10]
				#kwz['text'] = e[4:10]
				kwzv.delete(0, END)
				kwzv.insert(0, e[4:10])
			elif e[0:3] == 'hwz':
				print 'Got HWZ with value: ' + e[4:10]
				#hwz['text'] = e[4:10]
				hwzv.delete(0, END)
				hwzv.insert(0, e[4:10])

		
    #kam['text'] = str(time())
    #ham['text'] = str(time())
    #kwz['text'] = str(time())
    #hwz['text'] = str(time())
    
    root.after(time_space, update_from_serial)  # reschedule event in 2 seconds

# conts for guid grid padding
label_padx = 100
label_pady = 20
entry_padx = 100
entry_pady = 20
entry_width = 10

kam = Label(root, text = 'KAM value:', font = labelFont)
kam.grid(row=1, column=1, padx=label_padx, pady=label_pady)
ham = Label(root, text = 'HAM value:', font = labelFont)
ham.grid(row=1, column=2, padx=label_padx, pady=label_pady)
kwz = Label(root, text = 'KWZ value:', font = labelFont)
kwz.grid(row=3, column=1, padx=label_padx, pady=label_pady)
hwz = Label(root, text = 'HWZ value:', font = labelFont)
hwz.grid(row=3, column=2, padx=label_padx, pady=label_pady)

kamv = Entry(root, font = labelFont, width=entry_width)
kamv.grid(row=2, column=1, padx=entry_padx, pady=entry_pady)
hamv = Entry(root, font = labelFont, width=entry_width)
hamv.grid(row=2, column=2, padx=entry_padx, pady=entry_pady)
kwzv = Entry(root, font = labelFont, width=entry_width)
kwzv.grid(row=4, column=1, padx=entry_padx, pady=entry_pady)
hwzv = Entry(root, font = labelFont, width=entry_width)
hwzv.grid(row=4, column=2, padx=entry_padx, pady=entry_pady)

root.title("ArduPi 0.3.1")
root.geometry("1000x600")
root.after(time_space, update_from_serial)
root.bind("<Escape>", quit)
root.mainloop()
