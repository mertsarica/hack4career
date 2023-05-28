# -*- coding: cp1254 -*-
# Language Identification v1.0
# Description: Identify the language of a text
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: https://www.hack4career.com
#
# pip install fasttext
import fasttext

# pip install langid
import langid

# pip install langdetect
from langdetect import detect

import time
import os
import sys

# Debug mode 
debug = 0

def cls():
	if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
		os.system("clear")
	elif sys.platform == 'win32':
		os.system("cls")
	else:
		os.system("cls")

def banner():
	cls()

	print ("=========================================================")
	print (u"Language Identification v1.0 [https://www.hack4career.com]")
	print ("=========================================================")

def usage():
		print ("Usage: python3 lang_id.py <log file> <language code> [confidence level (low by default)]\n")

def identify_language(filename, langcode, confidence):
	selected_language = langcode

	# Suppress dummy fastText error
	try:
	    # silences warnings as the package does not properly use the python 'warnings' package
	    # see https://github.com/facebookresearch/fastText/issues/1056
	    fasttext.FastText.eprint = lambda *args,**kwargs: None
	except:
	    pass

	# wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
	lang_model = fasttext.load_model('lid.176.bin')

	try:
		with open(filename) as file:
		    for line in file:
		    	if len(line.rstrip()) <  4:
		    		continue

		    	ft_lang_code = "".join(lang_model.predict(line.rstrip())[0]).split("__")[-1]
		    	li_lang_code = langid.classify(line.rstrip())[0]
		    	try:
		    		ld_lang_code = detect(line.rstrip())
		    	except:
		    		continue

		    	if debug:
		    		print("\nText:", line.rstrip())
		    		time.sleep(1)

		    	if debug:
		    		print("Detected Language Codes:", ft_lang_code, li_lang_code, ld_lang_code)

		    	if (ft_lang_code == li_lang_code == ld_lang_code == selected_language) and confidence == "high":
		    		print("\nLanguage Code:" + selected_language.upper() + " Confidence Level:High" + " Text:" + line.rstrip())
		    		if debug:
		    			time.sleep(1)
		    	elif ((ft_lang_code == li_lang_code == selected_language) or (ft_lang_code == ld_lang_code == selected_language) or (li_lang_code == ld_lang_code == selected_language)) and confidence == "medium":
		    		print("\nLanguage Code:" + selected_language.upper() + " Confidence Level:Medium" + " Text:" + line.rstrip())
		    		if debug:
		    			time.sleep(1)
		    	elif ((ft_lang_code == selected_language) or (ld_lang_code == selected_language) or (li_lang_code == selected_language)) and confidence == "low":
		    		print("\nLanguage Code:" + selected_language.upper() + " Confidence Level:Low" + " Text:" + line.rstrip())
		    		if debug:
		    			time.sleep(1)
	except IOError:
		print ("[+]", filename, "file not found, terminating! \n")
		sys.exit(1)

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
			langcode = sys.argv[2].lower()
			if len(sys.argv) == 4:
				confidence = sys.argv[3].lower()
			else:
				confidence = "low"

			identify_language(filename, langcode, confidence)
		except KeyboardInterrupt:
			# banner()
			print ("[+] Bye...")
			sys.exit(1)	
