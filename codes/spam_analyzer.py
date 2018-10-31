# -*- coding: utf-8 -*-
# Gmail Spam Analyzer v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: https://www.mertsarica.com
#
# Credits: https://github.com/abhishekchhibber/Gmail-Api-through-Python/blob/master/gmail_read.py , https://developers.google.com/gmail/api/quickstart/python , https://raw.githubusercontent.com/Gawen/virustotal/master/virustotal.py
#
import os
import datetime
import re
import time
import base64
import sys
import pytz
import codecs
import subprocess
import httplib
import simplejson
import urllib
import urllib2
from apiclient import errors
from apiclient import discovery
from oauth2client import file, client, tools
from pytz import timezone
from httplib2 import Http

# Global Variables
SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
debug = 0
final_list = [ ]
logfile = "logs.txt"
hashfile = "hashes.txt"
folder = "attachments"

# How many hours to sleep until re-checking
sleephour = "1"

# VX authorization header - (base64(api_key:api_secret))
vx_authorization = ""

# Fix 4 Turkish Chars
sys.stdout = codecs.getwriter("iso-8859-9")(sys.stdout, 'xmlcharrefreplace')
cmd = "chcp 1254"
subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			
def log(txt):      
    try:
            now = datetime.datetime.now()
            time = now.strftime("%d-%m-%Y %H:%M:%S")                
            file = open(logfile, "a")
            txt = str(time + " " + str(txt).encode("cp1254") + "\n")
            file.write(txt)
            file.close()
    except Exception as e:
        if debug:
            log("|log() error: " + str(e))
            pass

def log_hashes(txt):      
    try:
            now = datetime.datetime.now()
            time = now.strftime("%d-%m-%Y %H:%M:%S")                
            file = open(hashfile, "a")
            txt = str(time + "|" + str(txt).encode("cp1254") + "\n")
            file.write(txt)
            file.close()
    except Exception as e:
        if debug:
            log("|log_hashes() error: " + str(e))
            pass

def update_hashes(txt):
	try:               
			file = open(hashfile, "w")
			for line in txt:
				file.write(line)
			file.close()
	except Exception as e:
		if debug:
			log("|update_hashes() error: " + str(e))
			pass			

def get_credentials():
    global creds
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    store = file.Storage('storage.json') 
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)

def get_mail_info(m_id, user_id, temp_dict, service):
	global final_list
	msg_subject = ""
	
	message = service.users().messages().get(userId=user_id, id=m_id).execute() # fetch the message using API
	payld = message['payload'] # get payload of the message
		
	utc = pytz.utc
	utc_dt = utc.localize(datetime.datetime.utcfromtimestamp(float(message['internalDate'])/1000))
	tr_tz = timezone('Europe/Istanbul')
	tr_dt = utc_dt.astimezone(tr_tz)

	temp_dict['InternalDate'] = str(tr_dt.strftime ("%d-%m-%Y %H:%M:%S"))
	
	headr = payld['headers'] # get header of the payload

	for one in headr: # getting the Subject
		if one['name'] == 'Subject':
			msg_subject = one['value']
			temp_dict['Subject'] = msg_subject
		else:
			pass

	for three in headr: # getting the Sender
		if three['name'] == 'From':
			msg_from = three['value']
			temp_dict['Sender'] = msg_from
		else:
			pass

	temp_dict['Snippet'] = message['snippet'] # fetching message snippet
	
	if debug:
		print "Date:", str(tr_dt.strftime ("%d-%m-%Y %H:%M:%S")), "\nFrom:", unicode(msg_from), "\nSubject:", unicode(msg_subject), "\nSnippet:", unicode(message['snippet'])
	
	final_list.append(temp_dict)
	log(temp_dict)
	
	try:
		GetAttachments(service, user_id, m_id)
	except:
		pass
		
	if debug:
		print "\n"

