# Paypass Credit Card Reader v1.0
# Author: Mert SARICA
# E-mail: mert [ . ] sarica [ @ ] gmail [ . ] com
# URL: http://www.mertsarica.com
# Test Device: Omnikey CardMan 5321

# This is a modified ChAP.py from RFIDIOt (http://rfidiot.org/ChAP.py)
# and ChasePayPassBlink.py from Brad Antoniewicz (http://nosedookie.blogspot.com)
# Original Copyright 2008 RFIDIOt
# Author: Adam Laurie, mailto:adam@algroup.co.uk (http://rfidiot.org/ChAP.py)

from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.CardConnection import CardConnection
from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.Exceptions import CardRequestTimeoutException

import os
import getopt
import sys
import string
import binascii
from operator import *

# default global options
Protocol= CardConnection.T0_protocol
Verbose= False

# AIDs
# 'VISA' -> [0xa0,0x00,0x00,0x00,0x03]
# 'VISA Debit/Credit' -> [0xa0,0x00,0x00,0x00,0x03,0x10,0x10]
# 'VISA Credit' -> [0xa0,0x00,0x00,0x00,0x03,0x10,0x10,0x01]
# 'VISA Debit' -> [0xa0,0x00,0x00,0x00,0x03,0x10,0x10,0x02]
# 'VISA Electron' -> [0xa0,0x00,0x00,0x00,0x03,0x20,0x10]
# 'VISA Interlink' -> [0xa0,0x00,0x00,0x00,0x03,0x30,0x10]
# 'VISA Plus' -> [0xa0,0x00,0x00,0x00,0x03,0x80,0x10]
# 'VISA ATM' -> [0xa0,0x00,0x00,0x00,0x03,0x99,0x99,0x10]
# 'MASTERCARD',0xa0,0x00,0x00,0x00,0x04,0x10,0x10]
# 'Maestro' -> [0xa0,0x00,0x00,0x00,0x04,0x30,0x60]
# 'Maestro UK' -> [0xa0,0x00,0x00,0x00,0x05,0x00,0x01]
# 'Maestro TEST' -> [0xb0,0x12,0x34,0x56,0x78]
# 'Self Service' -> [0xa0,0x00,0x00,0x00,0x24,0x01]
# 'American Express' -> [0xa0,0x00,0x00,0x00,0x25]
# 'ExpressPay' -> [0xa0,0x00,0x00,0x00,0x25,0x01,0x07,0x01]
# 'Link' -> [0xa0,0x00,0x00,0x00,0x29,0x10,0x10]
# 'Alias AID' -> [0xa0,0x00,0x00,0x00,0x29,0x10,0x10]
	     	
# MASTERCARD AID
AID = [0xa0,0x00,0x00,0x00,0x04,0x10,0x10]

# define the apdus used in this script
GET_RESPONSE = [0x00, 0xC0, 0x00, 0x00 ]
SELECT = [0x00, 0xA4, 0x04, 0x00]
CMD = [0x00, 0xB2, 0x01, 0x0C, 0x00]

# define SW1 return values
SW1_RESPONSE_BYTES= 0x61
SW1_WRONG_LENGTH= 0x6c
SW12_OK= [0x90,0x00]
SW12_NOT_SUPORTED= [0x6a,0x81]
SW12_NOT_FOUND= [0x6a,0x82]
SW12_COND_NOT_SAT= [0x69,0x85]          # conditions of use not satisfied

def printhelp():
        if sys.platform == 'linux-i386' or sys.platform == 'linux2':
                os.system("clear")
        elif sys.platform == 'win32':
                os.system("cls")
        else:
                os.system("cls")
        
	print "======================================================"
	print u"Paypass Credit Card Reader [http://www.mertsarica.com]"
	print "======================================================"

def hexprint(data):
        index= 0

        while index < len(data):
                print '%02x' % data[index],
                index += 1
        print


def textprint(data):
        index= 0
        out= ''

        while index < len(data):
                if data[index] >= 0x20 and data[index] < 0x7f:
                        out += chr(data[index])
                else:
                        out += '.'
                index += 1
        print out

def try_cmd():
        le= 0x00
        apdu = CMD
        response, sw1, sw2 = send_apdu(apdu)
        if response:
                if Verbose:
                        print '\t[VERBOSE] Got Response!'
                return response
        else:
                print '\t[ERROR] No Response'
                return False, 0, ''


def parse_ccdata(response2):
        OFFSET_CC= 121
        OFFSET_EXP = 77

        print "[+] Primary Account Number (PAN):",
        index=0
        ccnum=""
        while index < len(response2[OFFSET_CC:OFFSET_CC + 8]):
                ccnum += '%02x' % response2[OFFSET_CC + index]
                index +=1
        print ccnum

        print "[+] Expiration Date:",
        index=0
        exp=[]
        while index < len(response2[OFFSET_EXP:OFFSET_EXP + 4]):
                exp += chr(response2[OFFSET_EXP + index]),
                index +=1
        exp = "".join(exp)
        exp = exp[2:4] + "/" + exp[0:2] 
        print exp

def check_return(sw1,sw2):
        if [sw1,sw2] == SW12_OK:
                return True
        return False

def send_apdu(apdu):
        response, sw1, sw2 = cardservice.connection.transmit( apdu, Protocol )
        if sw1 == SW1_WRONG_LENGTH:
                apdu= apdu[:len(apdu) - 1] + [sw2]
                return send_apdu(apdu)
        if sw1 == SW1_RESPONSE_BYTES:
                apdu = GET_RESPONSE + [sw2]
                response, sw1, sw2 = cardservice.connection.transmit( apdu, Protocol )
        return response, sw1, sw2

def select_aid(aid):
        apdu = SELECT + [len(aid)] + aid + [0x00]
        response, sw1, sw2= send_apdu(apdu)
        if check_return(sw1,sw2):
                return True, response, sw1, sw2
        else:
                return False, [], sw1,sw2

# main loop

if __name__ == '__main__':
        if sys.platform == 'linux-i386' or sys.platform == 'linux2':
                os.system("clear")
        elif sys.platform == 'win32':
                os.system("cls")
        else:
                os.system("cls")
        
	print "======================================================"
	print u"Paypass Credit Card Reader [http://www.mertsarica.com]"
	print "======================================================"

	try:
                
                try:
                        cardtype = AnyCardType()
                        
                        print '[*] Insert a card within 10s...'
                        
                        cardrequest = CardRequest( timeout=10, cardType=cardtype )
                        cardservice = cardrequest.waitforcard()
                        cardservice.connection.connect(Protocol)

                        print '[*] Connecting...'
                        # hexprint(AID)
                        
                        selected, response, sw1, sw2= select_aid(AID)
                        
                        if selected:
                                if Verbose:
                                        print "Success!"
                                        print "Response: \n\t",
                                        textprint(response)

                                if Verbose:
                                        print "\t[VERBOSE]: ",
                                        hexprint(response)
                                        print '\nRequesting Track Info: \n\t',
                                        hexprint(CMD)
                                        
                                response2 = try_cmd()
                                
                                if Verbose:
                                        print "\t[VERBOSE]: ",
                                        hexprint(response2)
                                        print "\t[VERBOSE]: ",
                                        textprint(response2)
                                parse_ccdata(response2)

                except CardRequestTimeoutException:
                        print 'time-out: no card inserted during last 10s'
                        
        except KeyboardInterrupt:	
            print "[+] Bye..."
