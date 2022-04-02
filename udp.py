import socket, struct

UDP_IP = "192.168.8.101" #"172.23.183.43"
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
        print("Game Time: ", data[0], " x: ", data[1], " y: ", data[2], " z: ", data[3])
except KeyboardInterrupt:
    print('exit')
    pass #Ctrl+C to terminate