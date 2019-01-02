#!/bin/sh

# Directory where images and videos will be saved
DIRCAM=/volume1/homes/*********/camip

# Freebox camera password (user is freeboxcam)
CAMPWD="************"

# camera IP addr
CAMIP="192.168.1.*******"

DIRJPG=$DIRCAM/camipjpg
DIRMPG=$DIRCAM/camipmpg
DIRTMP=$DIRCAM/tmp

### create directories if not present
mkdir -p $DIRJPG
mkdir -p $DIRMPG
mkdir -p $DIRTMP

while true
do

    JPG=`date +%Y%m%d%H%M%S`.jpg
    DT=`date '+%Y-%m-%d_%H:%M:%S'`
    DTMPG=`date +%Y%m%d`.mp4

    wget -O $DIRJPG/$JPG -q http://freeboxcam:$CAMPWD@$CAMIP/img/snapshot.cgi?size=4&quality=5

    ### Overlay datetime to image
    ### too complex to use convert since no font is available on syno
    #convert -font helvetica -fill white -pointsize 10 -draw "text 5,10 '$DT'" $DIRJPG/$JPG $DIRJPG/$JPG
    
    ### instead use webservice to convert datetime to image
    ### use img3me service (you will need an API key)
    URL="https://img4me.p.mashape.com/?bcolor=000000&fcolor=FFFFFF&font=trebuchet&size=12&text=$DT&type=jpg"
    wget -O $DIRTMP/dt.jpg -q `curl -s --get --include $URL -H 'X-Mashape-Key: **************************' -H 'Accept: text/plain' | grep http`

    ### Now overlay datetime to image
    composite -blend 30 $DIRTMP/dt.jpg $DIRJPG/$JPG $DIRJPG/$JPG

    if [ $(date '+%H%M') = '0000' ]
	then
        cat $DIRJPG/*.jpg | ffmpeg -f image2pipe -r 25 -i - -vcodec mpeg4 -b 15000k $DIRMPG/$DTMPG
        rm -f $DIRJPG/*.jpg
    fi

    ### do a capture every 5 seconds
    sleep 5

done
