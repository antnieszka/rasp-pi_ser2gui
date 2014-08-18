#!/usr/bin/python

from serial import Serial
from Tkinter import *
from time import sleep, time
import re
import tkFont

# set to True for debug messages
debug = True

# set to True for serial communication
ser_com = False

if debug: print("imports done!")

# serial settings
serial_bauds = 9600
serial_port = '/dev/ttyACM0'
serial_pattern = re.compile("\\w\\w\\w\\ \\dx\\d{4}")

# advanced mode
advanced = False


# holds button states and amp values
serial_table = {
	"BTT1":0,
	"BTT2":0,
	"BTT3":0,
	"BTT4":0,
	"BTT5":0,
	"BTT6":0,
	"BTT7":0,
	"BTT8":0,
	"BTT9":0,
	"KAMP":"",
	"HAMP":"",
	"AAMP":"",
	"GPER":""
}

#print "" == serial_table["AAMP"]

if ser_com:
	ser = Serial(serial_port, serial_bauds)
	if debug: print("binding serial done!")

# Main window
root = Tk()

# intervals between updating variables from serial
time_space = 100

# font for labels
labelFont = tkFont.Font(family = "Georgia", size = 32)

def update_mode():
	# if advanced mode is toggled ON
	if advanced:
		for w in adv_widgets:
			w.grid_forget()
	else:
		for w in adv_widgets:
			w.grid()

# updating method (checks serial for values)
def update_from_serial():
	# update mode
	update_mode()
	# serial update
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
ham.grid(row=1, column=3, padx=label_padx, pady=label_pady)
kwz = Label(root, text = 'KWZ value:', font = labelFont)
kwz.grid(row=3, column=1, padx=label_padx, pady=label_pady)
hwz = Label(root, text = 'HWZ value:', font = labelFont)
hwz.grid(row=3, column=3, padx=label_padx, pady=label_pady)

kamv = Entry(root, font = labelFont, width=entry_width, justify=CENTER, state="normal", takefocus="no", highlightthickness=False)
kamv.grid(row=2, column=1, padx=entry_padx, pady=entry_pady)
hamv = Entry(root, font = labelFont, width=entry_width)
hamv.grid(row=2, column=3, padx=entry_padx, pady=entry_pady)
kwzv = Entry(root, font = labelFont, width=entry_width)
kwzv.grid(row=4, column=1, padx=entry_padx, pady=entry_pady)
hwzv = Entry(root, font = labelFont, width=entry_width)
hwzv.grid(row=4, column=3, padx=entry_padx, pady=entry_pady)

adv_widgets = []
adv_widgets.append(kamv)
adv_widgets.append(hamv)

def switchMode():
	global advanced
	if advanced:
		advanced = False
	else:
		advanced = True

# temp buttons for debug
if debug:
	exitButton = Button(root, text = "Zamknij", command=quit)
	exitButton.grid(row=6, column=2)

	switchButton = Button(root, text = "Zaawansowane", command=switchMode)
	switchButton.grid(row=6, column=3)

root.title("ArduPi 0.3.2")
#root.geometry("1000x600")

root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

root.after(time_space, update_from_serial)
#root.bind("<Escape>", quit)
root.mainloop()
