#!/usr/bin/env python
#
# Author: Sebastien Damaye
# Description: streaming custom search command that shows information about youtube
#   videos based on squid proxy logs
# Use as follows:
# source="*squid*" uri="*www.youtube.com/watch?v=*" | sort _time | youtube uri | table _time clientip uri youtube
#

import splunk.Intersplunk 
import re
import urllib2
import urlparse
import time

def getYoutube(uri):
    m = re.match(r'^https:\/\/www.youtube.com\/watch\?v=([a-zA-Z0-9_-]+)(&.+)?$', uri)
    if m:
        response = urllib2.urlopen('http://youtube.com/get_video_info?video_id=%s' % m.group(1))
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
