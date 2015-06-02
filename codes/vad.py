# -*- coding: utf-8 -*-
# vBulletin Attachment Downloader v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com
#
import os, sys, re, time
import mechanize
import urlparse
import shutil

debug = 0
signin = 0
virusscan = 0
username = ""
password = ""
url = ""
signed = 0
i = 0

mechanize.HTTPRedirectHandler.max_redirections = 100
mechanize.HTTPRedirectHandler.max_repeats = 100

def cls():
    if sys.platform == 'linux-i386' or sys.platform == 'linux2':
            os.system("clear")
    elif sys.platform == 'win32':
            os.system("cls")
    else:
            os.system("cls")

def download_attachments():
        global i
        global signed
        global signin
        
        while i >= 0: 
                b=mechanize.Browser()
                b.set_handle_robots(False)
                # b.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.11) Gecko/20100701 Firefox/3.5.11')]
                if signin and not signed:
                        login_url = url + "/search.php?do=getdaily"
                        if debug:
                                print login_url
                        b.open(login_url)
    
                        try:
                            b.select_form(nr=0)
                            b['vb_login_username'] = username
                            b['vb_login_password'] = password
                            b.submit()

                            if debug:
                                print b.geturl()
                        except:
                                pass

                        if b.response().read().find(username) < 0:
                            print "[!] Wrong username or password..."
                            sys.exit()
                        else:
                            signed = 1
                        
                attachment_url = url + "/misc.php?do=showattachments&t=" + str(i)

                print "[+] URL:", attachment_url

                line = str(i) + "|NOSCAN|NOSCAN|" + url + "\n"
                FILE = open("resume.txt", "w")
                FILE.writelines(line)
                FILE.close()
                        
                try:
                        b.open(attachment_url)
                except KeyboardInterrupt:
                        print "[+] Bye..."
                        sys.exit()
                except:
                        i = i + 1
                        download_attachments()
                    
                if debug:
                        print attachment_url
                        print b.geturl()
                                            
                for l in b.links():
                        if not l.url or not l.text:
                            continue

                        if l.text.find(".zip") < 0 and l.text.find(".exe") < 0 and l.text.find(".rar") < 0 and l.text.find(".7z") < 0:
                            continue
                        
                        if len(l.url) > 1 and l.text.find(".") > 0:
                                if l.url.find("lostpw") > 0:
                                        i = i + 1
                                        download_attachments()
                                        if debug:
                                                print l.url
                                download_url = url + "/" + l.url

                                if len(l.text) >= 85:
                                    local_file = folder + "/" + l.text[0:40] + "." + l.text.split(".")[1]
                                else:
                                    local_file = folder + "/" + l.text
                                    
                                if not os.path.isfile(local_file):
                                    if not signin and not signed:
                                        b.open(download_url)
                                        if b.response().read().find("register.php") >= 0 or b.response().read().find("vb_login_username") >= 0:
                                            print "[!] You need to specify a username and a password in order to continue..."
                                            sys.exit()
                                            
                                    if signin and not signed:
                                        b.open(download_url)
                                        b.select_form(nr=0)
                                        b['vb_login_username'] = username
                                        b['vb_login_password'] = password
                                        b.submit()

                                        if b.response().read().find(username) < 0:
                                                print "[!] Wrong username or password..."
                                                sys.exit()
                            
                                        if b.response().read().find("vb_login_username") >= 0:
                                            if not signin:
                                                print "[!] You need to specify a username and a password in order to continue..."
                                                sys.exit()
                                        else:
                                            signed = 1

                                    try:
                                        f = b.retrieve(download_url)[0]
                                    except KeyboardInterrupt:
                                        print "[+] Bye..."
                                        sys.exit()
                                    except:
                                        i = i + 1
                                        download_attachments()
                                        
                                    shutil.move(f, local_file)
                                    if len(l.text) >= 85:
                                        print "   [*] Downloaded file:", l.text[0:40] + "." + l.text.split(".")[1]
                                    else:
                                        print "   [*] Downloaded file:", l.text

                                    if virusscan:
                                            c=mechanize.Browser()
                                            c.open('http://scanner2.novirusthanks.org/')
                                            c.select_form(nr=0)
                                            if len(l.text) >= 85:
                                                c.add_file(open(local_file), "text/plain", l.text[0:40] + "." + l.text.split(".")[1])
                                            else:
                                                c.add_file(open(local_file), "text/plain", l.text)    
                                            c.submit()
                                            if debug:
                                                    print c.geturl()
                                            line = ""
                                            
                                            try:
                                                c.reload()
                                            except KeyboardInterrupt:
                                                print "[+] Bye..."
                                                sys.exit()
                                            except:
                                                pass

                                            while c.response().read().find("Scanning") >= 0:
                                                    if debug:
                                                        print c.geturl()
                                                    c.reload()

                                            if c.response().read().find("CLEAN") >= 0:
                                                    print "      [x] Sent to NoVirusThanks - Status: CLEAN"
                                                    line = str(i) + "|" + l.text + "|CLEAN|" + c.geturl() + "\n"
                                                    FILE = open("scan.txt", "a")
                                                    FILE.writelines(line)
                                                    FILE.close()
                                            if c.response().read().find("INFECTED") >= 0:
                                                    print "      [x] Sent to NoVirusThanks - Status: INFECTED"
                                                    line = str(i) + "|" + l.text + "|INFECTED|" + c.geturl() + "\n"
                                                    FILE = open("scan.txt", "a")
                                                    FILE.writelines(line)
                                                    FILE.close()
                                else:
                                    print "   [*] " + l.text + " already exists, skipping..."
                i = i + 1

    
