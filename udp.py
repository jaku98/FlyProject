import socket, time, sys
import struct
import codecs
from numpy import byte

UDP_IP = "" #"172.23.183.43" git fetch --prune
UDP_PORT = 8000
BUFFER_SIZE = 512

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
data = []
try:
    run = True
    while run:
        data, addr = sock.recvfrom(BUFFER_SIZE) # buffer size
        data = struct.unpack("20f3c", data)
        print("Game Time: ", data[0])

except KeyboardInterrupt:
    print('exit')
    pass #Ctrl+C to terminate

