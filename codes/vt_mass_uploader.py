# -*- coding: utf-8 -*-
# VirusTotal Mass Uploader v1.0
# Description: You should copy all malicious files to malwares folder and then run this program. It will submit/resubmit all files to VirusTotal and write report url to vt_report.txt
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com

import os
import time
import locale
import httplib, mimetypes
import urllib
import urllib2
import simplejson
import sys
import hashlib
import datetime

debug = 0
# Define your VirusTotal API key!
vt_api_key = ""

reportfile = "vt_report.txt"

def report(fname, sha256, txt):
    now = datetime.datetime.now()
    time = now.strftime("%d-%m-%Y %H:%M")
    file = open(reportfile, "a")
    txt = str(time + "|" + fname + "|" + txt.encode("cp1254") + "|" + sha256 + "\n")
    file.write(txt)
    file.close()
	
def cls():
	if sys.platform == 'linux-i386' or sys.platform == 'linux2':
		os.system("clear")
	elif sys.platform == 'win32':
		os.system("cls")
	else:
		os.system("cls")

# Reference: https://raw.githubusercontent.com/Gawen/virustotal/master/virustotal.py
def post_multipart(host, selector, fields, files):
	"""
	Post fields and files to an http host as multipart/form-data.
	fields is a sequence of (name, value) elements for regular form fields.
	files is a sequence of (name, filename, value) elements for data to be uploaded as files
	Return the server's response page.
	Reference: https://raw.githubusercontent.com/Gawen/virustotal/master/virustotal.py
	"""
	content_type, body = encode_multipart_formdata(fields, files)
	h = httplib.HTTPS(host)
	h.putrequest('POST', selector)
	h.putheader('content-type', content_type)
	h.putheader('content-length', str(len(body)))
	h.endheaders()
	h.send(body)
	errcode, errmsg, headers = h.getreply()

	return h.file.read()

# Reference: https://raw.githubusercontent.com/Gawen/virustotal/master/virustotal.py
def encode_multipart_formdata(fields, files):
	"""
	fields is a sequence of (name, value) elements for regular form fields.
	files is a sequence of (name, filename, value) elements for data to be uploaded as files
	Return (content_type, body) ready for httplib.HTTP instance
	"""
	BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
	CRLF = '\r\n'
	L = []
	for (key, value) in fields:
		L.append('--' + BOUNDARY)
		L.append('Content-Disposition: form-data; name="%s"' % key)
		L.append('')
		L.append(value)
	for (key, filename, value) in files:
		L.append('--' + BOUNDARY)
		L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
		L.append('Content-Type: %s' % get_content_type(filename))
		L.append('')
		L.append(value)
	L.append('--' + BOUNDARY + '--')
	L.append('')
	body = CRLF.join((bytes(i) for i in L))
	content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
	
	return content_type, body

# Reference: https://raw.githubusercontent.com/Gawen/virustotal/master/virustotal.py
def get_content_type(filename):
	return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

def get_sha256(fname):
	return hashlib.sha256(open(fname,'rb').read()).hexdigest()
	
def banner():
	cls()
	print "========================================================="
	print u"VirusTotal Mass Uploader v1.0 [http://www.mertsarica.com]"
	print "========================================================="	

def usage():
	print "Usage: You should copy all malicious files to malwares folder and then run this program. It will submit or resubmit all files to VirusTotal\n"
	
def vt_submit_file(fname, file_to_send):
	host = "www.virustotal.com"
	selector = "https://www.virustotal.com/vtapi/v2/file/scan"
	fields = [("apikey", vt_api_key)]
	files = [("file", fname, file_to_send)]
	print "[*] Submitting", fname, "to VirusTotal"
	json = post_multipart(host, selector, fields, files)
	if debug:
		print "Response:", json
	response_dict = simplejson.loads(json)
	permalink = str(response_dict.get('permalink'))
	report(file, sha256, permalink)
	if debug:
		print "Permalink:", permalink

def vt_check_file(file, file_to_send, sha256):
	url = "https://www.virustotal.com/vtapi/v2/file/rescan"
	parameters = {"resource": sha256,
				"apikey": vt_api_key}
	data = urllib.urlencode(parameters)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	json = response.read()
	if debug:
		print "Response:", json
	response_dict = simplejson.loads(json)
	if int(response_dict.get('response_code')) == 0:
		vt_submit_file(file, file_to_send)
	else:
		permalink = str(response_dict.get('permalink'))
		report(file, sha256, permalink)
		if debug:
			print "[*] Resubmitted", file, "to VirusTotal", "(" + str(response_dict.get('permalink')) + ")"
		else:
			print "[*] Resubmitted", file, "to VirusTotal"

def main():
	dir = os.getcwd() + "/malwares/"
	files = [ f for f in os.listdir(dir) if os.path.isfile(dir+f) ]
	for file in files:
		sha256 = get_sha256(dir+file)
		file_to_send = open(dir+file, "rb").read()
		vt_check_file(file, file_to_send, sha256)
		time.sleep(15)
		
if __name__ == "__main__":
	banner()
	if vt_api_key is "":
		print "You should edit this file and define your VirusTotal API key!"
		sys.exit(1)
	main()
	print "[*] Now, wait 30 minutes and then run vt_reporter.py"
	sys.exit(1)
	
	