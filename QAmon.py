#!/usr/bin/python
import os

os.environ['DISPLAY'] = ":0"


import gtk, pygtk
import sys, glob, re, time, socket
import subprocess, shlex


# Open monitoring file
os.chdir('/var/home/resource/monitor')
MonFile = open('/var/home/resource/monitor/LTXC_PAx_Dragon.mon', 'r')
MonLines = MonFile.readlines()
MonFile.close()

# Initalize variables
CurrentLimits = ""
CurrentLotID = ""
tester = ""
SendAlert = False


# Read monitoring file to get limits and lotID
for line in MonLines:
	if "Lot Number:" in line:
		line = line.split(':')
		line[1] = re.sub("\n", "", line[1])
		CurrentLotID = re.sub(" ", "", line[1])
	if "Limit Set:" in line:
		line = line.split(':')
		line[1] = re.sub("\n", "", line[1])
		CurrentLimits = re.sub(" ", "", line[1])
	if "Equipment ID:" in line:
		line = line.split(':')
		line[1] = re.sub("\n", "", line[1])
		tester = re.sub(" ", "", line[1])
	if CurrentLimits and CurrentLotID and tester:
		break

# Debug
print CurrentLimits, CurrentLotID, tester


# Define message and command
Message = """\
Alarma!!!!
Se detectaron limites de QA con lote fresco!
No se puede correr asi.
Se descargara el programa.
LotID: %s
Limits: %s
""" % (CurrentLotID, CurrentLimits)
GetUser = os.popen("/opt/ltx/releases/U4.3.1/x86_64_linux_2.6.32/com/cex -t %s -c get_username" % tester).read()
User = GetUser[GetUser.find("owner:")+7:]
User = re.sub("\n","", User)
UnloadCommand = "su %s -c '/opt/ltx/releases/U4.3.1/x86_64_linux_2.6.32/com/cex -t %s -command stop_session'" % (User, tester)
# UnloadCommand = "/opt/ltx/releases/U4.3.1/x86_64_linux_2.6.32/com/cex -t %s -command stop_session" % tester
# UnloadCommand = "ltx/com/restart_tester %s" % tester

# Check limits vs LotID
if "QA" in CurrentLimits.upper():
	if not "QA" in CurrentLotID.upper() and not "X" in CurrentLotID.upper()[0]:
		SendAlert = True

# Show alarm 
if SendAlert:
# if True:
	# os.system(UnloadCommand)
	Error = gtk.MessageDialog(
		parent = None,
		flags = 0,
		type = gtk.MESSAGE_WARNING,
		buttons = gtk.BUTTONS_OK,
		message_format = Message)
	Error.show_all()
	while gtk.events_pending():
		gtk.main_iteration_do(False)

	output = os.popen(UnloadCommand).read()


	res = Error.run()
	if res:
		Error.destroy()
exit(0)

