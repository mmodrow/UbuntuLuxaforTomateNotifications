#!/usr/bin/env python3
from _dbus_glib_bindings import DBusGMainLoop

from gi.repository import GLib
import dbus

from pyluxafor import LuxaforFlag
from time import sleep

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


def setColor(flagstatus):
    global state, flag
    state = flagstatus
    for ledSet in flagstatus :
        flag.do_static_colour(leds=ledSet[0], r=ledSet[1], g=ledSet[2], b=ledSet[3])


def notifications(bus, message):
    # print(message)
    keys = ["app_name", "replaces_id", "app_icon", "summary","body", "actions", "hints", "expire_timeout"]
    args = message.get_args_list()
    if len(args) == 8:
        notification = dict([(keys[i], args[i]) for i in range(8)])
        # print("app_name: " + notification["app_name"] + "\nbody: " + notification["body"] + "\nsummary: " + notification["summary"])
        if notification["app_name"] == "notify-send":
            if notification["body"] == 'RED' or notification["body"] == 'red' or notification["body"] == 'BUSY':
                setColor(red)
            elif notification["body"] == 'YELLOW' or notification["body"] == 'yellow' or notification["body"] == 'QUIET':
                setColor(yellow)
            elif notification["body"] == 'GREEN' or notification["body"] == 'green' or notification["body"] == 'OPEN':
                setColor(green)
            elif notification["body"] == 'COPS':
                flag.do_pattern(LuxaforFlag.PATTERN_POLICE, 3)
                sleep(3)
                setColor(state)
            elif notification["body"] == 'CONFUSED':
                setColor(confused)
            elif notification["body"] == 'EXTRA_CONFUSED':
                setColor(extra_confused)
            elif notification["body"] == 'BLACK' or notification["body"] == 'black' or notification["body"] == 'OFF':
                setColor(black)
        elif notification['app_name'] == 'tomate-notify-plugin':
            if notification["summary"] == "Pomodoro":
                setColor(red)
            elif notification["summary"] == "The time is up!":
                setColor(black)
            elif notification["summary"] == "Session stopped manually.":
                setColor(black)
            elif notification["summary"] == "Long Break":
                setColor(green)
            elif notification["summary"] == "Short Break":
                setColor(green)


DBusGMainLoop(set_as_default=True)

session_bus = dbus.SessionBus()
session_bus.add_match_string("type='method_call',interface='org.freedesktop.Notifications',member='Notify',eavesdrop=true")
session_bus.add_message_filter(notifications)

mainloop = GLib.MainLoop()
mainloop.run()
