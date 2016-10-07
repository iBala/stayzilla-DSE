#!/usr/local/bin/python

import sys
import csv
import numpy as np

#Read the user data filee
#user_data = csv.reader(open(sys.argv[1],"rb"), delimiter = ',')
#x=list(user_data)
#user_data=np.array(x)

user_data=np.genfromtxt(sys.argv[1],delimiter=",")

#Get index no for uemail
index=user_data.index("uemail")

for i in range(0,len(user_data)):
	if(user_data[i][index].endswith(".temp")):
		user_data[i][index].strip(".temp")

writer=csv.writer(open(filename,"wb"))
for i in range(0,len(data)):
	writer.writerow(data[i])

