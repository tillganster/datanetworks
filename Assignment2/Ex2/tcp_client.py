#!/usr/bin/env python

import socket

'''
CONSTANTS:
'''
TCP_IP = 'snoopy.mpi-inf.mpg.de'
TCP_PORT = 666
MESSAGE = "HELLO.\n".encode()
DOWNLOAD = "DOWNLOAD.\n".encode()
BUFFER_SIZE = 1024


'''
HELPER FUNCTION:
'''
def receive(messagelen):
    # bis buffer leer ist besser
    message = b''
    receivedlen = 0
    while messagelen > receivedlen:
        rec_bytes = s.recv(BUFFER_SIZE)
        receivedlen += len(rec_bytes)
        if receivedlen >= messagelen:
            #we read too much 
            #extract token from recbytes
            last_message = rec_bytes.split(b'TOKEN:')
            #everything in front of TOKEN belongs to the image
            message += last_message[0]
            #extract token from the disconnect phase string
            token = last_message[1].split(b'\n')[0]
            tokenfile = open("token.txt","wb")
            tokenfile.write(token)
            tokenfile.close()
            print(token)
        else:
            message += rec_bytes
        
    return message


'''
MAIN SCRIPT:
'''


#Conecction Phase
print("Connecting...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

# Handshake Phase
hello = s.recv(7)
print("Got response: ",hello)
print("Sending HELLO back..")
s.send(MESSAGE)
command = s.recv(9)
print("GOT: ",command)
s.send(DOWNLOAD)

# Command Phase
filename = s.recv(18).split()[1]
print(filename)
filesizestring = s.recv(22)
print(filesizestring)
filesize = int(filesizestring.split()[1])

# Dowloading phase + Disconnection in receive(num_bytes)
image = receive(filesize)

# Write bytes to file
f = open(filename,"wb")
f.write(image)
f.close()
s.close()
 
print("Connection closed..") 