# -*- coding: cp1254 -*-
# Cam2Jpg v1.0
# Description: Extract frames from video files for OCR
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: https://www.mertsarica.com
#
import cv2 
import os 
import sys

def cls():
	if sys.platform == 'linux-i386' or sys.platform == 'linux2':
		os.system("clear")
	elif sys.platform == 'win32':
		os.system("cls")
	else:
		os.system("cls")
		
def banner():
	cls()

	print ("=========================================")
	print (u"cam2jpg v1.0 [https://www.mertsarica.com]")
	print ("=========================================")

def usage():
       print ("Usage: python cam2jpg.py <video file> <output folder> [frame number]\n")

if __name__ == '__main__':
	if len(sys.argv) < 3:
		cls()
		banner()
		usage()
		sys.exit(1)
	else:
		cls()
		banner()
		try:
			filename = sys.argv[1]
			cam = cv2.VideoCapture(filename)
			path = sys.argv[2]
			try:
				if not os.path.exists(path): 
					os.makedirs(path)
			except:
				print ("[+]", "Can not create directory, terminating! \n")
				sys.exit(1)
			if len(sys.argv) == 4:
				currentframe = int(sys.argv[3])
				cam.set(cv2.CAP_PROP_POS_FRAMES, currentframe)
			else:
				currentframe = 0

			while(True): 
				
				ret,frame = cam.read() 

				if ret:  
					name = path + "\\" + str(currentframe) + ".jpg"
					print ("[*]", "Creating frame", name)
					cv2.imwrite(name, frame) 
					currentframe += 1
				else: 
					break

			cam.release() 
			cv2.destroyAllWindows()
		except KeyboardInterrupt:
			# banner()
			print ("[+] Bye...")
			sys.exit(1)	
		except IOError:
			print ("[+]", sys.argv[1], "file not found, terminating! \n")
			sys.exit(1)
		
