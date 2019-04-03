#!/usr/bin/env python3
import socket
import sys
import os
import inspect

def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)

#append the relative location you want to import from
os.chdir(get_script_dir())
#print(get_script_dir())
#append the relative location you want to import from
sys.path.insert(0, get_script_dir()+'/webcolors/')

#import your module stored in '../webcolors'
import webcolors


if len(sys.argv) <= 1:
    print("No message was provided. Exiting now.")
    sys.exit()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 12345)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)
try:
    
    # Send data
    message = sys.argv[1]
    try:
        message = webcolors.name_to_hex(message)
        print(sys.argv[1] + " is name for hex color. Using hex code " + message + " instead")
    except:
        print(message + " is a literal message.")

    print('sending "%s"' % message)
    sock.sendall(bytearray(message, 'utf-8'))

finally:
    print('closing socket')
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

sys.exit()