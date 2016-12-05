# Polgov Decryptor v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com

import base64
from binascii import *
from struct import *
import wincrypto
import sys
import os

CALG_RC4 = 0x6801
CALG_MD5 = 0x8003

def banner():
        cls()

        print "=================================================="
        print u"Polgov Decryptor v1.0 [https://www.mertsarica.com]"
        print "=================================================="

def cls():
	if sys.platform == 'linux-i386' or sys.platform == 'linux2':
		os.system("clear")
	elif sys.platform == 'win32':
		os.system("cls")
	else:
		os.system("cls")

def usage():
       print "Usage: python polgov_decryptor.py <RC4(base64(encrypted string))>\n"

def decrypt(data):
	md5_hasher = wincrypto.CryptCreateHash(CALG_MD5)
	wincrypto.CryptHashData(md5_hasher, 'WePWNhouses12345')
	generated_key = wincrypto.CryptDeriveKey(md5_hasher, CALG_RC4)
	decrypted_data = wincrypto.CryptDecrypt(generated_key, data)
	return decrypted_data

# encdata = "Xse6YMBpp41xbkuGWhbHl151RryXs7GYOzvoaBfRvyUNKJpBQpNg8Fr9ACEp+mekjx+JkZcb40yNxAKh+r/pFduZsviHQq2g3RWyfz1Kqd731PbPxWv1oSdyei4a7XgeejFn/eglHorsho+DaCsyX5Y48rfXDWF0tn9LZqVCTPnpBERy0a1R5l7DtscVw0o0Oy0VXRHjWM/v3PxEat96QiBcruyK7vXkmsr20elGpP6opBzzhOBrk5FRqgr3KfhPidqnuUpRYZjrfs7lQV0no+HtNavevzhjhDFz8Q1reaa6C54aJXCpqEKFkhc6bQcgcDnh4TAB7KUEGSefO9pc0/KcSqner6mkharZTJ1ITK9Xo7mEVAByL32Q5ypCE3hAoZwHEdLyJy8aarneA40BNASya3KC1d3rCJOApKZAPbj8Tvzn3zBeTrQHqnvbz4wcjLGg/l5rkGJwtB/A5nfBJwwsBgyd1+p4qyMeRV9SnoJ9H+ZtMI8VA5oqNQqllVjC0QlPIMpm0FyG/8iMzQz9KlMzA/wnel/2BbKp0HJB1jHuVmFkb/SWQLhbyGg0hD1RqTCg9GhrgqeQGgIGrDA="

if __name__ == '__main__':
	cls()
	banner()
	if len(sys.argv) < 2:
		usage()
		sys.exit(1)
	else:
		print "[*] Encrypted data:", sys.argv[1]
		decdata = decrypt(base64.b64decode(sys.argv[1]))
		print "\n[*] Decrypted data:", decdata
