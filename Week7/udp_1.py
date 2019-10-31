from socket import *
import random, time


class UDPsocket(socket):
    def __init__(self):
        super().__init__(AF_INET, SOCK_DGRAM)

    def send(self, data):
        super().send(data)
