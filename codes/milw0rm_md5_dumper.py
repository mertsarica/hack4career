import urllib2
import re
import time
import os

counter = 88380
m = 0

FILE = open("md5.txt","w")

os.system("cls")
print "       http://www.mertsarica.com          "
print "=========================================="
print "Milw0rm MD5 Hash Dumper v1.0 (M.S Edition)"
print "=========================================="
print "[+] Dumping md5 hashes...\n"
while counter > 0:
    url = "http://www.milw0rm.com/cracker/list.php?start=" + str(counter)
    response = urllib2.urlopen(url)
    html = response.read()
    md5 = re.findall(r"([a-fA-F\d]{32})<", html)

    i = 0
    
    while i < len(md5):
        re1=md5[i]	# Md5 hash
        re2='(<[^>]+>)'	# Tag 2
        re3='(<[^>]+>)'	# Tag 3
        re4='(<TD nowrap="nowrap" width=150>)'	# Tag 4
        re5='(<div align="center">)'	# Tag 5
        re6='((?:[a-z0-9_#!\'^\+%&/()=\?\-_]*))'
        re7='.*?'	# Non-greedy match on filler
        re8='(cracked)'	# Word 2
        re9='.*?'	# Non-greedy match on filler
        re10='((?:2|1)\\d{3}(?:-|\\/)(?:(?:0[1-9])|(?:1[0-2]))(?:-|\\/)(?:(?:0[1-9])|(?:[1-2][0-9])|(?:3[0-1]))(?:T|\\s)(?:(?:[0-1][0-9])|(?:2[0-3])):(?:[0-5][0-9]):(?:[0-5][0-9]))'	# Time Stamp 1
        re11='.*?'
        rg = re.compile(re1+re2+re3+re4+re5+re6+re7+re8+re9+re10+re11,re.IGNORECASE|re.DOTALL)
        m = rg.search(html)
        if m:
            word1=m.group(1)
            word2=m.group(2)
            word3=m.group(3)
            word4=m.group(4)
            word5=m.group(5)
            word6=m.group(6)
            word7=m.group(7)
            hs = md5[i] + " " + word5 + " " + word6 + " " + word7 + " " + "\n"
            print md5[i] + " " + word5 + " " + word6 + " " + word7 + " "
            FILE.write(hs)
        i = i + 1
    counter = counter - 30
    FILE.flush()
    time.sleep(1)
FILE.close()
