#!/bin/env python
import sys

if len(sys.argv) < 2:
    print "Usage: %s <file.csv>" % sys.argv[0]
    sys.exit()

f = open(sys.argv[1])
linenum = 1
output = []

print "domain,classification"

for l in f:
    line = l.split("\n")[0]

    if linenum == 1: # header
        header = line.split(",")
        # remove first 3 items (rank, domain, total)
        header = header[3:]

    else: # std line
        vals = line.split(",")
        # gather domain and nreq
        domain = vals[1]

        # remove first 3 values
        vals = vals[3:]

        count = 0
        for i, v in enumerate(vals):
            if v == "1":
                print "%s,%s" % (domain, header[i].replace('"',''))
                count += 1

        # if no classification found, still print the domain with N/A
        if count == 0:
     	    print "%s,N/A" % domain

    linenum += 1

