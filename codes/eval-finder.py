# JavaScript eval() Finder v1.0 
# Author: Mert SARICA 
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com
#
# Reference: http://bt3gl.github.io/black-hat-python-infinite-possibilities-with-the-scapy-module.html
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
from scapy.error import Scapy_Exception
import os
import sys
import threading
import signal
import zlib
# from time import time
import time
import subprocess

debug = 0
JS_DIR = "javascripts"

def find_html(headers, http_payload):
    html = None
    try:
        if 'html' in headers['Content-Type']:
            html = http_payload[http_payload.index('\r\n\r\n')+4:]
            try:
                if 'Content-Encoding' in headers.keys():
                    if headers['Content-Encoding'] == 'gzip':
                        html = zlib.decompress(image, 16+zlb.MAX_WBITS)
                    elif headers['Content-Encoding'] == 'deflate':
                        html = zlib.decompress(image)
            except:
                pass
        if 'javascript' in headers['Content-Type']:
            html = http_payload[http_payload.index('\r\n\r\n')+4:]
            try:
                if 'Content-Encoding' in headers.keys():
                    if headers['Content-Encoding'] == 'gzip':
                        html = zlib.decompress(image, 16+zlb.MAX_WBITS)
                    elif headers['Content-Encoding'] == 'deflate':
                        html = zlib.decompress(image)
            except:
                pass
    except:
        return None
    return html

def find_js(fileName):
	js = 0
        html = fileName
        regex = re.compile(r"(<script>)(.*?)(</script>)", re.MULTILINE|re.IGNORECASE|re.DOTALL)

        if (regex):
                matches = [m.groups() for m in regex.finditer(html)]

                for m in matches:
			if debug:
				print m[1]
			js = 1
	if js:
		return 1
	else:
		return 0

def find_eval(fileName):
	cmd = "phantomjs js-extractor.js " + JS_DIR + "/" + fileName
	if debug:
		print "Cmd:", cmd
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        line = p.stdout.readline().strip()
	if debug:
		print "Line:", line
	if line.find("Detected") >= 0:
		print "\n[*] Suspicious file:", fileName
		print line
	if line.find("js-extractor.js") >= 0:
		print "[*] Can not find js-extractor.js"
		sys.exit(1)

def find_html_files():
	list = os.listdir(JS_DIR)

	if debug:
		print "Dir:", list
	for file_name in list: 
		html = file_name.find('.html')
		if html >= 0:
			if debug:
				print "Filename:", file_name
			find_eval(file_name)

def http_assembler(PCAP):
    print "[*] Loading PCAP file..."
    p = rdpcap(PCAP)
    print "[*] Loading sessions..."
    sessions = p.sessions()
    for session in sessions:
        http_payload = ''
        for packet in sessions[session]:
            try:
                if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                    http_payload += str(packet[TCP].payload)
            except:
                pass

        headers = get_http_headers(http_payload)

        if headers is None:
		continue

	html = find_html(headers, http_payload)

	if html is not None:
		js = find_js(http_payload)
		
		if js:
		 	print "[*] JavaScript detected"
			t = time.time()
			try:
    				os.makedirs(JS_DIR)
			except OSError:
   				if os.path.exists(JS_DIR):
        				pass
    				else:
        				raise
			print "[*] Writing html file %s-%d.html to %s folder" %(PCAP, t, JS_DIR)
			file_name = '%s-%d.html' %(PCAP, t)
			fd = open('%s/%s' % (JS_DIR, file_name), 'wb')
			fd.write(html)
			fd.close()
			time.sleep(1)
    return

def get_http_headers(http_payload):
    try:
        headers_raw = http_payload[:http_payload.index("\r\n\r\n")+2]
        headers = dict(re.findall(r'(?P<name>.*?):(?P<value>.*?)\r\n', headers_raw))
    except:
        return None

    if 'Content-Type' not in headers:
        return None

    return headers

def banner():
        if sys.platform == 'linux-i386' or sys.platform == 'linux2':
                os.system("clear")
        elif sys.platform == 'win32':
                os.system("cls")
        else:
                os.system("cls")

        print "======================================================="
        print u"JavaScript Eval Finder v1.0 [http://www.mertsarica.com]"
        print "======================================================="

def usage():
        print "Usage: python eval-finder.py <PCAP file>\n"

if __name__ == '__main__':
        if sys.platform == 'linux-i386' or sys.platform == 'linux2':
                os.system("clear")
        elif sys.platform == 'win32':
                os.system("cls")
        else:
                os.system("cls")

	banner()
        
	if len(sys.argv) < 2:
		usage()
		sys.exit(1)
	else:
		http_assembler(sys.argv[1])
		find_html_files()
