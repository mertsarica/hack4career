# JavaScript eval() Finder v1.0 
# Author: Mert SARICA 
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com
#
# Mspy data sample: H4sIAAAAAAAAAFWRQW7EIAxF78I6HZE0k6jZ9STIAae1SnAETGbSqnevUauIesHi-cP_Nl8q04pqavuxH7uh1UOjOJkdYyIOalLDRatGzZAzxsN43NGrSV9eREdBWABvMmcQ2nbjVTA-_mNdKWEH8jD74iiWulJXLcF3WshYDgFtRqemHG_YqJVn8ljzBXwqjUTJlbjtVaorZy-xSbjA51Z3gz5LGrxhhMxRmq_BRSYnMDJXXmUvnxwkzlPb91oywbaZojldHe5k0YBbKZwR03aYDzxmhujMLVUhLaziWg_6eyW9892QLev-Uz42losGbKYd6jnlX2g5TEmCobxxxn3bTMJY8iRZ4PcPA7sv8dgBAAA=
#

import base64
import zlib
import sys
import os

def decode(data):
	data = base64.b64decode(data,"-_")
	print "[*] Decoded data:", zlib.decompress(bytes(data), zlib.MAX_WBITS|16)

def cls():
	if sys.platform == 'linux-i386' or sys.platform == 'linux2':
		os.system("clear")
	elif sys.platform == 'win32':
		os.system("cls")
	else:
		os.system("cls")
		
def banner():
	cls()

	print "=============================================="
	print u"mSPY Decoder v1.0 [https://www.mertsarica.com]"
	print "=============================================="

def usage():
       print "Usage: python mspy_decoder.py <encoded data>\n"

if __name__ == '__main__':
	cls()
	banner()
        
	if len(sys.argv) < 2:
		usage()
		sys.exit(1)
	else:
		decode(sys.argv[1])