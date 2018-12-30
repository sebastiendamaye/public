#!/bin/env python
import sys

def main():
    if(len(sys.argv)<2):
        print("CSV file missing")
        sys.exit(0)

    gpx = open("mytrace.gpx","w")
    csv = open(sys.argv[1],"r")
    
    ### GPX trace header
    gpx.write('<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n')
    gpx.write('<gpx xmlns="http://www.topografix.com/GPX/1/1" creator="byHand" version="1.1"\n') 
    gpx.write('    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
    gpx.write('    xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">"\n')
   
    numl = 1
    for l in csv:
        # dt is list of fields for each line
        dt = l.split(',')

        # very 1st line is file header
        if(numl==1):
            # search index of 'GPS' and 'Alt(m)' in file header
            idate = dt.index('Date')
            itime = dt.index('Time')
            igps = dt.index('GPS')
            ialt = dt.index('Alt(m)')

        # normal lines (not header)
        else:
            gps = dt[igps].split(" ")
            gpx.write('    <wpt lat="%s" lon="%s">\n' % (gps[0], gps[1]))
            gpx.write('        <ele>%s</ele>\n' % dt[ialt])
            gpx.write('        <time>%sT%sZ</time>\n' % (dt[idate], dt[itime].split(".")[0]))
            gpx.write('        <name>P%s</name>\n' % numl)
            gpx.write('        <sym>empty</sym>\n')
            gpx.write('    </wpt>\n')


        numl += 1

    ### End of GPX trace
    gpx.write('</gpx>\n')

    csv.close()
    gpx.close()

if __name__ == "__main__":
    main()
