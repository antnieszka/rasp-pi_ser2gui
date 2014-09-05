#!/usr/bin/python
# -*- coding: utf-8 -*-

from serial import Serial
from Tkinter import *
from time import sleep, time
#import re
import tkFont
from threading import Thread

# set to True for debug messages
debug = False
key_debug = False
anihi_key = False
spam_serial = True

# set to True for serial communication
ser_com = True

if debug: print("imports done!")

# serial settings
serial_bauds = 57600#9600
serial_port = '/dev/ttyACM0'#'/dev/ttyAMA0'
#serial_pattern = re.compile("\\w{4}\\ \\dx\\d{4}")

# advanced mode
advanced = False

# iterations with entry backgroud lit after updating its value
lightUpTime = 5

# holds button states and amp values
serial_table = {
	"KAMP":"",
	"HAMP":"",
	"AAMP":"",
	"GPER":"",
	"GAMP":""
}


if ser_com:
	ser = Serial(serial_port, serial_bauds, timeout=1)
	if debug: print("binding serial done!")

# Main window
root = Tk()

# backgroud
background_image = PhotoImage(file="img/back.gif")
background_label = Label(root, image=background_image)
background_label.photo = background_image
background_label.place(x=0, y=0, relwidth=1, relheight=1)

winWid = 640 #root.winfo_screenwidth()
winHei = 480 #root.winfo_screenheight()

wrapper = Tk()

# backgroud wrapper
background_image2 = PhotoImage(master=wrapper, file="img/back.gif")
background_label2 = Label(wrapper, image=background_image2)
background_label2.photo = background_image2
background_label2.place(x=0, y=0, relwidth=1, relheight=1)

# intervals between updating variables from serial
time_space = 25

# font for labels
labelFont = tkFont.Font(family = "Georgia", size = 14)

# key code for showing different windows
KeyCode = True
# switch killing serial thread
threadWork = True
# laste received message on serial port
last_received = ''

def receiving(ser):
    global last_received, threadWork

    buffer = ''
    while threadWork:
        buffer = buffer + ser.read(ser.inWaiting())
        if '\n' in buffer:
            lines = buffer.split('\n')
            if lines[-2]: last_received = lines[-2]
            buffer = lines[-1]
            sleep(0.01)
            
if ser_com:
	ser_th = Thread(target=receiving, args=(ser,)).start()

# lightup color
lightUpColour = 'grey'

# helper counters for entry bg lightup
gpert = 0
gampt = 0
kampt = 0
aampt = 0
hampt = 0

