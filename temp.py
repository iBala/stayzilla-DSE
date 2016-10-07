#!/usr/local/bin/python
import re
f = open('wrongphno.txt', 'r')

for line in f:
        match = re.match('^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$', line)
        if match == None:
		print line.strip() + " failed"
        else:
		print line.strip() + " passed"
