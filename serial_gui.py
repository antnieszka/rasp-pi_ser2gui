#!/usr/bin/python
# -*- coding: utf-8 -*-

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
		kamv.grid(row=2, column=1, padx=entry_padx, pady=entry_pady)
		hamv.grid(row=2, column=3, padx=entry_padx, pady=entry_pady)

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


entrySett = {"font":labelFont, "width":None, "justify":CENTER, "state":"normal", "takefocus":"no", "highlightthickness":False}
basicLabelSett = {"font":labelFont, "width":None, "justify":LEFT, "wraplength":"300"}

def createBasicScreen():
	global basicLabelSett
	# ustawienia fabryczne
	holder1 = Label(root, width=root.winfo_screenwidth()/3)
	holder1.grid(row=1, column=1)
	basicLabelSett["text"]="Przywróć ustawienia fabryczne"
	labDefSett = Label(root, basicLabelSett)
	labDefSett.grid(row=1, column=1, sticky=W, pady=0)
	# przycisk pierwszy, po lewej
	basicLabelSett["text"]="przycisk pierwszy"
	button1 = Label(root, basicLabelSett)
	button1.grid(row=2, column=1, sticky=W, pady=30)
	# przycisk drugi, po lewej
	basicLabelSett["text"]="przycisk drugi"
	button2 = Label(root, basicLabelSett)
	button2.grid(row=3, column=1, sticky=W, pady=30)
	# przycisk trzeci, po lewej
	basicLabelSett["text"]="przycisk trzeci"
	button3 = Label(root, basicLabelSett)
	button3.grid(row=4, column=1, sticky=W, pady=30)

createBasicScreen()

kamv = Entry(root, entrySett)
kamv.grid(row=2, column=1)
hamv = Entry(root, entrySett)
hamv.grid(row=2, column=3)

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
	exitButton.grid(row=3, column=2)

	switchButton = Button(root, text = "Zaawansowane", command=switchMode)
	switchButton.grid(row=6, column=3)

# banner
photo = PhotoImage(file="logo.gif")
banner = Label(root, image=photo)
banner.grid(row=1, column=1, sticky="N", columnspan=3)

root.title("ArduPi 0.3.2")
#root.geometry("1000x600")

root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

root.after(time_space, update_from_serial)
#root.bind("<Escape>", quit)
root.mainloop()