if __name__ == '__main__':
    global folder
    count = 0
    
    cls()
    
    print "================================================================"
    print u"vBulletin Attachment Downloader v1.0 [http://www.mertsarica.com]"
    print "================================================================"

    if len(sys.argv) < 2:
        print "Usage: python vad.py [arguments]"
        print "\nRequired arguments:"
        print "-h <URL>	    Forum URL (Ex: http://www.mertsarica.com/forum)"
        print "\nOptional arguments:"
        print "-u <username>	    Username for login phase (Ex: -u mert)"
        print "-p <password> 	    Password for login phase (Ex: -p sarica)"
        print "-s 		    Send every attachment to NoVirusThanks (Ex: -s)"
        sys.exit(1)
    else:                   
        for arg in sys.argv:
                if arg == "-v":
                        print "Usage: python vad.py [arguments]"
                        print "\nRequired arguments:"
                        print "-h <URL>            Forum URL (Ex: http://www.mertsarica.com/forum)"
                        print "\nOptional arguments:"
                        print "-u <username>	    Username for login phase (Ex: -u mert)"
                        print "-p <password> 	    Password for login phase (Ex: -p sarica)"
                        print "-s 		    Send every attachment to NoVirusThanks (Ex: -s)"
                        sys.exit(1)
                elif arg == "-h":
                        if len(sys.argv) > count+1:
                            url = sys.argv[count+1]
                            if url[-1] == "/":
                                print "[!] Do not include a trailing slash at the end of the URL"
                                sys.exit()

                elif arg == "-u":
                        username = sys.argv[count+1]
                        signin = 1
                elif arg == "-p":
                        password = sys.argv[count+1]
                        signin = 1
                elif arg == "-s":
                        virusscan = 1
                count = count + 1

    if not url or not url.startswith("http"):
        print "Usage: python vad.py [arguments]"
        print "\nRequired arguments:"
        print "-h <URL>	    Forum URL (Ex: http://www.mertsarica.com/forum)"
        print "\nOptional arguments:"
        print "-u <username>	    Username for login phase (Ex: -u mert)"
        print "-p <password> 	    Password for login phase (Ex: -p sarica)"
        print "-s 		    Send every attachment to NoVirusThanks (Ex: -s)"
        sys.exit(1)
        
    folder = urlparse.urlparse(url)
    folder = folder[1]
    
    try:
        os.makedirs(folder)
    except OSError:
        pass

    if os.path.isfile("resume.txt"):
	try:
		FILE  = open ("resume.txt","r" )   
		entries = FILE.readlines()
		FILE.close()
		lastentry = entries[-1].split("|")
		if url.strip().lower() == entries[0].split("|")[-1].strip().lower():
                    i = int(lastentry[0]) + 1
                    print "[+] Resuming..."
	except IOError:
                pass
        
    try:
        download_attachments()
    except KeyboardInterrupt:	
        print "[+] Bye..."  