# updating method (checks serial for values)
def update_from_serial():
	# serial update
	if spam_serial:
		# key ON
		global last_received
		global gampt, gpert, hampt, kampt, aampt
		e = last_received[1:12]
		# checking for authorization
		if e[0:5] == 'KEY 0':
			print "-------" + e[9:10]
			if e[9:10] == '0':
				setKey(False)
				showWrapper()
			else:
			#elif e[9:10] == '1':
				setKey(True)
				showRoot()

	# if KeyCode we update entry values
	# authorization is KeyCode bool
	if KeyCode:
		if e[0:3] == 'ADV':
			if e[9:10] == '1':
				setMode(True)
			else:
				setMode(False)
		elif e[0:5] == 'GPER ':
			if serial_table["GPER"] <> e[5:11]:
				entStepTime['background'] = lightUpColour
				gpert = lightUpTime
				serial_table["GPER"] = e[5:11]
			print '>>>>>>>>>>>Got GPER with value: ' + e[5:11]
			#entStepTime.delete(0, END)
			#entStepTime.insert(0, e[5:11])
		elif e[0:5] == 'GAMP ':
			if serial_table["GAMP"] <> e[5:11]:
				entStepAmp['background'] = lightUpColour
				gampt = lightUpTime
				serial_table["GAMP"] = e[5:11]
			print 'Got GAMP with value: ' + e[5:11]
			#entStepAmp.delete(0, END)
			#entStepAmp.insert(0, e[5:11])
		elif e[0:4] == 'KAMP':
			if serial_table["KAMP"] <> e[5:11]:
				entKneeAmp['background'] = lightUpColour
				kampt = lightUpTime
				serial_table["KAMP"] = e[5:11]
			print 'Got KAMP with value: ' + e[5:11]
			#entKneeAmp.delete(0, END)
			#entKneeAmp.insert(0, e[5:11])
		elif e[0:4] == 'HAMP':
			if serial_table["HAMP"] <> e[5:11]:
				entHipAmp['background'] = lightUpColour
				hampt = lightUpTime
				serial_table["HAMP"] = e[5:11]
			print 'Got HAMP with value: ' + e[5:11]
			#entHipAmp.delete(0, END)
			#entHipAmp.insert(0, e[5:11])
		elif e[0:4] == 'AAMP':
			if serial_table["AAMP"] <> e[5:11]:
				entAnkAmp['background'] = lightUpColour
				aampt = lightUpTime
				serial_table["AAMP"] = e[5:11]
			print 'Got AAMP with value: ' + e[5:11]
			#entAnkAmp.delete(0, END)
			#entAnkAmp.insert(0, e[5:11])
		else:
			pass
		
		# show chosen entry
		if advanced:
			if e[0:4] == 'HMOD':
				labHipAmp['fg'] = fgBlue
				labAnkAmp['fg'] = 'black'
				labKneeAmp['fg'] = 'black'
			elif e[0:4] == 'AMOD':
				labHipAmp['fg'] = 'black'
				labAnkAmp['fg'] = fgBlue
				labKneeAmp['fg'] = 'black'
			elif e[0:4] == 'KMOD':
				labHipAmp['fg'] = 'black'
				labAnkAmp['fg'] = 'black'
				labKneeAmp['fg'] = fgBlue
			else:
				pass
		
		# if for lightup counters
		if gpert > 0:
			gpert -= 1
		else:
			entStepTime['background'] = 'white'
		if gampt > 0:
			gampt -= 1
		else:
			entStepAmp['background'] = 'white'
		if hampt > 0:
			hampt -= 1
		else:
			entHipAmp['background'] = 'white'
		if aampt > 0:
			aampt -= 1
		else:
			entAnkAmp['background'] = 'white'
		if kampt > 0:
			kampt -= 1
		else:
			entKneeAmp['background'] = 'white'
	else:
		# key OFF
		if debug: print 'nope'
		
	# value update for gui
	entStepTime.delete(0, END)
	entStepTime.insert(0, serial_table["GPER"])
	entStepAmp.delete(0, END)
	entStepAmp.insert(0, serial_table["GAMP"])
	entHipAmp.delete(0, END)
	entHipAmp.insert(0, serial_table["HAMP"])
	entKneeAmp.delete(0, END)
	entKneeAmp.insert(0, serial_table["KAMP"])
	entAnkAmp.delete(0, END)
	entAnkAmp.insert(0, serial_table["AAMP"])
	root.after(time_space, update_from_serial)  # reschedule event in time_space


# advanced widgets list
adv_widgets = []

# basic widgets list
bas_widgets = []

#entrySett = {"font":labelFont, "width":None, "justify":LEFT, "state":"normal", "takefocus":"no", "highlightthickness":False}
basicEntrySett = {"font":labelFont, "width":"7", "justify":LEFT, "state":"normal", "takefocus":"no", "highlightthickness":False}
advancedEntrySett = {"font":labelFont, "width":"7", "justify":LEFT, "state":"normal", "takefocus":"no", "highlightthickness":False}

buttonLabelSett = {"font":labelFont, "width":8, "justify":LEFT, "wraplength":"150"}
basicLabelSett = {"font":labelFont, "width":29, "justify":RIGHT, "wraplength":"500"}
advancedLabelSett = {"font":labelFont, "width":29, "justify":RIGHT, "wraplength":"500"}
rightButtonLabelSett = {"font":labelFont, "width":8, "justify":LEFT, "wraplength":"150"}

padTopLabel = (90,40)
padYLabel = 38
bgLabelLocked = '#eaf3fb'
# background settings for labels
bgRow1 = '#fefffc'
bgRow2 = '#e7f2f7'
bgRow3 = '#c6dae3'
bgRow4 = '#afc1cc'
# foreground settings for labels
fgBlue = '#1d96ca'

