#!/bin/bash

rsync -aAv --progress --delete "$(pwd)/" heatmaster:~/HeatMaster/

LOG_FORMAT="COLOREDLOGS_LOG_FORMAT=\"%(asctime)s %(name)s - %(levelname)s -> %(message)s\""

case "$1" in
    "req")
        ssh -t heatmaster \
            pip3 install --user -r /home/$USER/HeatMaster/requirements.txt
        ;;
    "main")
        ssh -t heatmaster "PYTHONPATH=/home/$USER/HeatMaster ${LOG_FORMAT} \
            python3 /home/$USER/HeatMaster/heatmaster/__main__.py \
                    /home/$USER/HeatMaster/data/config.json"
        ;;
    "mmain")
        ssh -t heatmaster "pushd /home/$USER/HeatMaster && \
            ${LOG_FORMAT} python3 -m heatmaster data/config.json"
        ;;
    *)
        exit 4
        ;;
esac
