# -*- coding: utf-8 -*-
# Cryptolocker Detection & Killer Utility v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: https://www.mertsarica.com
 
import os
import binascii
import time
from winappdbg import Process, System, Debug, EventHandler
import locale
import re
import platform
import subprocess
import sys
import re
from Tkinter import *
import Tkinter
import threading
import Queue # This is thread safe
import time
from threading import *
import datetime
from winappdbg.win32 import ERROR_ACCESS_DENIED

reload(sys)
sys.setdefaultencoding('iso-8859-9')

# Global Variables
dev = 0
turkish = 0
gpid = 0
oldpid = 0
root = Tk()
fileLock = Semaphore(value=1)
filename = r"C:\Cryptokiller\log.txt"
filename_err = r"C:\Cryptokiller\error.txt"
folder = r"C:\Cryptokiller"

if dev:
    print "Platform:", platform.release()

if platform.release().find("XP") >= 0:
    xp = 1
else:
    xp = 0

def excepthook(*args):
    sys.exit(1)

# Reference: http://stackoverflow.com/questions/19672352/how-to-run-python-script-with-elevated-privilege-on-windows
def isUserAdmin():

    if os.name == 'nt':
        import ctypes
        # WARNING: requires Windows XP SP2 or higher!
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            traceback.print_exc()
    else:
        if turkish:
            raise RuntimeError, "[*] Unsupported operating system for this module: %s" % (os.name,)
        else:
            raise RuntimeError, u"[*] Desteklenmeyen işletim sistemi: %s" % (os.name,)
        sys.exit(1)
    
def log(txt):
        if not os.path.exists(folder):
            os.mkdir(folder)
            
	try:
		fileLock.acquire()
		FILE  = open (filename,"a" )
	except IOError:
		if console:
			print "[-] Can not open log.txt!\n"
		log("[-] Hata: Can not open log.txt!")
		sys.exit(1)
		
	start = str(datetime.datetime.now())
	txt = "(" + start + ")" + " " + txt + "\r\n"
	FILE.writelines(txt)
	FILE.close()
	fileLock.release()

def error_log(txt):
        try:
		fileLock.acquire()
                FILE  = open (filename_err,"a" )                                
        except IOError:
		if console:
                	print "[-] Can not open error.txt!\n"
		error_log("[-] Can not open error.txt!")
                sys.exit(1)

        start = datetime.datetime.now()
        txt = "(" + str(start) + ")" + " " + txt + "\r\n"
        FILE.writelines(txt)   
        FILE.close()
	fileLock.release()

# Reference: http://stackoverflow.com/questions/20303291/issue-with-redirecting-stdout-to-tkinter-text-widget-with-threads
class Std_redirector():
    def __init__(self, widget):
        self.widget = widget

    def write(self,string):
        self.widget.write(string)

class ThreadSafeText(Text):
    def __init__(self, master, **options):
        Text.__init__(self, master, **options)
        self.queue = Queue.Queue()
        self.update_me()

    def write(self, line):
        self.queue.put(line)

    def update_me(self):
        while not self.queue.empty():
            line = self.queue.get_nowait()
            self.insert(END, line)
            self.see(END)
            self.update_idletasks()
        self.after(10, self.update_me)
        
def get_svchost_pid():
    cmd = 'tasklist /svc /fi "imagename eq svchost.exe" /fi "services eq LanmanServer"'
    p = subprocess.Popen(cmd,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,
                     stdin=subprocess.PIPE)
    result = p.communicate()[0]
    re1='.*?'	# Non-greedy match on filler
    re2='(\\d+)'	# Integer Number 1

    rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)
    m = rg.search(result)
    if m:
        int1=m.group(1)
        return int1

def get_explorer_pid():
    # Request debug privileges.
    System.request_debug_privileges()

    # Scan for running processes.
    system = System()
    try:
        system.scan_processes()
        #system.scan_process_filenames()
    except WindowsError:
        system.scan_processes_fast()

    # For each running process...
    for process in system.iter_processes():
        try:

            pid = process.get_pid()

            if pid in (0, 4, 8):
                continue

            if dev:
                print "* Process:", process.get_filename(), "Pid:", pid, "Time:", process.get_running_time()
            if process.get_filename() == "explorer.exe":
                if process.get_running_time() < 300000:
                    return pid

        # Skip processes we don't have permission to access.
        except WindowsError, e:
            if e.winerror == ERROR_ACCESS_DENIED:
                continue
            raise

    sys.exit(1)

def cls():
    if sys.platform == 'linux-i386' or sys.platform == 'linux2':
        os.system("clear")
    elif sys.platform == 'win32':
        os.system("cls")
    else:
        os.system("cls")