def cls():
    if sys.platform == 'linux-i386' or sys.platform == 'linux2':
        os.system("clear")
    elif sys.platform == 'win32':
        os.system("cls")
    else:
        os.system("cls")
		
def banner():
    cls()
    print "====================================================="
    print u"Gmail Spam Analyzer v1.0 [https://www.mertsarica.com]"
    print "====================================================="

def download_attachments():
    global creds
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    get_credentials()
    service = discovery.build('gmail', 'v1', http=creds.authorize(Http()))
	
    user_id =  'me'
    label_id_one = 'SPAM'
    label_id_two = 'UNREAD'

    unread_msgs = service.users().messages().list(userId='me',labelIds=[label_id_one, label_id_two]).execute()

    try:
        mssg_list = unread_msgs['messages']
    except:
        print "[*] All e-emails are already analyzed in Spam folder..."
        return
		
    print "[*] Total unread messages in spam folder: ", str(len(mssg_list))
    if debug:
        print "\n"

    for mssg in mssg_list:
		temp_dict = { }
		m_id = mssg['id'] # get id of individual message
		get_mail_info(m_id, user_id, temp_dict, service)
		message = service.users().messages().get(userId=user_id, format='raw', id=m_id).execute() # fetch the message using API
		msg_str = base64.urlsafe_b64decode(message['raw'].encode('utf-8'))	
		service.users().messages().modify(userId=user_id, id=m_id,body={ 'removeLabelIds': ['UNREAD']}).execute()
		
def GetAttachments(service, user_id, msg_id, prefix=""):
	global	attcount
	data = ""
	
	if not os.path.exists(folder):
		os.mkdir(folder)
	
	try:
			message = service.users().messages().get(userId=user_id, id=msg_id).execute()

			for part in message['payload'].get('parts', ''):
				if part['filename']:
					if 'data' in part['body']:
						data=part['body']['data']
					else:
						att_id=part['body']['attachmentId']
						att=service.users().messages().attachments().get(userId=user_id, messageId=msg_id,id=att_id).execute()
						data=att['data']
			if data:
				file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
				path = prefix+part['filename'].encode('UTF-8')

				with open(folder + "/" + path, 'wb') as f:
					f.write(file_data)
				if debug:
					print "Attachment:", path
				file_to_send = open(folder + "/" + path, "rb").read()
				vx_submit_file(path, file_to_send)

			else:
				att_id=message['payload']['body']['attachmentId']
				att=service.users().messages().attachments().get(userId=user_id, messageId=msg_id,id=att_id).execute()
				data=att['data']
				if data:
					file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
					
					re1='(filename=")'	# Word 1
					re2='(.*?)'	# Any Single Character 1
					re3='(")'	# Any Single Character 2
					re4='(.*?)'	# Any Single Character 1
					re5='(----)'	# Any Single Character 2
					
					rg = re.compile(re1+re2+re3+re4+re5,re.IGNORECASE|re.DOTALL)
					m = rg.search(file_data)
					if m:
						word1=m.group(1)
						path=m.group(2).encode('UTF-8')
						var1=m.group(3)
						var2=m.group(4)						
						var3=m.group(5)
						decoded_file_data = base64.urlsafe_b64decode(var2.encode('UTF-8'))

						with open(folder + "/" + path, 'wb') as f:
							f.write(decoded_file_data)
						if debug:
							print "Attachment:", path
						file_to_send = open(folder + "/" + path, "rb").read()
						vx_submit_file(path, file_to_send)

	except errors.HttpError as error:
		print('An error occurred: %s' % error)

def post_multipart(host, selector, fields, files):
	content_type, body = encode_multipart_formdata(fields, files)
	h = httplib.HTTPS(host)
	h.putrequest('POST', selector)
	h.putheader('Host', 'www.hybrid-analysis.com')
	h.putheader('User-agent', "VxApi CLI Connector")
	h.putheader('Authorization', "Basic " + vx_authorization)
	h.putheader('content-type', content_type)
	h.putheader('content-length', str(len(body)))
	h.endheaders()
	h.send(body)
	errcode, errmsg, headers = h.getreply()

	return h.file.read()
		
