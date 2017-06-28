#!/usr/bin/python
# Telnet Honeypot v1.0 (Designed to emulate Airties Air6372SO telnetd)
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com
#
# Based on manhole/telnet.py by Twisted Matrix Laboratories


# twisted imports
from twisted.protocols import telnet
# from twisted.internet import protocol
from twisted.internet.protocol import Protocol, Factory
# from twisted.python import log, failure
from twisted.internet import reactor

# system imports
import string, copy, sys, os, datetime, subprocess, mechanize, cookielib

IAC = chr(255)
WILL = chr(251)
WONT = chr(252)
ECHO  = chr(1)

debug = 0

class Shell(telnet.Telnet):
    fail_count = 0

    def get_ip(self):
	return self.transport.getPeer().host

    def get_date(self):
        now = datetime.datetime.now()
        time = now.strftime("%d-%m-%Y %H:%M:%S")
	return time

    def who_when(self):
	source = self.get_ip()
	date = self.get_date()
	who_when = date + "|" + str(source) + "|"
	return who_when  

    def log(self, txt):
	try:
		now = datetime.datetime.now()
		time = now.strftime("%d-%m-%Y %H:%M:%S")
		file = open(logfile, "a")
		# txt = str(time + " - " + txt.encode("cp1254") + "\n")
		txt = str(txt.encode("cp1254") + "\n")
		file.write(txt)
		file.close()
	except:
		pass

    def run_wget(self, cmd):
	print cmd.split(" ")[0], "".join(cmd.split(" ")[1:])
	p = subprocess.Popen([cmd.split(" ")[0], "".join(cmd.split(" ")[1:])],
		stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT,
		cwd=r'/home/honeypot/archive')
	out, err = p.communicate()
	return out

    def cmd_wget(self, cmd):
        try:
                param = cmd.split(" ")[1]
        except:
                param = 0
        if param:
		self.write(self.run_wget(cmd))
                return "Done"
        else:
                self.write("BusyBox v1.14.1 (2011-10-25 17:21:22 EEST) multi-call binary\r\n\r\n")
                self.write("Usage: wget [-csq] [-O file] [-Y on/off] [-P DIR] [-U agent] url\r\n\r\n")
		return "Done"

    def cmd_exit(self, cmd):
	try:
		param = cmd.split(" ")[1]
	except:
		param = 0
	if not param:
		self.log(self.who_when() + "Connection Closed!")
		print self.who_when() + "Connection Closed!"
		self.transport.abortConnection()
		return "Done"
	if param.isdigit():
		self.log(self.who_when() + "Connection Closed!")
		print self.who_when() + "Connection Closed!"
		self.transport.abortConnection()
		return "Done"
	else:
		self.write("-sh: exit: Illegal number: " + param + "\r\n")
		return "Done"

    def cmd_help(self):
	if debug:
		print "cmd_help()"
	self.write("Built-in commands:\r\n")
	self.write("------------------\r\n")
	self.write("\t. : [ alias bg break cd chdir continue echo eval exec exit export\r\n")
	self.write("\tfalse fg hash help jobs kill let local pwd read readonly return\r\n")
	self.write("\tset shift source test times trap true type ulimit umask unalias\r\n")
	self.write("\tunset wait\r\n")

    def connectionLost(self, reason):
        # self.log(self.get_date() + "|Connection Closed!")
        # print self.get_date() + "|Connection Closed!"
        return "Done"

    def connectionMade(self):
	# self.log(self.who_when() + "Connected!")
	print self.who_when() + "Connected!"
	self.write(self.loginPrompt())
	# self.lineBuffer = []

    def welcomeMessage(self):
	if debug:
		print self.who_when() + "WelcomeMessage()"
	return

    def loginPrompt(self):
	if debug:
		print self.who_when() + "loginPrompt()"
        if self.fail_count:
                self.write("Air6372SO login: ")
		# return "Air6372SO login: "
        else:
                return "Air6372SO login: "

    def telnet_User(self, user):
	# self.log(self.who_when() + "Username: " + user)
	# print self.who_when() + "Username:", user
	self.username = user
	if self.fail_count:
		self.write(IAC+WILL+ECHO+"Password: ")
		return "Password"
	else:
		self.write(IAC+WILL+ECHO+"Password: ")
		return "Password"

    def telnet_Password(self, passwd):
	# self.log(self.who_when() + "Password: " + passwd)
	# print self.who_when() + "Password:", passwd
	self.write(IAC+WONT+ECHO+"\r\n")
	self.password = passwd
	try:
		if (self.username == "root" and passwd == "dsl_2012_Air") or (self.username == "root" and passwd == "SoL_FiBeR_1357"):
			checked = 1
		else:
			checked = 0
		if not checked and self.fail_count < 2:
			self.fail_count += 1
			# self.write(IAC+WILL+ECHO+"Login incorrect\r\n")
			self.write("Login incorrect\r\n")
			# self.lineBuffer = []
			self.mode = "User"
			self.loginPrompt()
			return
	except:
		return "Done"
	if not checked:
		return "Done"
	self.loggedIn()
	return "Command"
    
    def loggedIn(self):
	self.log(self.who_when() + "Username: " + self.username)
	print self.who_when() + "Username:", self.username
	self.log(self.who_when() + "Password: " + self.password)
	print self.who_when() + "Password:", self.password
	self.log(self.who_when() + "Logged In!")
	print self.who_when() + "Logged In!"
        self.transport.write("\r\n\r\nBusyBox v1.14.1 (2011-10-25 17:21:22 EEST) built-in shell (ash)\r\nEnter 'help' for a list of built-in commands.\r\n\r\n")
	self.transport.write("# ")
    
    def telnet_Command(self, cmd):
	try:
		self.log(self.who_when() + "Command: " + cmd)
		print self.who_when() + "Command:", cmd
	except:
		pass
        result = None
	try:
		param = cmd.split(" ")
		if len(param)-1 == len(cmd):
			self.transport.write("# ")
			return
	except:
		param = 0 
	if cmd == "help" or cmd.startswith("help "):
		self.cmd_help()
        elif cmd == "exit" or cmd.startswith("exit "):
                self.cmd_exit(cmd)
        elif cmd == "wget" or cmd.startswith("wget "):
                self.cmd_wget(cmd)
	elif cmd == "":
		self.transport.write("# ")
	else:
		self.transport.write("-sh: " + cmd + ": not found" + "\r\n")
        
        if result is not None:
            self.transport.write(repr(result))
            self.transport.write('\r\n')
        self.transport.write("# ")
	return "Command"

def clear():
    if sys.platform == 'linux-i386' or sys.platform == 'linux2':
	os.system("clear")
    elif sys.platform == 'win32':
	os.system("cls")
    else:
	os.system("cls")

def main():
    factory = Factory()
    factory.protocol = lambda: Shell()
    reactor.listenTCP(2323, factory)
    reactor.run()

if __name__ == '__main__':
    clear()
    print "==========================================="
    print u"Telnet Honeypot [http://www.mertsarica.com]"
    print "==========================================="    
    main() 