def kill_cryptolocker( pname, pid ):
                
    # Instance a Process object.
    process = Process( pid )

    # Kill the process.
    process.kill()

    proc = "(" + pname + ":" + str(gpid) + ")"
    
    if turkish:
        txt = u"[*] Cryptolocker işlemcisi durduruldu! " + proc
        log(txt)
        print u"[*] Cryptolocker işlemcisi durduruldu! " + proc
    else:
        txt = "[*] Terminated Cryptolocker process! " + proc
        log(txt)
        print "[*] Terminated Cryptolocker process! " + proc

    if root.state() != "normal":
        os.system(filename)
    sys.exit(1)
    
class MyEventHandler( EventHandler ):
    global xp

    # Here we set which API calls we want to intercept
    apiHooks = {

        # Hooks for the kernel32 library
        'kernel32.dll' : [
                           #  Function            Parameters
                           ( 'CreateFileA'                      ,   7  ),
                           ( 'CreateFileW'                      ,   7  ),
                           ( 'CreateProcessA'                   ,   10  ),
                           ( 'CreateProcessW'                   ,   10  ),
                         ],
    }


    # Now we can simply define a method for each hooked API.
    # Methods beginning with "pre_" are called when entering the API,
    # and methods beginning with "post_" when returning from the API.
        
    def pre_CreateProcessA( self, event, ra, lpApplicationName, lpCommandLine, lpProcessAttributes, lpThreadAttributes,
                            bInheritHandles, dwCreationFlags, lpEnvironment, lpCurrentDirectory, lpStartupInfo,
                            lpProcessInformation):
        if dev:
            self.__print_ansi( event, "CreateProcessA", lpApplicationName )

    def pre_CreateProcessW( self, event, ra, lpApplicationName, lpCommandLine, lpProcessAttributes, lpThreadAttributes,
                            bInheritHandles, dwCreationFlags, lpEnvironment, lpCurrentDirectory, lpStartupInfo,
                            lpProcessInformation):
        if dev:
            self.__print_unicode( event, "CreateProcessW", lpApplicationName )
            
    def post_CreateProcessA( self, event, retval ):
            if dev:
                print "XP:", xp
            if xp:
                time.sleep(3)
                pid = find_hook_pid("explorer.exe")
                if pid > 0:
                    monitor("explorer.exe", pid)

    def post_CreateProcessW( self, event, retval ):
            if dev:
                print "XP:", xp
            if xp:
                time.sleep(3)
                pid = find_hook_pid()
                if pid > 0:
                    monitor("explorer.exe", pid)

    def pre_CreateFileA( self, event, ra, lpFileName, dwDesiredAccess,
             dwShareMode, lpSecurityAttributes, dwCreationDisposition,
                                dwFlagsAndAttributes, hTemplateFile ):

        if dev:
            self.__print_ansi( event, "CreateFileA", lpFileName )
                
        if int(dwCreationDisposition) == 3:

            fname = event.get_process().peek_string( lpFileName, fUnicode = False )
            if fname.lower().find("vssadmin") >= 0:
                pid = find_hook_pid("explorer.exe")
                time.sleep(3)
                if pid > 0:
                    monitor("explorer.exe", pid)
            if fname.find(".sifreli") >= 0 or fname.find(".encrypted") >=0:
                if dev:
                    if turkish:
                        print u"[*] Cryptolocker tespit edildi! ->", fname
                    else:
                        print "[*] Cryptolocker has detected! ->", fname
                    
                pid = event.get_pid()
                pname = event.get_process().get_filename()
                pname = pname.split("\\")[2]
                proc = "(" + pname + ":" + str(pid) + ")"
                
                if turkish:
                    txt = u"[*] Cryptolocker tespit edildi! " + proc
                    log(txt)
                    print u"[*] Cryptolocker tespit edildi! " + proc
                else:
                    txt = "[*] Cryptolocker has detected! " + proc
                    log(txt)
                    print "[*] Cryptolocker has detected! " + proc
                        
                kill_cryptolocker(pname, pid)

    def pre_CreateFileW( self, event, ra, lpFileName, dwDesiredAccess,
             dwShareMode, lpSecurityAttributes, dwCreationDisposition,
                                dwFlagsAndAttributes, hTemplateFile ):

        if dev:
            self.__print_unicode( event, "CreateFileA", lpFileName )


        if int(dwCreationDisposition) == 3:

            fname = event.get_process().peek_string( lpFileName, fUnicode = True )
            if fname.lower().find("vssadmin") >= 0:
                pid = find_hook_pid("explorer.exe")
                time.sleep(3)
                if pid > 0:
                    monitor("explorer.exe", pid)
            if fname.find(".sifreli") >= 0 or fname.find(".encrypted") >=0:
                if dev:
                    if turkish:
                        print u"[*] Cryptolocker tespit edildi! ->", fname
                    else:
                        print "[*] Cryptolocker has detected! ->", fname

                pid = event.get_pid()
                pname = event.get_process().get_filename()
                pname = pname.split("\\")[2]
                proc = "(" + pname + ":" + str(pid) + ")"
                
                if turkish:
                    txt = u"[*] Cryptolocker tespit edildi! " + proc
                    log(txt)
                    print u"[*] Cryptolocker tespit edildi! " + proc
                else:
                    txt = "[*] Cryptolocker has detected! " + proc
                    log(txt)
                    print "[*] Cryptolocker has detected! " + proc
                    
                kill_cryptolocker(pname, pid)
                
    # Some helper private methods...

    def __print_ansi( self, event, tag, pointer ):
        string = event.get_process().peek_string( pointer, fUnicode = False )
        tid    = event.get_tid()
        print  "%d: %s: %s" % (tid, tag, string)

    def __print_unicode( self, event, tag, pointer ):
        string = event.get_process().peek_string( pointer, fUnicode = True )
        tid    = event.get_tid()
        print  "%d: %s: %s" % (tid, tag, string)     

