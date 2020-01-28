#!/bin/sh
scp -r pilou@192.168.1.4:/data/script/camip2/camipoutput/* /volume1/video-project/footages/camip/
ssh pilou@192.168.1.4 "rm -f /data/script/camip2/camipoutput/*"