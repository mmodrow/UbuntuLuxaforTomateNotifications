#!/usr/bin/env python2
import socket
import sys
import imp

webcolors = imp.load_source('webcolors', './webcolors/webcolors.py')

if len(sys.argv) <= 1:
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
    sock.sendall(message)

finally:
    print('closing socket')
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

sys.exit()