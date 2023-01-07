#!/bin/bash

HOST=heatmaster

rsync -rPv --delete "$(pwd)/" $HOST:~/HeatMaster/

case "$1" in
    "req")
        ssh -t ${HOST} pip3 install --user -r /home/$USER/HeatMaster/requirements.txt
        ssh -t ${HOST} pip3 install --user -r /home/$USER/HeatMaster/tests/requirements.txt
        ;;
    "main")
        ssh -t ${HOST} "cd HeatMaster ; python3 -m heatmaster heatmaster/data/config.json"
        ;;
    "test")
        ssh -t "${HOST}" "cd HeatMaster ; nose2-3 "
        ;;
    "copy")
        echo "Just copy and done"
        ;;
    *)
        exit 4
        ;;
esac
