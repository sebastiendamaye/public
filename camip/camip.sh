#!/bin/sh

# Directory where images and videos will be saved
DIRCAM=/data/script/camip

# Freebox camera password (user is freeboxcam)
CAMPWD="**************"

# camera IP addr
CAMIP="192.168.******"

DIRJPG=$DIRCAM/camipjpg
DIRMPG=$DIRCAM/camipmpg
DIRTMP=$DIRCAM/tmp
DIRBCP=$DIRCAM/bcp

### create directories if not present
mkdir -p $DIRJPG
mkdir -p $DIRMPG
mkdir -p $DIRTMP
mkdir -p $DIRBCP

while true
do

    JPG=`date +%Y%m%d%H%M%S`.jpg
    DT=`date '+%Y-%m-%d_%H:%M:%S'`
    DTMPG=`date +%Y%m%d`.mp4

    wget -O $DIRJPG/$JPG -q "http://freeboxcam:$CAMPWD@$CAMIP/img/snapshot.cgi?size=4&quality=5"
    
    ### Overlay datetime to image
    convert -font helvetica -fill white -pointsize 10 -draw "text 5,10 '$DT'" $DIRJPG/$JPG $DIRJPG/$JPG
    
    ### instead use webservice to convert datetime to image
    ### use img3me service (you will need an API key)
    #URL="https://img4me.p.mashape.com/?bcolor=000000&fcolor=FFFFFF&font=trebuchet&size=12&text=$DT&type=jpg"
    #wget -O $DIRTMP/dt.jpg -q `curl -s --get --include $URL -H 'X-Mashape-Key: ***********************************' -H 'Accept: text/plain' | grep http`

    ### Now overlay datetime to image
    #composite -blend 30 $DIRTMP/dt.jpg $DIRJPG/$JPG $DIRJPG/$JPG

    if [ $(date '+%H%M') = '2359' ]
	then
        #cat $DIRJPG/*.jpg | ffmpeg -f image2pipe -r 25 -i - -vcodec mpeg4 -b 15000k $DIRMPG/$DTMPG
        #ffmpeg -r 25 -f image2 -s 1280x720 -i $DIRJPG/%*.jpg -vcodec libx264 -crf 25  -pix_fmt yuv420p $DIRMPG/$DTMPG
        ffmpeg -y -framerate 25 -pattern_type glob -i "$DIRJPG/*.jpg" -c:v libx264 -crf 25 -vf format=yuv420p -movflags +faststart $DIRMPG/$DTMPG
        rm -f $DIRBCP/*.jpg
        mv $DIRJPG/*.jpg $DIRBCP
        # push mp4 to syno
        scp -P 2223 $DIRMPG/$DTMPG **********@192.168.******:/volume1/camip/
    fi

    ### do a capture every 5 seconds
    sleep 5

done
