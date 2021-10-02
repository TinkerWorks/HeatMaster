#!/bin/bash

rsync -aAv --progress --delete "$(pwd)/" heatmaster:~/HeatMaster/

case "$1" in
    "req")
        ssh -t heatmaster pip3 install --user -r /home/$USER/HeatMaster/requirements.txt
        ;;
    "main")
        ssh -t heatmaster "PYTHONPATH=/home/$USER/HeatMaster python3 /home/$USER/HeatMaster/heatmaster/__main__.py"
        ;;
    *)
        exit 4
        ;;
esac
