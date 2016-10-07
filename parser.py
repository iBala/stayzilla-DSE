#!/usr/bin/python

#################
#Parser file for user data cleanup project
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
		print "Written "+filename
	if isinstance(data, pd.DataFrame):
		data.to_csv(filename,index = False)
		print "Written "+filename



#Input check
if(len(sys.argv) <2):
	print "usage:"
	print sys.argv[0] + " <property data file>" + " <user data file>"
	print "property data file should have the fields \n1. HID \n2. mapped UID\n3. umono\n4. uphno\n5. email\n6. hotel_type\n7. hliano1\n8. hliano2\n9. hliaemail\n10. hotelstatus"
	print "User data file should have the following fields \n1. uid\n2. uregdate\n3. uemail\n4. uname\n5. fname\n6. lname\n7. umono\n8. uphno"

#Read the property data file
#prop_data = csv.reader(open(sys.argv[1],"rb"), delimiter = ',')

#Read the user data filee
#user_data = csv.reader(open(sys.argv[2],"rb"), delimiter = ',')

#Convert the csv data into array for easier processing
#x = list(prop_data)
#prop_data=np.array(x)

#x = list(user_data)
#user_data=np.array(x)
prop_data=pd.read_csv(sys.argv[1],dtype=None,sep='\t')
user_data=pd.read_csv(sys.argv[2],dtype=None)
prop_data.replace(r'\s+', np.nan, regex=True)
user_data.replace(r'\s+', np.nan, regex=True)

#Get all live properties
live_prop=prop_data.loc[prop_data["hotelstatus"] == 2]
live_prop=live_prop.drop('hadd',1)
#no_uid = live_prop.loc[live_prop["uid"]==np.nan]

#live_prop.add("Comment")
write_to_file(live_prop,"live_prop.csv")
#live_prop.loc[live_prop["uid"].isnull()]["Comment"]="UID Does not exist"
#write_to_file(live_prop,"live_prop.csv")

nouid_prop=live_prop.loc[(live_prop["uid"].isnull()) | (live_prop["uid"] == 0) ]
write_to_file(nouid_prop,"nouid_prop.csv")
prop_with_id=live_prop.loc[(live_prop["uid"].notnull()) | (live_prop["uid"] == 0) ]
write_to_file(prop_with_id,"uid_prop.csv")

#Check if the liason details have any UID mapped
#user_data_1 = user_data.copy(deep=True)
#user_data_1.rename(columns={'uemail': 'hliaemail'}, inplace=True)
#user_data_1.rename(columns={'uid': 'uid_hliaemail'}, inplace=True)
#user_data_1.rename(columns={'umono': 'umono_hliaemail'}, inplace=True)
#user_data_1.rename(columns={'uphno': 'uphno_hliaemail'}, inplace=True)
#user_data_1.rename(columns={'fname': 'fname_hliaemail'}, inplace=True)
#user_data_1.rename(columns={'lname': 'lname_hliaemail'}, inplace=True)
#print "user_data_1="
#print user_data_1[0:4]
#hliaemail_mapped=pd.merge(live_prop,user_data_1,  on="hliaemail",how="left")
#hliaemail_mapped=live_prop.merge(user_data_1,  on="hliaemail")
#write_to_file(user_data_1,"user_data_1.csv")
#hliaemail_mapped=live_prop.join(user_data_1)
#hliaemail_mapped=live_prop.join(user_data_1,on="hliaemail")
#print "userdata 1 mapped. Now writing to file"
#print "Live_prop="
#print live_prop.shape
#print "user_data="
#print user_data.shape
#print "hliaemail_mapped="
#print hliaemail_mapped.shape
#print hliaemail_mapped[0:4]
#hliaemail_2=hliaemail_mapped[0:100000]
#write_to_file(hliaemail_2,"liaemail.csv")
#print "Written yo!"
#print hliaemail_mapped[0:4]
#print live_prop[0:4]


#Check if email ID matches re
