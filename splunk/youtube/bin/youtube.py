#!/usr/bin/env python
#
# Author: Sebastien Damaye
# Description: streaming custom search command that shows information about youtube videos based on squid proxy logs
# Revision: 2
# Update: 20160724
#
# Use as follows:
# source="*squid*" uri="*www.youtube.com/watch?v=*" OR source="*squid*" uri="*www.youtube.com/csi_204*docid=*" | sort _time | youtube uri | table _time clientip uri youtube v
#

import splunk.Intersplunk 
import re
import urllib2
import urlparse
import time

def getYoutube(uri):
    # youtube (PC format)
    m1 = re.match(r'^https:\/\/www.youtube.com\/watch\?v=([a-zA-Z0-9_-]+)(&.+)?$', uri)
    # youtube (Android tablet)
    m2 = m = re.match(r'^https:\/\/www.youtube.com(.*)&docid=([a-zA-Z0-9_-]+)(&.+)?$', uri)
    if m1 or m2:
        if m1:
            id = m.group(1)
        else:
            id = m.group(2)
        response = urllib2.urlopen('http://youtube.com/get_video_info?video_id=%s' % id)
        html = response.read()
        qs = urlparse.parse_qs(html)
        if 'title' in qs:
            title = qs['title'][0]
            length = time.strftime("%H:%M:%S", time.gmtime(int(qs['length_seconds'][0])))
            return "(%s) %s" % (length, title)
        else:
            return "Error while retrieving info"
    else:
        return "Regexp not recognized"

# get the previous search results
results,unused1,unused2 = splunk.Intersplunk.getOrganizedResults()

# for each results, add a 'youtube' attribute, calculated from the uri field
for result in results:
   result["youtube"] = getYoutube(result["uri"])

# output results
splunk.Intersplunk.outputResults(results)
