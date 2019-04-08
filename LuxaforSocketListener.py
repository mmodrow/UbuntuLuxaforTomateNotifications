#!/usr/bin/env python3
from pyluxafor import LuxaforFlag
from time import sleep
import re
import sys

green = [[LuxaforFlag.LED_ALL, 0, 255, 0]]
red = [[LuxaforFlag.LED_ALL, 255, 0, 0]]
yellow = [[LuxaforFlag.LED_ALL, 255, 192, 0]]
confused = [[LuxaforFlag.LED_BACK_SIDE, 255, 0, 0],[LuxaforFlag.LED_TAB_SIDE, 0, 255, 0]]
extra_confused = [
    [LuxaforFlag.LED_TAB_1, 255, 0, 0],
    [LuxaforFlag.LED_TAB_2, 0, 64, 64],
    [LuxaforFlag.LED_TAB_3, 0, 255, 0],
    [LuxaforFlag.LED_BACK_1, 0, 255, 255],
    [LuxaforFlag.LED_BACK_2, 0, 0, 255],
    [LuxaforFlag.LED_BACK_3, 255, 0, 255]
]
blue = [[LuxaforFlag.LED_BACK_1, 0, 0, 255]]
black = [[LuxaforFlag.LED_ALL, 0, 0, 0]]

state = black

flag = LuxaforFlag()

hexColor = re.compile("^#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})$")
time = re.compile("^(\d{2}):(\d{2}):(\d{2})$")

def setColorByLabel(label):
    label = label.lower()
    flagstatus = []
    if label == 'red' or label == 'busy':
        flagstatus = red
    elif label == 'yellow' or label == 'quiet':
        flagstatus = yellow
    elif label == 'green' or label == 'open':
        flagstatus = green
    elif label == 'black' or label == 'off':
        flagstatus = black
    elif label == 'confused':
        flagstatus = confused
    elif label == 'extra_confused':
        flagstatus = extra_confused
    elif label == 'cops':
        flag.do_pattern(LuxaforFlag.PATTERN_POLICE, 3)
        sleep(3)
        flagstatus = state
    elif label == 'rainbow':
        flag.do_pattern(LuxaforFlag.PATTERN_RAINBOWWAVE, 3)
        sleep(3)
        flagstatus = state
    elif label == 'luxafor':
        flag.do_pattern(LuxaforFlag.PATTERN_LUXAFOR, 3)
        sleep(3)
        flagstatus = state
    elif hexColor.match(label):
        newColor = getColorFromHexString(label)
        flagstatus = [getFlagColor(LuxaforFlag.LED_ALL, newColor)]
    elif time.match(label):
        newColors = getColorsFromTimeString(label)

        hoursLed = getFlagColor(LuxaforFlag.LED_BACK_2, newColors[0])
        minutesLed = getFlagColor(LuxaforFlag.LED_BACK_1,newColors[1])

        flagstatus = [hoursLed, minutesLed]
    setColor(flagstatus)

def setColor(flagstatus):
    global state, flag
    state = flagstatus
    for ledSet in flagstatus :
        flag.do_static_colour(leds=ledSet[0], r=ledSet[1], g=ledSet[2], b=ledSet[3])


#-------------------------------------------------------------------------
#                              Color Handling                            #
#-------------------------------------------------------------------------
def getFlagColor(flag, color):
    return [flag, color[0], color[1], color[2]]

def getColorFromHexString(hexString):
    match = re.match(hexColor, hexString)
    matchGroups = match.groups()
    hexRed = int(matchGroups[0], 16)
    hexGreen = int(matchGroups[1], 16)
    hexYellow = int(matchGroups[2], 16)
    return [hexRed, hexGreen, hexYellow]

def getColorsFromTimeString(timeString):
    match = re.match(time, timeString)
    matchGroups = match.groups()


    seconds = int(matchGroups[2])
    secondsOfMinute = max(0, min(59, seconds))
    secondsPartial = secondsOfMinute / 59.0
    secondsColor = get7StopHeatMapColor(secondsPartial)

    minutes = int(matchGroups[1])
    minutesOfHour = max(0, min(59, minutes))
    minutesPartial = minutesOfHour / 59.0
    minutesColor = get7StopHeatMapColor(minutesPartial)

    hours = int(matchGroups[0])
    hoursOfDay = max(9, min(18, hours)) - 9
    hoursPartial = (hoursOfDay + minutesPartial) / 9.0
    hoursColor = get7StopHeatMapColor(hoursPartial)

    return [hoursColor, minutesColor, secondsColor]

def get7StopHeatMapColor(value):
    stops = [
        [000, 000, 000], # [0] -   0,00% : Black
        [000, 000, 255], # [1] -  16,66% : Blue
        [000, 255, 255], # [2] -  33,33% : Cyan
        [000, 255, 000], # [3] -  50,00% : Green
        [255, 255, 000], # [4] -  66,66% : Yellow
        [255, 000, 000], # [5] -  83,33% : Red
        [255, 255, 255], # [6] - 100,00% : White
    ]

    numStops = len(stops)
    steps = numStops - 1
    stepWidth = 1.0 / steps

    below = max(int(steps*value), 0)
    above = min(below + 1, steps)

    stepProgress = (value - float(below) * stepWidth) / stepWidth

    return getValueBetweenTwoColors(stepProgress, stops[below], stops[above])

def getValueBetweenTwoColors(value, color1, color2):
    newRed   = int(float(color2[0] - color1[0]) * value + color1[0])
    newGreen = int(float(color2[1] - color1[1]) * value + color1[1])
    newBlue  = int(float(color2[2] - color1[2]) * value + color1[2])

    return [newRed, newGreen, newBlue]

#-------------------------------------------------------------------------
#                             Socket Listener                            #
#-------------------------------------------------------------------------
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('localhost', 12345)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)# Listen for incoming connections
sock.listen(2)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)
        message = ""
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(256).decode()
            print('received "%s"' % data)
            if data:
                print('sending data back to the client')
                message += data
            else:
                print('no more data from', client_address)
                break
        print(message)
        setColorByLabel(message)
    finally:
        # Clean up the connection
        connection.close()
   
