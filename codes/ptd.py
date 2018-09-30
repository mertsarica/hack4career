# Phishing Tweet Detector v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: https://www.mertsarica.com

import tweepy
import datetime
from pprint import pprint
import urllib, urllib2, urlparse
import time
import datetime
import sys
import os
import socket
import hashlib
import datetime
from PIL import Image
import pytesseract
import cv2
import smtplib
from email.MIMEText import MIMEText

# Global Variables
default_timeout = 120
socket.setdefaulttimeout(default_timeout)
imgpath = "images/"
title = "Phishing Tweet Detected!"
mailto = ""
GMAIL_LOGIN = ''
GMAIL_PASSWORD = ''
debug = 0
waittime = 60*60*1
keywords = ["bankasi"]

reload(sys)
sys.setdefaultencoding('iso-8859-9')


consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def send_email(subject, message, from_addr=GMAIL_LOGIN, to_addr=mailto):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.ehlo()
    server.login(GMAIL_LOGIN,GMAIL_PASSWORD)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.close()

def log(md5, imgurl):
    entries = ""
    try:
            FILE  = open ("download_log.txt","r" )
            entries = FILE.readlines()
            entries = "".join(entries)
            FILE.close()
    except IOError:
            pass
            # print "[+] download_log.txt file not found but do not worry I will create it right now :)\n"
            # time.sleep(3)

    if entries.find(imgurl) < 0:
	# print imgurl
	txt = " " + imgurl
    	now = datetime.datetime.now()
    	time = now.strftime("%d-%m-%Y %H:%M:%S")
    	file = open("download_log.txt", "a")
    	txt = str(time + " " + txt.encode("cp1254") + "\n")
    	file.write(txt)
    	file.close()

def ocr(imgfile):
    print "[+] Running OCR on:", imgfile
    text = pytesseract.image_to_string(Image.open(imgpath + imgfile))
    if debug:
       print "----------------------------"
       print "OCR Message:", text
       print "----------------------------"

    if text.find("YUKARIDAK") >= 0 or text.find("SANSLI KISI") >= 0 or text.find("SANSLI KiSi") >= 0 or text.find("KATILIM YAPAN") >= 0:
        # print "[!] Phishing tweet detected!\n"
	return 1
    else:
	# print imgpath + imgfile
	os.remove(imgpath + imgfile)
	return 0


def get_md5(imgfile):
	BLOCKSIZE = 65536
	hasher = hashlib.md5()
	with open(imgfile, 'rb') as afile:
    		buf = afile.read(BLOCKSIZE)
    		while len(buf) > 0:
        		hasher.update(buf)
        		buf = afile.read(BLOCKSIZE)
	return hasher.hexdigest()

def download_image(imgurl, imgfile):
    # print "[+] Downloading image..."
    entries = ""
    try:
            FILE  = open ("download_log.txt", "r")
            entries = FILE.readlines()
            entries = "".join(entries)
            FILE.close()
    except IOError:              
            pass       
            # print "[+] download_log.txt file not found but do not worry I will create it right now :)\n"
            # time.sleep(3)

    if entries.find(imgurl) < 0:
        print "[+] Downloading image:", imgurl
	dir = os.path.dirname(imgpath)

	try:
    		os.stat(dir)
	except:
    		os.makedirs(dir)

	try:
		f = urllib2.urlopen(imgurl)
		imgfile = imgpath + imgfile
		with open(imgfile, "wb") as code:
			code.write(f.read())
		return get_md5(imgfile)
	except:
		return 0
#    else:
#	print "Skipping:", imgurl

def banner():
    if sys.platform == 'linux-i386' or sys.platform == 'linux2':
            os.system("clear")
    elif sys.platform == 'win32':
            os.system("cls")    
    else:
            os.system("cls")

    print "===================================================="
    print "Phishing Tweet Detector [https://www.mertsarica.com]"
    print "===================================================="


def check_tweets():
        for keyword in keywords:
            print "[+] Checking tweets for keyword:", keyword
	    for tweet in tweepy.Cursor(api.search, q=keyword, count=10,result_type="recent", until=datetime.datetime.today().strftime('%Y-%m-%d'), include_entities=True, lang="tr").items():

                try:
                        if tweet._json["entities"]["media"][0]["media_url"]:
                                # print "Screen Name:", tweet._json["user"]["screen_name"], "Name:", tweet._json["user"]["name"], "Media URL:", tweet._json["entities"]["media"][0]["media_url"], "Tweet URL:", tweet._json["entities"]["media"][0]["url"], "\n"
                                imgurl = tweet._json["entities"]["media"][0]["media_url"].strip()
                                imgfile = imgurl.rsplit("/",1)[1]
                        	try:          
                	              md5 = download_image(imgurl, imgfile)
                                      # print md5
            	                except Exception,e:
                	              # print str(e)
                	              pass
            	                time.sleep(1)
            	                if md5:            
                	            msg = imgurl
                	            log(md5, imgurl)
                                    if ocr(imgfile):
                                       print "\n[!] Phishing tweet detected! -> Screen Name:", tweet._json["user"]["screen_name"], "Name:", tweet._json["user"]["name"], "Media URL:", tweet._json["entities"]["media"][0]["media_url"], "Tweet URL:", tweet._json["entities"]["media"][0]["url"], "\n"
                                       msg = title + "\n" + "Screen Name:", tweet._json["user"]["screen_name"] + "\n" + "Tweet URL:", tweet._json["entities"]["media"][0]["url"] + "\n"
        			       # print msg
                                       send_email(title, ''.join(msg))

                except Exception,e:
                        # print str(e)
                        pass

if __name__ == '__main__':
    banner()
    try:
        while(1):
	    try:
		    # print "[+] Checking tweets"
		    if debug:
			print "check_tweets()"
                    check_tweets()
            except Exception,e: 
		    # print str(e)
            	    pass
	    print "Sleeping for", waittime/60/60, "hour" 
            time.sleep(waittime)
    except KeyboardInterrupt:	
        print "[+] Bye..."
