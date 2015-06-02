# Hesperbot E-mail Decoder v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com
import os, re, sys
import binascii

# 00401EC5  |> 8A4C30 FF      /MOV CL,BYTE PTR DS:[EAX+ESI-1]
# 00401EC9  |. 300C30         |XOR BYTE PTR DS:[EAX+ESI],CL
# 00401ECC  |. 40             |INC EAX
# 00401ECD  |. 3BC7           |CMP EAX,EDI
# 00401ECF  |.^72 F4          \JB SHORT _014E000.00401EC5

def xor(data):
		data = binascii.unhexlify(data)
		decryptedData = ""
		m = 0
		for i in data:
			if m == len(data)-1:
				break
			if m == 0:
				decryptedData = i
			else:
				decryptedData = decryptedData + (chr(ord(i) ^ ord(data[m+1])))
			m = m + 1
		decryptedData = binascii.hexlify(decryptedData).replace("00", "")
		return binascii.unhexlify(decryptedData)

if __name__ == '__main__':
        if sys.platform == 'linux-i386' or sys.platform == 'linux2':
                os.system("clear")
        elif sys.platform == 'win32':
                os.system("cls")
        else:
                os.system("cls")
        
	print "===================================================="
	print u"Hesperbot E-mail Decoder [http://www.mertsarica.com]"
	print "===================================================="
	if len(sys.argv) < 2:
		print "Usage: python hesperbot_email_decoder.py [encoded data file]\n"
		sys.exit(1)

	try:
				cfile = sys.argv[1]

				m = open(cfile, "rb")
				data = m.read()
				m.close()
				print xor(data)
				
	except KeyboardInterrupt:	
				print "[+] Bye..."
