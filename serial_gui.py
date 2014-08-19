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

# banner
photo = PhotoImage(file="logo.gif")

# intervals between updating variables from serial
time_space = 100

# font for labels
labelFont = tkFont.Font(family = "Georgia", size = 32)



# updating method (checks serial for values)
def update_from_serial():
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


# advanced widgets list
adv_widgets = []

# basic widgets list
bas_widgets = []

entrySett = {"font":labelFont, "width":None, "justify":LEFT, "state":"normal", "takefocus":"no", "highlightthickness":False}
basicEntrySett = {"font":labelFont, "width":"10", "justify":LEFT, "state":"normal", "takefocus":"no", "highlightthickness":False}
advancedEntrySett = {"font":labelFont, "width":"10", "justify":LEFT, "state":"disabled", "takefocus":"no", "highlightthickness":False}

buttonLabelSett = {"font":labelFont, "width":None, "justify":LEFT, "wraplength":"300"}
basicLabelSett = {"font":labelFont, "width":None, "justify":RIGHT, "wraplength":"500"}
advancedLabelSett = {"font":labelFont, "width":None, "justify":RIGHT, "wraplength":"500"}

# ustawienia fabryczne
buttonLabelSett["text"]="Przywróć ustawienia fabryczne"
labDefSett = Label(root, buttonLabelSett)
labDefSett.grid(row=1, column=1, sticky=W, padx=0)
# przycisk pierwszy, po lewej
buttonLabelSett["text"]="przycisk pierwszy"
button1 = Label(root, buttonLabelSett)
button1.grid(row=2, column=1, sticky=W, pady=30)
# przycisk drugi, po lewej
buttonLabelSett["text"]="przycisk drugi"
button2 = Label(root, buttonLabelSett)
button2.grid(row=3, column=1, sticky=W, pady=30)
# przycisk trzeci, po lewej
buttonLabelSett["text"]="przycisk trzeci"
button3 = Label(root, buttonLabelSett)
button3.grid(row=4, column=1, sticky=W, pady=30)

# banner
banner = Label(root, image=photo)
banner.grid(row=1, column=2)

# basic widgets for hiding
basicLabelSett["text"] = "Czas trwania kroku:"
labStepTime = Label(root, basicLabelSett)
labStepTime.grid(row=2, column=2, sticky=E)

basicLabelSett["text"] = "Amplituda kroku:"
labStepAmp = Label(root, basicLabelSett)
labStepAmp.grid(row=3, column=2, sticky=E)

entStepTime = Entry(root, basicEntrySett)
entStepTime.grid(row=2, column=3, sticky=W)

entStepAmp = Entry(root, basicEntrySett)
entStepAmp.grid(row=3, column=3, sticky=W)

bas_widgets.append(labStepTime)
bas_widgets.append(entStepTime)

# advanced widgets for hiding
advancedLabelSett["text"] = "Amplituda biodra:"
labHipAmp = Label(root, advancedLabelSett)

advancedLabelSett["text"] = "Amplituda czegoś:"
labMoreAmp = Label(root, advancedLabelSett)

entHipAmp = Entry(root, advancedEntrySett)

entMoreAmp = Entry(root, advancedEntrySett)

adv_widgets.append(labHipAmp)
adv_widgets.append(labMoreAmp)
adv_widgets.append(entHipAmp)
adv_widgets.append(entMoreAmp)


def spawnAdvancedScreen():
	# hide basic widgets
	for w in bas_widgets:
		w.grid_forget()
		
	# spawn advanced widgets
	global labHipAmp
	global labMoreAmp
	labHipAmp.grid(row=2, column=2, sticky=E)
	labMoreAmp.grid(row=4, column=2, sticky=E)
	entHipAmp.grid(row=2, column=3, sticky=W)
	entMoreAmp.grid(row=4, column=3, sticky=W)


def respawnBasicScreen():
	# hide advanced widgets
	for w in adv_widgets:
		w.grid_forget()
		
	# spawn basic widgets
	labStepTime.grid(row=2, column=2, sticky=E)
	entStepTime.grid(row=2, column=3, sticky=W)

def switchMode():
	global advanced
	if advanced:
		advanced = False
		respawnBasicScreen()
	else:
		advanced = True
		spawnAdvancedScreen()

# temp buttons for debug
if debug:
	exitButton = Button(root, text = "Zamknij", command = quit)
	exitButton.grid(row=5, column=2)

	switchButton = Button(root, text = "Zaawansowane", command = switchMode)
	switchButton.grid(row=5, column=3)

root.title("ArduPi 0.4.1")

#createBasicScreen()

root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

root.after(time_space, update_from_serial)
#root.bind("<Escape>", quit)
root.mainloop()
