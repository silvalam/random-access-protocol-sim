# Project 2 Part 2
# Authors: Sylvia Lam, Brian LaBar

import random
from socket import *

def udpserver():
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', 12000))
    while True:
        rand = random.randint(0, 10)
        message, address = serverSocket.recvfrom(1024)
        message = message.upper()
        if rand < 4:
            continue
        else:
            serverSocket.sendto(message, address)


