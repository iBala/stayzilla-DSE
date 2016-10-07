#!/usr/bin/python

#################
#Cleaning User data
#balakumaran.p@stayzilla.com
#(c) inasra.com
#################

import sys
import csv
import pandas as pd
import numpy as np

#Functions

###############
#Write to file 
#Input: variable to be written, file name
#Input variable should be a 2D array
###############
def write_to_file(data,filename="output1.csv"):
	if type(data).__module__ == np.__name__:
		writer=csv.writer(open(filename,"wb"))
		for i in range(0,len(data)):
			writer.writerow(data[i])
	if isinstance(data, pd.DataFrame):
		print "writing to file"
		data.to_csv(filename)


#Input check
if(len(sys.argv) <1):
	print "usage:"
	print sys.argv[0] +"<user data file>"
	print "User data file should have the following fields \n1. uid\n2. uregdate\n3. uemail\n4. uname\n5. fname\n6. lname\n7. umono\n8. uphno"

user_data=pd.read_csv(sys.argv[1],dtype=None)
user_data.replace(r'\s+', np.nan, regex=True)
#user_data["parsed_email"]=np.nan

#Regex check for email
# 1.Get all emails with .temp
#user_data["parsed_email"]=np.where(user_data["uemail"].endswith(".temp"),user_data["uemail"].strip(".temp"))
user_data["parsed_email"]=user_data["uemail"].str.strip("temp")

#Get all user IDs where email is empty
#empty_uid=user_data.loc[user_data["uemail"].isnull()]

write_to_file(user_data,"emptyuid.csv")