# label for button 0 on the left
buttonLabelSett["text"]="START "
button0 = Label(root, buttonLabelSett, bg=bgRow1)
button0.grid(row=1, column=1, sticky=W, pady=padTopLabel)
# label for button 1 on the left
buttonLabelSett["text"]="STOP   "
button1 = Label(root, buttonLabelSett, bg=bgRow2)
button1.grid(row=2, column=1, sticky=W, pady=padYLabel)
# label for button 2 on the left
buttonLabelSett["text"]="PAUZA "
button2 = Label(root, buttonLabelSett, bg=bgRow3)
button2.grid(row=3, column=1, sticky=W, pady=padYLabel)
# label for button 3 on the left
buttonLabelSett["text"]="ZAAWA."
button3 = Label(root, buttonLabelSett, bg=bgRow4)
button3.grid(row=4, column=1, sticky=W, pady=padYLabel)


# label for button 0 on the right
rightButtonLabelSett["text"]=u"Tk "+u"\u21E7"
labGperPlus = Label(root, rightButtonLabelSett, bg=bgRow1)
labGperPlus.grid(row=1, column=4, sticky=E, pady=padTopLabel)
# label for button 1 on the right
rightButtonLabelSett["text"]=u"Tk "+u"\u21E9"
labGperMinus = Label(root, rightButtonLabelSett, bg=bgRow2)
labGperMinus.grid(row=2, column=4, sticky=E, pady=padYLabel)
# label for button 2 on the right
rightButtonLabelSett["text"]=u"Wk "+u"\u21E7"
labGampPlus = Label(root, rightButtonLabelSett, bg=bgRow3)
labGampPlus.grid(row=3, column=4, sticky=E, pady=padYLabel)
# label for button 3 on the right
rightButtonLabelSett["text"]=u"Wk "+u"\u21E9"
labGampMinus = Label(root, rightButtonLabelSett, bg=bgRow4)
labGampMinus.grid(row=4, column=4, sticky=E, pady=padYLabel)

# banner for main window
#photo = PhotoImage(file="logo_small.gif")
#banner = Label(root, image=photo)
#banner.image = photo
#banner.grid(row=1, column=2, columnspan=2)

# info for keyCode block window
labStepTime = Label(wrapper, {"text":"Oczekiwanie na autoryzację...", \
"font":labelFont, "width":None, "justify":RIGHT, "wraplength":"500", \
"bg":bgLabelLocked})
#labStepTime.grid(row=2, column=2, pady=20)
labStepTime.place(x=200, y=200)

# banner
#ph2 = PhotoImage(master=wrapper, file="img/lol.gif")
#ban2 = Label(wrapper, image=ph2)
#ban2.image = ph2
#ban2.grid(row=1, column=2, padx=70, pady=50)

# basic widgets for hiding
basicLabelSett["text"] = "Czas trwania kroku (Tk):"
labStepTime = Label(root, basicLabelSett, bg=bgRow2)
labStepTime.grid(row=2, column=2, sticky=E)

basicLabelSett["text"] = "Wzmocnienie kroku (Wk):"
labStepAmp = Label(root, basicLabelSett, bg=bgRow3)
labStepAmp.grid(row=3, column=2, sticky=E)

entStepTime = Entry(root, basicEntrySett)
entStepTime.grid(row=2, column=3, sticky=W)

entStepAmp = Entry(root, basicEntrySett)
entStepAmp.grid(row=3, column=3, sticky=W)

bas_widgets.append(labStepTime)
bas_widgets.append(entStepTime)
bas_widgets.append(labStepAmp)
bas_widgets.append(entStepAmp)

# advanced widgets for hiding
advancedLabelSett["text"] = "Wzmocnienie stawu biodrowego:"
labHipAmp = Label(root, advancedLabelSett, bg=bgRow2)

advancedLabelSett["text"] = "Wzmocnienie stawu kolanowego:"
labKneeAmp = Label(root, advancedLabelSett, bg=bgRow3)

advancedLabelSett["text"] = "Wzmocnienie stawu skokowego:"
labAnkAmp = Label(root, advancedLabelSett, bg=bgRow4)

entHipAmp = Entry(root, advancedEntrySett)
entKneeAmp = Entry(root, advancedEntrySett)
entAnkAmp = Entry(root, advancedEntrySett)

adv_widgets.append(labHipAmp)
adv_widgets.append(labKneeAmp)
adv_widgets.append(labAnkAmp)
adv_widgets.append(entHipAmp)
adv_widgets.append(entKneeAmp)
adv_widgets.append(entAnkAmp)


