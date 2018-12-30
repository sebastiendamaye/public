#!/bin/env python
###
# AUTHOR:      Captain Pilou (https://www.youtube.com/channel/UCSS8dwwaBDS6-hRnYo2yVDA)
# REVISION:    2
# LAST MODIF:  2018-12-30
# DESCRIPTION: This program takes a CSV file as parameter (Taranis telemetry logs) and
#              creates a GPX file based on GPS coords, altitude and date/time

import argparse
import sys

def main(args):
    gpx = open("mytrace.gpx","w")
    csv = open(args.csv,"r")
    relativealt = 99999
    
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
            #if GPS field is empty, take previous GPS entry
            if dt[igps]:
                gps = dt[igps].split(" ")
            
            # if relativealt is set
            if args.relativealt:
                if relativealt == 99999:
                    relativealt = int(dt[ialt])
            else:
                relativealt = 0

            gpx.write('    <wpt lat="%s" lon="%s">\n' % (gps[0], gps[1]))
            gpx.write('        <ele>%s</ele>\n' % str(int(dt[ialt])-relativealt))
            gpx.write('        <time>%sT%sZ</time>\n' % (dt[idate], dt[itime].split(".")[0]))
            gpx.write('        <name>P%s</name>\n' % numl)
            gpx.write('        <sym>empty</sym>\n')
            gpx.write('    </wpt>\n')

        numl += 1

    ### End of GPX trace
    gpx.write('</gpx>\n')

    csv.close()
    gpx.close()

def args():
    parser = argparse.ArgumentParser(description='Extracts GPS coords from Taranis CSV log file to create a GPX file.')
    parser.add_argument('csv',
                    help='input file (Taranis CSV log file)')
    parser.add_argument('-r', '--relativealt', action='store_true',
                    help='consider altitude as relative (1st known altitude considered as zero)')
    args = parser.parse_args()
    main(args)

if __name__ == "__main__":
    args()