def encode_multipart_formdata(fields, files):
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
		L.append('')
		L.append(value)
	L.append('--' + BOUNDARY + '--')
	L.append('')
	body = CRLF.join((bytes(i) for i in L))
	content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
	
	return content_type, body

def vx_check_report(line):
	re1='(.*?)'
	re2='(\\|)'	# DDMMYYYY 1
	re3='(.*?)'	# Variable Name 1
	re4='(\\|)'	# Any Single Character 2
	re5='(.*?)'	# Alphanum 1
	re6='(\\|)'	# Any Single Character 3
	re7='(submitted)'	# Word 1

	rg = re.compile(re1+re2+re3+re4+re5+re6,re.IGNORECASE|re.DOTALL)
	m = rg.search(line.strip())

	if m:
		fname = m.group(3)
		alphanum=m.group(5)
		# Malicious file hash for debugging purposes
		# alphanum = "040c0111aef474d8b7bfa9a7caa0e06b4f1049c7ae8c66611a53fc2599f0b90f"
		host = "www.hybrid-analysis.com"
		selector = "https://wwww.hybrid-analysis.com/api/summary/" + alphanum + "?environmentId=100"
		h = httplib.HTTPS(host)
		h.putrequest('GET', selector)
		h.putheader('Host', 'www.hybrid-analysis.com')
		h.putheader('User-agent', "VxApi CLI Connector")
		h.putheader('Authorization', "Basic " + vx_authorization)
		h.endheaders()

		h.send("")
		errcode, errmsg, headers = h.getreply()

		response = h.file.read()
		
		response_dict = simplejson.loads(response)
		vx_status = str(response_dict.get('response').get('verdict'))
		if vx_status == "None":
			vx_status = "https://www.hybrid-analysis.com/sample/" + alphanum + "?environmentId=100|clean"
		else:
			print "[*] Verdict of", fname + ":", vx_status
			vx_status = "https://www.hybrid-analysis.com/sample/" + alphanum + "?environmentId=100|" + vx_status
		return vx_status
	
def vx_check_hash():
	hashes = []
	try:
		filename = "hashes.txt"
		FILE  = open (filename,"r" )   
		lines = FILE.readlines()
		FILE.close()	
	except IOError:
		print "[+] hashes.txt file not found! \n"
		return
	
	for line in lines:
		if line.find("submitted") >= 0:
			line = line.replace("submitted", vx_check_report(line.strip()))
		hashes.append(line)
		
	update_hashes(hashes)
			
def vx_submit_file(fname, file_to_send):
	host = "www.hybrid-analysis.com"
	selector = "https://www.hybrid-analysis.com/api/submit"
	fields = [("environmentId", "100"), ("nosharevt", "1")]
	files = [("file", fname, file_to_send)]
	print "[*] Submitting", fname, "to Falcon Sandbox"
	json = post_multipart(host, selector, fields, files)
	response_dict = simplejson.loads(json)
	vx_hash = str(response_dict.get('response').get('sha256'))
	log_hashes(fname + "|" + vx_hash + "|" + "submitted")

def main():
    while (1==1):
        try:
            banner()
            print "[+] Working on attachments..."
            download_attachments()
            print "[+] Checking for malicious samples..."
            vx_check_hash()
            print "[+] Sleeping %s hour..." % (sleephour)
            time.sleep(int(sleephour)*60*60)
        except KeyboardInterrupt:
             # banner()
             print "[+] Bye..."
             sys.exit(1)
        except Exception as e:
             print "[+] Error: ", str(e)
             log("|log() error: " + str(e))
	     sys.exit(1)
		 
if __name__ == '__main__':
    main()
