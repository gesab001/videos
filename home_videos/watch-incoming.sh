#!/bin/bash

echo hello

TARGET=/media/pi/Transcend/goprosync/

inotifywait -m -e create -e moved_to --format "%f" $TARGET \
        | while read FILENAME
                do
                        echo Detected $FILENAME, adding new font
                        python3 videos.py
                done
