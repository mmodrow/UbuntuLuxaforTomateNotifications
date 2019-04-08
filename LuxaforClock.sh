#!/bin/bash
argument="$1"
scriptDir="$(cd "$(dirname "$0")" && pwd)"

function update {
    currentTime=`date +"%H:%M:%S"`
    echo "LuxaforCommand $currentTime"
    python $scriptDir/LuxaforCommand.py $currentTime
}

update
if [ "$argument" = "repeat" ]; then
    while [ 1 = 1 ]
    do
        sleep 60
        update
    done
fi