def spawnAdvancedScreen():
	# hide basic widgets
	for w in bas_widgets:
		w.grid_forget()
	
	# change labels
	labGperPlus["text"] = u"wybór "+u"\u21E7"
	labGperMinus["text"] = u"wybór "+u"\u21E9"
	labGampPlus["text"] = u"wzm.  "+u"\u21E7"
	labGampMinus["text"] = u"wzm. "+u"\u21E9"
		
	# spawn advanced widgets
	#global labHipAmp, labKneeAmp, labAnkAmp
	labHipAmp.grid(row=2, column=2, sticky=E)
	labKneeAmp.grid(row=3, column=2, sticky=E)
	labAnkAmp.grid(row=4, column=2, sticky=E)
	entHipAmp.grid(row=2, column=3, sticky=W)
	entKneeAmp.grid(row=3, column=3, sticky=W)
	entAnkAmp.grid(row=4, column=3, sticky=W)


def respawnBasicScreen():
	# hide advanced widgets
	for w in adv_widgets:
		w.grid_forget()
	
	# change labels
	labGperPlus["text"] = u"Tk "+u"\u21E7"
	labGperMinus["text"] = u"Tk "+u"\u21E9"
	labGampPlus["text"] = u"Wk "+u"\u21E7"
	labGampMinus["text"] = u"Wk "+u"\u21E9"
		
	# spawn basic widgets
	labStepTime.grid(row=2, column=2, sticky=E)
	entStepTime.grid(row=2, column=3, sticky=W)
	labStepAmp.grid(row=3, column=2, sticky=E)
	entStepAmp.grid(row=3, column=3, sticky=W)

def switchMode():
	global advanced
	if advanced:
		advanced = False
		respawnBasicScreen()
	else:
		advanced = True
		spawnAdvancedScreen()

def setMode(newMode):
	global advanced
	advanced = newMode
	if advanced:
		spawnAdvancedScreen()
	else:
		respawnBasicScreen()
	
def togKey():
	global KeyCode
	if KeyCode:
		KeyCode = False
	else:
		KeyCode = True
	if debug: print KeyCode

def setKey(newKey):
	global KeyCode
	KeyCode = newKey
	if debug: print KeyCode

def showRoot():
	root.overrideredirect(True)
	root.geometry("{0}x{1}+0+0".format(winWid, winHei))
	#root.after(time_space, update_from_serial)
	root.update()
	root.deiconify()
	wrapper.withdraw()
	
def showWrapper():
	wrapper.overrideredirect(True)
	wrapper.geometry("{0}x{1}+0+0".format(winWid, winHei))
	wrapper.update()
	wrapper.deiconify()
	root.withdraw()

def killall():
	global threadWork
	threadWork = False
	sys.exit()

# temp buttons for debug
if key_debug:
	exitButton = Button(root, text = "Toggle view", command = showWrapper)
	exitButton.grid(row=5, column=2)
	
	exitButtonWr = Button(wrapper, text = "Toggle view", command = showRoot, width=10)
	#exitButtonWr.grid(row=3, column=2)
	exitButtonWr.place(x=winWid/2-60, y=230)

	switchButton = Button(root, text = "Advanced", command = switchMode)
	switchButton.grid(row=5, column=3)
	
	keyButton = Button(root, text = "Toggle key", command = togKey)
	keyButton.grid(row=5, column=4)
	
	keyButton2 = Button(wrapper, text = "Toggle key", command = togKey, width=10)
	#keyButton2.grid(row=4, column=2)
	keyButton2.place(x=winWid/2-60, y=260)

if anihi_key:
	closeB = Button(wrapper, text = "Annihilate", command = killall, width=10)
	#closeB.grid(row=5, column=2)
	closeB.place(x=winWid/2-60, y=290)
	
	closeC = Button(wrapper, text='x', command = killall, width=1)
	closeC.place(x=600, y=5)

root.title("ArduPi 0.7.3")

root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(winWid, winHei))
root.after(time_space, update_from_serial)
root.withdraw()
wrapper.overrideredirect(True)
wrapper.geometry("{0}x{1}+0+0".format(winWid, winHei))

wrapper.mainloop()
root.mainloop()
