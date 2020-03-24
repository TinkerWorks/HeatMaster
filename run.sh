#!/bin/bash

rsync -aAv --progress --delete "$(pwd)/" pi@heatmaster:~/HeatMaster_$USER/

ssh -t pi@heatmaster pip3 install -r /home/pi/HeatMaster_$USER/requirements.txt

case "$1" in
    "init")
        ssh -t pi@heatmaster python3 /home/pi/HeatMaster_$USER/HeatMaster/__init__.py
        ;;
    "main")
        ssh -t pi@heatmaster python3 /home/pi/HeatMaster_$USER/HeatMaster/__main__.py
        ;;
    *)
        exit 4
        ;;
esac
