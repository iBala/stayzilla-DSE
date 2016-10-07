import re
import csv
import socket
import requests
import json
import smtplib
import dns.resolver
import sys

#Input check
if(len(sys.argv) <1):
	print "usage:"
	print sys.argv[0] + " <user data file>"
	print "List of emails in a file separated by newlines"
	exit()

##############
#Sends an SMS to the actual number and waits for a response.
#Input: Phone number
#Output: live/dead
#############
def phone_isalive(pPhone):
        res = requests.get('http://api-alerts.solutionsinfini.com/v3/?method=hlr&api_key= 105987m0t645eqc90r7g5&to=91'+pPhone+'&format=json')
        data = json.loads(res.text)
        if (data['data'][0]['status'] == 'DELIVRD'):
                return "exists"
        else:
		print pPhone
		print data['data'][0]['status']
                return "not_exists"

# Simple Regex for syntax checking
#regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'
regex = '^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$'

# Email address to verify
#inputAddress = input('Please enter the ph no to verify:')
#addressToVerify = str(inputAddress).lower()

fd = open(sys.argv[1],'rb')
fdw = open("phoneResponse.txt",'w')
for inputAddress in fd:
	inputAddress = inputAddress.strip()
	addressToVerify = str(str(inputAddress).lower()).strip()

	# Syntax check
	match = re.match(regex, inputAddress)
	if match == None:
    		fdw.write(addressToVerify + ", dead\n")
		print "No Match"
		continue
	if (phone_isalive(addressToVerify) == "exists"):
	    	fdw.write(addressToVerify + ", alive\n")
	else:
	    	fdw.write(addressToVerify + ", dead\n")

