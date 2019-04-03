#!/bin/bash
scriptDir="$(cd "$(dirname "$0")" && pwd)"
currentTime=`date +"%H:%M:%S"`
python $scriptDir/LuxaforCommand.py $currentTime