def find_hook_pid( procname ):
    global gpid
    global xp
    global oldpid

    s = System()
    s.request_debug_privileges()
    
    try:
        s.scan_processes()
        s.scan_process_filenames()
    except WindowsError:
        s.scan_processes_fast()
        
    pid_list = s.get_process_ids()
    pid_list.sort(reverse=True)
    
    if not pid_list:
        print "Unknown error enumerating processes!"
        # s = raw_input()
        sys.exit(1)
    
    for pid in pid_list:
        p = s.get_process(pid)
        fileName = p.get_filename()
        fname = str(fileName).lower()
        if dev:
            print "Process:", fname, "Pid:", pid
        if fname.find(procname) >= 0:
            if int(pid) != int(gpid):
                oldpid = gpid
                gpid = pid
                if procname.find("svchost.exe") >= 0:
                    gpid = int(get_svchost_pid())
                    return gpid
                elif procname.find("explorer.exe") >= 0:
                    gpid = int(get_explorer_pid())
                    return gpid
                else:
                    return pid
    return 0

def banner():
        cls()
        print "==========================================================="            
        print "Cryptokiller v1.0 [https://www.mertsarica.com/cryptokiller]"
        print "==========================================================="

def usage():
        if turkish:
            print u"Kullanım: python cryptokiller.py [hidden] \n"
        else:
            print "Usage: python cryptokiller.py [hidden]\n"

debug = Debug( MyEventHandler() )

def monitor( procname, pid ):      
    if dev:
        if turkish:
            print procname + ":" + str(pid)
        else:
            print procname + ":" + str(pid)

    # Instance a Debug object.
    if pid > 0:
        # debug = Debug( MyEventHandler() )
        try:
                debug.stop(True)
                # Attach to a running process.
                debug.attach( pid )

                # Wait for the debugee to finish.
                debug.loop()

        # Stop the debugger.
        finally:
                debug.stop()

def main():
    import sys
    global turkish
    
    try:
        if dev:
            print "Locale:", locale.getdefaultlocale()[0]
        if locale.getdefaultlocale()[0].lower() == "tr_tr":
            turkish = 0
    except:
        turkish = 0
        
    banner()

    if isUserAdmin() == 0:
        if turkish:
            print "[*] Bu aracı yönetici yetkisi (administrator) yetkisi ile çalıştırmanız gerekmektedir."
        else:
            print "[*] You must have an administrator privilege."
        sys.exit(1)
    
    if turkish:
        txt = u"[*] Cryptolocker tespit ve önleme aracı devrede..."
        log(txt)
        print u"[*] Cryptolocker tespit ve önleme aracı devrede..."
    else:
        txt = "[*] Monitoring your system against Cryptolocker..."
        log(txt)
        print "[*] Monitoring your system against Cryptolocker..."
    
    try:
        if xp:
            monitor("explorer.exe", find_hook_pid("explorer.exe"))
        else:
            monitor("svchost.exe", find_hook_pid("svchost.exe"))
    except KeyboardInterrupt:
        try:
            thread1.stop()
        except:
            pass
        debug.stop()
        sys.exit(1) 
        thread1.stop()
    
    debug.stop()
    sys.exit(1)
    
# When invoked from the command line,
# the first argument is a process ID,
# the second argument is a DLL filename.

if __name__ == "__main__":
    global thread1
    if len(sys.argv) == 2:
        if sys.argv[1].lower() == "hidden":
            root.withdraw()

    root.title("Cryptokiller - https://www.mertsarica.com/cryptokiller")

    sb = Scrollbar(root)
    sb.pack(side="right", fill="y")

    text = ThreadSafeText(root)
    text.pack()
    
    
    text['yscrollcommand'] = sb.set
    sb['command'] = text.yview


    sys.stdout = Std_redirector(text)
    sys.stderr = Std_redirector(text)
    sys.stdin = Std_redirector(text)
    sys.excepthook = excepthook

    try: 
        thread1 = threading.Thread(target=main)
        thread1.start()
        root.mainloop()
    except KeyboardInterrupt:
        thread1._Thread__stop()
        debug.stop()
        sys.exit(1)

    debug.stop()
    sys.exit(1)
