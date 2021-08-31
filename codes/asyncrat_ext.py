# -*- coding: cp1254 -*-
# AsyncRAT Configuration Extractor v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: https://www.mertsarica.com
#
# Credits: https://pastebin.com/raw/MqF9jzjd

import os
import sys
import re
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Protocol import KDF
from Crypto.Util.Padding import pad, unpad
from binascii import hexlify

showbanner = 1

salt_bytes = [0xBF, 0xEB, 0x1E, 0x56, 0xFB, 0xCD, 0x97, 0x3B, 0xB2, 0x19, 0x2, 0x24, 0x30, 0xA5, 0x78, 0x43, 0x0, 0x3D, 0x56,0x44, 0xD2, 0x1E, 0x62, 0xB9, 0xD4, 0xF1, 0x80, 0xE7, 0xE6, 0xC3, 0x39, 0x41]
salt = "".join(map(chr, salt_bytes))

key_size = 32 # 256 bits

def decrypt_string(enc, key):

	# use PBKDF2 key derivation
	# RFC 2898: https://www.ietf.org/rfc/rfc2898.txt
	key = KDF.PBKDF2(base64.b64decode(key), salt, key_size, 50000)

	# print("AES key:", hexlify(key))

	# decode cipher text and determine iv (first 16 bytes)
	enc = base64.b64decode(enc)

	# create cipher and decrypt encrypted bytes (skip first 16 bytes)
	cipher = AES.new(key, AES.MODE_CBC)
	decrypted = cipher.decrypt(enc[AES.block_size:])

	# unpad decrypted bytes
	unpadded = unpad(decrypted, AES.block_size, 'pkcs7')

	# convert bytes to UTF-8 encoded string and return
	return unpadded[32:].decode('utf-8')
	
def cls():
	if sys.platform == 'linux-i386' or sys.platform == 'linux2':
		os.system("clear")
	elif sys.platform == 'win32':
		os.system("cls")
	else:
		os.system("cls")
		
def banner():
	cls()

	print ("==================================================================")
	print (u"AsyncRAT Configuration Extractor v1.0 [https://www.mertsarica.com]")
	print ("==================================================================")

def usage():
       print ("Usage: python asyncrat_ext.py <dump file>\n")

def find_settings(data):
	regex = re.compile(r"0x288c.*?IL_0000:\s+ldstr\s\"(.*?)\".*?IL_000a:\s+ldstr\s\"(.*?)\".*?IL_0014:\s+ldstr\s\"(.*?)\".*?IL_001e:\s+ldstr\s\"(.*?)\".*?IL_0032:\s+ldstr\s\"(.*?)\".*?IL_003c:\s+ldstr\s\"(.*?)\".*?IL_0046:\s+ldstr\s\"(.*?)\".*?IL_0050:\s+ldstr\s\"(.*?)\".*?IL_005a:\s+ldstr\s\"(.*?)\".*?IL_0064:\s+ldstr\s\"(.*?)\".*?IL_006e:\s+ldstr\s\"(.*?)\".*?IL_0078:\s+ldstr\s\"(.*?)\"", re.MULTILINE|re.IGNORECASE|re.DOTALL)

	if (regex):
		matches = [m.groups() for m in regex.finditer(data)]

		for m in matches:
			ports = decrypt_string(m[0], m[5])
			print ("Port:", ports)
			hosts = decrypt_string(m[1], m[5])
			print ("Host:", hosts)
			version = decrypt_string(m[2], m[5])
			print ("Version:", version)
			install = decrypt_string(m[3], m[5])
			print ("Install:", install)
			key = m[5]
			mtx = decrypt_string(m[6], m[5])
			print ("Mutex:", mtx)
			# certificate = m[7]
			# serversignature = m[8]
			# anti = decrypt_string(m[9], m[5])
			# print ("Anti Analysis:", anti)
			pastebin = decrypt_string(m[10], m[5])
			print ("Pastebin:", pastebin)
			# bdos = decrypt_string(m[11], m[5])
			# print (bdos)
			
			
			
	
if __name__ == '__main__':
	if len(sys.argv) < 2:
		usage()
		sys.exit(1)
	else:
		if showbanner:
			cls()
			banner()			
		try:
			filename = sys.argv[1]
			FILE  = open (filename,"r" )   
			data = FILE.readlines()
			FILE.close()
			find_settings("".join(data))
			print ("\n")
		except IOError:
			print ("[+]", sys.argv[1], "file not found, terminating! \n")
			sys.exit(1)