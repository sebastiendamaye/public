#!/bin/sh

CAMIPDIR=/data/script/camip2
CAMIPMPG=$CAMIPDIR/camipmpg
CAMIPCONFIG=$CAMIPDIR/config
CAMIPOUTPUT=$CAMIPDIR/camipoutput

rm -f $CAMIPCONFIG/mylist.txt
for f in $CAMIPMPG/*.mp4; do echo "file '$f'" >> $CAMIPCONFIG/mylist.txt; done

# Concat all mp4 into single mp4 output file
ffmpeg -f concat -safe 0 -i $CAMIPCONFIG/mylist.txt -c copy $CAMIPOUTPUT/`date +%Y%m%d`.mp4

#Remove old mp4 files
rm -f $CAMIPMPG/*
