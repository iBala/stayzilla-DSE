#!/usr/bin/python

#################
#Parser file to check validity of email and phone
#balakumaran.p@stayzilla.com
#(c) inasra.com
#################

import sys
import csv
import pandas as pd
import numpy as np
import re 
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

#Get index of email

uemail_index=prop_data[0].index("uemail")
uphno_index=prop_data[0].index("uphno")
umono_index=prop_data[0].index("umono")
hliaemail_index=prop_data[0].index("hliaemail")
hliano1_index=prop_data[0].index("hliano1")
hliano2_index=prop_data[0].index("hliano2")

for i in range(0,len(prop_data)):
	#Clean the data
	#Checks made: Remove extra white spaces, replace comma with New line, Replace / with new line, strip of '.' from the end, replace ;, : with new line
	prop_data[i][uemail_index]=prop_data[i][uemail_index].replace(",","\n")
	prop_data[i][uemail_index]=prop_data[i][uemail_index].replace(";","\n")
	prop_data[i][uemail_index]=prop_data[i][uemail_index].replace(":","\n")
	prop_data[i][uemail_index]=prop_data[i][uemail_index].replace("\/","\n")
	prop_data[i][uemail_index]=prop_data[i][uemail_index].replace("\\","\n")
	#prop_data[i][uemail_index]=prop_data[i][uemail_index].replace(" ","")
	#prop_data[i][uemail_index]=re.sub(' +','',prop_data[i][uemail_index])
	temp = prop_data[i][uemail_index].split("\n")
	temp=list(filter(None, temp))
	if (len(temp)>1):
		for i in range(0,len(temp)):
			temp[j]=temp[j].strip(".")
			temp[j]=re.sub('\s\s+','',temp[j])
			match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', temp[j].lower())
			if match == None:
	                	prop_data[i].append("CHECK: "+temp[j]+" is invalid\r")
        		else:
                		prop_data[i].append("CHECK: "+temp[j]+" is valid\r")
	else:
		match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', prop_data[i][uemail_index].lower())
		if match == None:
			prop_data[i].append("Email_regex_invalid")
		else:
			prop_data[i].append("Email_regex_valid")

for i in range(0,len(prop_data)):
	temp=prop_data[i][uphno_index]
	if (not "/" in temp) and (not "," in temp):
		prop_data[i][uphno_index]=temp.strip().replace(" ","")
		
	match = re.match('^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$', prop_data[i][uphno_index])
	if match == None:
		prop_data[i].append("uphno_regex_invalid")
	else:
		prop_data[i].append("uphno_regex_valid")

for i in range(0,len(prop_data)):
	match = re.match('^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$', prop_data[i][umono_index])
	if match == None:
		prop_data[i].append("umono_regex_invalid")
	else:
		prop_data[i].append("umono_regex_valid")

	prop_data[i][uemail_index]=prop_data[i][uemail_index].replace(",","\n")
	prop_data[i][uemail_index]=prop_data[i][uemail_index].strip(".")
	prop_data[i][uemail_index]=prop_data[i][uemail_index].replace(";","\n")
	prop_data[i][uemail_index]=prop_data[i][uemail_index].replace(":","\n")
	prop_data[i][uemail_index]=prop_data[i][uemail_index].replace("\/","\n")
	prop_data[i][uemail_index]=prop_data[i][uemail_index].replace("\\","\n")
	prop_data[i][uemail_index]=re.sub('\s\s+','',prop_data[i][uemail_index])
	#prop_data[i][uemail_index]=re.sub(' +','',prop_data[i][uemail_index])
	#prop_data[i][uemail_index]=prop_data[i][uemail_index].replace(" ","")
	temp = prop_data[i][hliaemail_index].split("\n")
	#prop_data[i][uemail_index]
	temp=list(filter(None, temp))
	if (len(temp)>1):
		for j in range(0,len(temp)):
			temp[j]=temp[j].strip(".")
			temp[j]=re.sub('\s\s+','',temp[j])
			match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', temp[j].lower())
			if match == None:
	                	prop_data[i].append("CHECK")
				break
        		else:
                		#prop_data[i].append("CHECK: "+temp[j]+" is valid  ")
	                	prop_data[i].append("CHECK")
				break
	else:
		match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', prop_data[i][hliaemail_index].lower())
		if match == None:
			prop_data[i].append("hliaemail_regex_invalid")
		else:
			prop_data[i].append("hliaemail_regex_valid")
#for i in range(0,len(prop_data)):
#	match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', prop_data[i][hliaemail_index].lower())
#	if match == None:
#		prop_data[i].append("hliaemail_regex_invalid")
#	else:
#		prop_data[i].append("hliaemail_regex_valid")

for i in range(0,len(prop_data)):
	match = re.match('^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$', prop_data[i][hliano1_index])
	if match == None:
		prop_data[i].append("hliano1_regex_invalid")
	else:
		prop_data[i].append("hliano1_regex_valid")

for i in range(0,len(prop_data)):
	match = re.match('^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$', prop_data[i][hliano2_index])
	if match == None:
		prop_data[i].append("hliano2_regex_invalid")
	else:
		prop_data[i].append("hliano2_regex_valid")

#FName_Issues=user_data.loc[(user_data["fname"].isnull()) | (len(user_data["fname"])<=2)]
#write_to_file(FName_Issues,"FnameIssues.csv")

write_to_file(prop_data,"email_regex.csv")
