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
serial_port = '/dev/ttyAMA0'
serial_pattern = re.compile("\\w{3,4}\\ \\dx\\d{4}")
serial_key = re.compile("KEY\\ \\w{2,3}")

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
	"GPER":"",
	"GAMP":""
}


if ser_com:
	ser = Serial(serial_port, serial_bauds)
	if debug: print("binding serial done!")

# Main window
root = Tk()

winWid = 800 #root.winfo_screenwidth()
winHei = 600 #root.winfo_screenheight()

wrapper = Tk()

# intervals between updating variables from serial
time_space = 100

# font for labels
labelFont = tkFont.Font(family = "Georgia", size = 24)

# key code for showing different windows
KeyCode = False

# updating method (checks serial for values)
def update_from_serial():
	# serial update
	
	if KeyCode:
		# key ON
		print 'fuck'
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
					
	else:
		# key OFF
		print 'nope'
	root.after(time_space, update_from_serial)  # reschedule event in time_space


# advanced widgets list
adv_widgets = []

# basic widgets list
bas_widgets = []

#entrySett = {"font":labelFont, "width":None, "justify":LEFT, "state":"normal", "takefocus":"no", "highlightthickness":False}
basicEntrySett = {"font":labelFont, "width":"6", "justify":LEFT, "state":"normal", "takefocus":"no", "highlightthickness":False}
advancedEntrySett = {"font":labelFont, "width":"6", "justify":LEFT, "state":"disabled", "takefocus":"no", "highlightthickness":False}

buttonLabelSett = {"font":labelFont, "width":8, "justify":LEFT, "wraplength":"150"}
basicLabelSett = {"font":labelFont, "width":18, "justify":RIGHT, "wraplength":"500"}
advancedLabelSett = {"font":labelFont, "width":18, "justify":RIGHT, "wraplength":"500"}
rightButtonLabelSett = {"font":labelFont, "width":8, "justify":LEFT, "wraplength":"150"}

# label for button 0 on the left
buttonLabelSett["text"]="START "
button0 = Label(root, buttonLabelSett)
button0.grid(row=1, column=1, sticky=W, pady=50)
# label for button 1 on the left
buttonLabelSett["text"]="STOP   "
button1 = Label(root, buttonLabelSett)
button1.grid(row=2, column=1, sticky=W, pady=50)
# label for button 2 on the left
buttonLabelSett["text"]="PAUZA "
button2 = Label(root, buttonLabelSett)
button2.grid(row=3, column=1, sticky=W, pady=50)
# label for button 3 on the left
buttonLabelSett["text"]="ADV    "
button3 = Label(root, buttonLabelSett)
button3.grid(row=4, column=1, sticky=W, pady=50)


# label for button 0 on the right
rightButtonLabelSett["text"]="GPER+"
labGperPlus = Label(root, rightButtonLabelSett)
labGperPlus.grid(row=1, column=4, sticky=E)
# label for button 1 on the right
rightButtonLabelSett["text"]="GPER-"
labGperMinus = Label(root, rightButtonLabelSett)
labGperMinus.grid(row=2, column=4, sticky=E)
# label for button 2 on the right
rightButtonLabelSett["text"]="GAMP+"
labGampPlus = Label(root, rightButtonLabelSett)
labGampPlus.grid(row=3, column=4, sticky=E)
# label for button 3 on the right
rightButtonLabelSett["text"]="GAMP-"
labGampMinus = Label(root, rightButtonLabelSett)
labGampMinus.grid(row=4, column=4, sticky=E)

# banner for main window
photo = PhotoImage(file="logo_small.gif")
banner = Label(root, image=photo)
banner.image = photo
banner.grid(row=1, column=2, columnspan=2)

# info for keyCode block window
#basicLabelSett["text"] = "Koteł przeprasza :< Trwają prace konserwatorskie..."
labStepTime = Label(wrapper, {"text":"Koteł przeprasza :< Trwają prace konserwatorskie...", \
"font":labelFont, "width":None, "justify":RIGHT, "wraplength":"500"})
labStepTime.grid(row=2, column=2, pady=20)

# banner
ph2 = PhotoImage(master=wrapper, file="lol.gif")
ban2 = Label(wrapper, image=ph2)
ban2.image = ph2
ban2.grid(row=1, column=2, padx=150, pady=100)

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

def togKey():
	global KeyCode
	if KeyCode:
		KeyCode = False
	else:
		KeyCode = True
	print KeyCode

def showRoot():
	wrapper.withdraw()
	root.overrideredirect(True)
	root.geometry("{0}x{1}+0+0".format(winWid, winHei))
	root.after(time_space, update_from_serial)
	root.update()
	root.deiconify()
	
def showWrapper():
	root.withdraw()
	wrapper.overrideredirect(True)
	wrapper.geometry("{0}x{1}+0+0".format(winWid, winHei))
	wrapper.update()
	wrapper.deiconify()

# temp buttons for debug
if debug:
	exitButton = Button(root, text = "Toggle view", command = showWrapper)
	exitButton.grid(row=5, column=2)
	
	exitButtonWr = Button(wrapper, text = "Toggle view", command = showRoot)
	exitButtonWr.grid(row=3, column=2)

	switchButton = Button(root, text = "Advanced", command = switchMode)
	switchButton.grid(row=5, column=3)
	
	keyButton = Button(root, text = "Toggle key", command = togKey)
	keyButton.grid(row=5, column=4)
	
	keyButton2 = Button(wrapper, text = "Toggle key", command = togKey)
	keyButton2.grid(row=4, column=2)
	
	closeB = Button(wrapper, text = "Annihilate", command = exit)
	closeB.grid(row=5, column=2)

root.title("ArduPi 0.5.1")

root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(winWid, winHei))
root.after(time_space, update_from_serial)
root.withdraw()
wrapper.overrideredirect(True)
wrapper.geometry("{0}x{1}+0+0".format(winWid, winHei))

wrapper.mainloop()
root.mainloop()
