#!/usr/bin/python

#################
#Program to validate and correct all Host user details in Stayzilla.
#balakumaran.p@stayzilla.com
#(c) inasra.com
#################

import sys
import csv
import pandas as pd
import numpy as np
import re 
import MySQLdb
import socket
import smtplib
import dns.resolver
import requests
import json

#Functions

###############
#Write to file 
#Input: variable to be written, file name
#Input variable should be a 2D array
###############
def write_to_file(data,filename="output1.csv"):
	if type(data).__module__ == np.__name__:
		print "writing to "+filename
		writer=csv.writer(open(filename,"wb"))
		for i in range(0,len(data)):
			writer.writerow(data[i])
	if isinstance(data, pd.DataFrame):
		print "writing to "+filename
		data.to_csv(filename,index_col=FALSE)
	else:
		writer=csv.writer(open(filename,"wb"))
		print "writing to "+filename
		for i in range(0,len(data)):
			writer.writerow(data[i])

##############
#Checks syntax and validates email for real
#Input: email address (or what is assumed to be one)
#Output: Valid/invalid
##############
def verify_real_email(pEmail):
    addressToVerify = str(str(pEmail).lower()).strip()
    # Get domain for DNS lookup
    splitAddress = addressToVerify.split('@')
    domain = str(splitAddress[1])
    print('Domain:', domain)
    
    # MX record lookup
    try:
	records = dns.resolver.query(domain, 'MX')
    except:
	print "No such domain"
	return "domain_invalid"
    mxRecord = records[0].exchange
    mxRecord = str(mxRecord)
    
    # Get local server hostname
    host = socket.gethostname()
    
    # SMTP lib setup (use debug level for full output)
    server = smtplib.SMTP()
    server.set_debuglevel(0)
    
    # SMTP Conversation
    try:
    	server.connect(mxRecord)
    	server.helo(host)
    	server.mail(fromAddress)
    	code, message = server.rcpt(str(addressToVerify))
    	server.quit()
    except:
	print "failed to connect to domain server"
	return "domain_not_responding"
    
    #print(code)
    #print(message)
    
    # Assume SMTP response 250 is success
    if code == 250:
	return "success"
    else:
	return "domain_not_responding"
	

##############
#Checks syntax and validates email for real
#Input: email address (or what is assumed to be one)
#Output: Valid/invalid
##############
def validate_email(pEmail):
	#Clean Email address
	chars_to_remove = [',',';',':','\/','\\',' ','+','(',')','-']
	pEmail = pEmail.translate("\n",chars_to_remove)
	match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', pEmail.lower())
	if match == None:
		return "syntax_error"
	else:
		#Verify if mail exists
		return (verify_real_email(pEmail))

###############
#Checks syntax and validates phone number
#Input: Phone number
#Output: Valid/Invalid
###############
def validate_phone(pPhone):
	#Clean Phone number
	chars_to_remove = [',',';',':','\/','\\',' ','+','(',')','-']
	pPhone = pPhone.translate("\n",chars_to_remove)
        match = re.match('^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$', pPhone)
	if match == None:
		return "syntax_error"
	else:
		#Verify if mail exists
		return (verify_real_phone(pPhone))
		

##############
#Sends an SMS to the actual number and waits for a response.
#Input: Phone number
#Output: live/dead
#############
def phone_isalive(pPhone):
	res = requests.get('http://api-alerts.solutionsinfini.com/v3/?method=hlr&api_key= 105987m0t645eqc90r7g5&to='+pPhone+'&format=json')
	data = json.loads(res.text)
	if (data['data'][0]['status'] == 'DELIVRD'):
		return "exists"
	else:
		return "not_exists"

##############
#Check if user is available with email
#Input: db cursor, email
#Output: yes/no
#############
def uid_with_email(cursor,pEmail):
	cursor.execute("select uid from insuser where uemail=\""+email+"\";")
	res = cursor.fetchall()
	if (len(cursor) >1 ):
		return "multiple"
	else if (len(res) <1 ):
		return "no"
	else:
		return res[0][0]

##############
#Check if user is available with phone
#Input: db cursor, phone
#Output: yes/no
#############
def uid_with_phone(cursor,pPhone):
	cursor.execute("select uid from insuser where umono=\""+email+"\";")
	res = cursor.fetchall()
	if (len(cursor) >1 ):
		return "multiple"
	else if (len(res) <1 ):
		return "no"
	else:
		return res[0][0]

##############
#Clean email ID
#Input: email id
#Output: email id
#############
def clean_email(pEmail):
	pEmail = pEmail.strip()
	pEmail = pEmail.strreplace("","")

#Input check
if(len(sys.argv) <1):
	print "usage:"
	print sys.argv[0] + " <user data file>"
	print "User data file should have the following fields \n1. uid\n3. uemail\n4. uname\n5. fname\n6. lname\n7. umono\n8. uphno"
	exit()

#Read the user data file
#user_data=pd.read_csv(sys.argv[1],dtype=None)

with open(sys.argv[1],"rU") as f:
	reader = csv.reader(f)
	prop_data=list(reader)

#Initiate DB Connection
db = MySQLdb.connect(host = "172.31.2.58",user="prod_balakumaran",passwd="StEh7$rAphap",db="inasra")
cursor = db.cursor()

#Cleaning up temp email IDs

