from udp_1 import UDPsocket
import struct
import random
import time
from threading import Timer

header_length = 15
data_length = 2048
header_format = "!B3IH"
data_format = "UTF-8"


class socket(UDPsocket):
    def __init__(self):
        super().__init__()
        self.seq = 0
        self.seq_ack = 0

    def connect(self, address):
        header_1 = struct.pack(header_format, 1, self.seq, self.seq_ack, 0, 0)
        print(header_1)
        self.sendto(header_1, address)
        data, addr_1 = self.recvfrom(2048)
        header_2 = struct.unpack(header_format, data)
        print(header_2)
        if header_2[0] != 5 or header_2[2] != self.seq + 1:
            self.connect()
        self.seq += 1
        self.seq_ack = header_2[1] + 1
        print("line {}".format(29))
        header_3 = struct.pack(header_format, 4, self.seq, self.seq_ack, 0, 0)
        print(header_3)
        self.sendto(header_3, address)
        self.client_address = address
        # send syn; receive syn, ack; send ack
        # your code here
        pass

    def accept(self):
        '''
        相当于这玩意的作用是
        socket本身接受一个,
        发送一个
        接受一个socket,然后new一个socket with recieve 地址返回.
        :return:
        '''
        data, addr = self.recvfrom(2048)
        header_1 = struct.unpack(header_format, data[0:15])
        print(header_1, addr)
        if header_1[0] != 1:
            self.accept()
            return
        self.seq_ack = header_1[1] + 1
        header_2 = struct.pack(header_format, 5, self.seq, self.seq_ack, 0, 0)
        print(header_2)
        self.sendto(header_2, addr)
        data_2, addr_2 = self.recvfrom(2048)
        header_3 = struct.unpack(header_format, data_2[0:15])
        print(header_3, addr_2)
        if header_3[0] != 4 or header_3[2] != self.seq + 1:
            self.accept()
            return
        self.seq += 1
        self.client_address = addr_2
        return self, self.getsockname()

        # receive syn ; send syn, ack; receive ack

        # your code here
        pass

    def close(self):
        # send fin; receive ack; receive fin; send ack
        # your code here
        print("{} {}".format(self.seq, self.seq_ack))
        time.sleep(1200)
        super().close()
        pass

    def recv(self, buffersize=2048):
        print("data in")
        data, addr = self.recvfrom(buffersize)
        header = struct.unpack(header_format, data[0:15])
        print(header, "???")
        self.seq_ack += header[3]
        willreturn = struct.unpack("{}s".format(header[3]), data[15:])[0]
        if check_sum(willreturn) == header[4]:
            self.sendto(struct.pack(header_format, 4, self.seq, self.seq_ack, 0, 0), self.client_address)
        print(willreturn)
        try:
            willreturn = str(data[15:].decode(data_format))
        except AttributeError:
            pass
        print(willreturn)
        print("data recv")
        return willreturn

    def send(self, data):
        try:
            print(data, self.client_address)
        except AttributeError:
            print(data, " without client_address")
        try:
            data = bytes(data.encode(data_format))
        except AttributeError:
            pass
        header = struct.pack(header_format, 4, self.seq, self.seq_ack, len(data), check_sum(data))
        self.sendto(header + data, self.client_address)
        resend = Timer(1.0, self.send, args=[data])
        resend.start()
        data_ack,useless_2 = self.recvfrom(2048)
        print(data_ack,"this is data_ack")
        data_ack_head = struct.unpack(header_format, data_ack[0:15])
        if data_ack_head[0] == 4:
            resend.cancel()
        self.seq += (header[0] & 0x01) + len(data)
        return

    def output_a_long_string(self, a, b):
        print("--------------------------------------------------------------")
        return


def get_control(control):
    return (
        control & 0x01,
        (control & 0x02) >> 1,
        (control & 0x04) >> 2,
    )


def get_random():
    return (int)((2 ** 29 - 1) * random.random())


def check_sum(data):
    sum = 0
    for byte in data:
        sum += byte
    sum = --(sum % 256)
    return sum & 0xFF


print(get_control(7))
print(get_random())
print(check_sum(b'Hello,world'))
print(len(b'Hello,world'))
print(b'Hello,world' + b'wei?zaima')
