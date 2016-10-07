import re
import socket
import smtplib
import dns.resolver
import sys

#Input check
if(len(sys.argv) <1):
	print "usage:"
	print sys.argv[0] + " <user data file>"
	print "List of emails in a file separated by newlines"
	exit()

# Address used for SMTP MAIL FROM command  
fromAddress = 'balakumaran.p@stayzilla.com'

# Simple Regex for syntax checking
regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'

# Email address to verify
#inputAddress = input('Please enter the emailAddress to verify:')
fd = open(sys.argv[1],'rb')
fdw = open("response.txt",'w')
for inputAddress in fd:
    inputAddress = inputAddress.strip()
    addressToVerify = str(str(inputAddress).lower()).strip()
    
    # Syntax check
    match = re.match(regex, addressToVerify)
    if match == None:
    	fdw.write(addressToVerify + ", dead\n")
	continue
    
    # Get domain for DNS lookup
    splitAddress = addressToVerify.split('@')
    domain = str(splitAddress[1])
    print('Domain:', domain)
    
    # MX record lookup
    try:
	records = dns.resolver.query(domain, 'MX')
    except:
	print "No such domain"
    	fdw.write(addressToVerify + ", dead\n")
	continue
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
    	fdw.write(addressToVerify + ", dead\n")
	continue
    
    #print(code)
    #print(message)
    
    # Assume SMTP response 250 is success
    if code == 250:
    	fdw.write(addressToVerify + ", alive\n")
    else:
    	fdw.write(addressToVerify + ", dead\n")
