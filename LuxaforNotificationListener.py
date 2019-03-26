#!/usr/bin/env python2
from dbus.mainloop.glib import DBusGMainLoop

from gi.repository import GLib
import dbus

import socket

# Create a TCP/IP socket

# Connect the socket to the port where the server is listening
server_address = ('localhost', 12345)
print('connecting to %s port %s' % server_address)

def send(message):
    try:
        # Send data
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_address)
        print('sending "%s"' % message)
        sock.sendall(message)
    finally:
        print('closing socket')
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()


#-------------------------------------------------------------------------
#                          Notification Listener                         #
#-------------------------------------------------------------------------


def notifications(bus, message):
    # print(message)
    keys = ["app_name", "replaces_id", "app_icon", "summary","body", "actions", "hints", "expire_timeout"]
    args = message.get_args_list()
    if len(args) == 8:
        notification = dict([(keys[i], args[i]) for i in range(8)])
        # print("app_name: " + notification["app_name"] + "\nbody: " + notification["body"] + "\nsummary: " + notification["summary"])
        if notification["app_name"] == "notify-send":
            send(notification["body"])
        elif notification['app_name'] == 'tomate-notify-plugin':
            if notification["summary"] == "Pomodoro":
                send('red')
            elif notification["summary"] == "The time is up!" or notification["summary"] == "Session stopped manually":
                send('black')
            elif notification["summary"] == "Long Break" or notification["summary"] == "Short Break":
                send('green')

DBusGMainLoop(set_as_default=True)

session_bus = dbus.SessionBus()
session_bus.add_match_string("type='method_call',interface='org.freedesktop.Notifications',member='Notify',eavesdrop=true")
session_bus.add_message_filter(notifications)

mainloop = GLib.MainLoop()
mainloop.run()
