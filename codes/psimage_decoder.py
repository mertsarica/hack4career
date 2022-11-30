# -*- coding: cp1254 -*-
# PSImage Decoder v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: https://www.mertsarica.com
import PIL
from PIL import Image
import sys
import math
import re
import os

def cls():
	if sys.platform == 'linux-i386' or sys.platform == 'linux2':
		os.system("clear")
	elif sys.platform == 'win32':
		os.system("cls")
	else:
		os.system("cls")

def banner():
	cls()

	print ("=================================================")
	print (u"PSImage Decoder v1.0 [https://www.mertsarica.com]")
	print ("=================================================")


def usage():
       print ("Usage: python psimage_decoder.py <PNG file>\n")

       
def decode(fname):
    im=Image.open(fname).convert('RGB')
    pix=im.load()
    w=im.size[0]
    h=im.size[1]
    m = []
    o = 0
    z = 0
    payload = ""

    for i in range(h):
      for j in range(w):
        r, g, b = pix[j, i]
        o = ((math.floor(b & 15)*16)|(g&15))
        m.append(o)

    payload = ''.join(chr(i) for i in m)
    payload = ("".join(payload))

    pay = re.split(r'\n\}\n', payload)
    pay = list(pay)

    while z < len(pay):
        pay[z] = pay[z] + "\n}\n"
        z = z + 1
    pay.pop()
    pay = "".join(pay)
    print (pay)


def main():
    if len(sys.argv) < 2:
        banner()
        usage()
        sys.exit(1)
    else:
        try:
            banner()
            if sys.argv[1].find(".png") > 0:
                print ("[*] Decoding payload...")
                decode(sys.argv[1])
                sys.exit(1)
            else:
               print ("[-] Error, target must be a PNG file") 
        except IOError:
            print ("[-]", sys.argv[1], "file not found, terminating! \n")
            sys.exit(1)
        except KeyboardInterrupt:
            # banner()
            print ("[+] Bye...")
            sys.exit(1)

		 
if __name__ == '__main__':
    main()
