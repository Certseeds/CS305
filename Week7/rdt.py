from udp import UDPsocket
import struct
import random
import time
from threading import Timer

header_length = 15
data_length = 2048
header_format = "!B3IH"
data_format = "UTF-8"
SYN_bit = 1
FIN_bit = 2
ACK_bit = 4
Reset_bit = 8


class socket(UDPsocket):
    def __init__(self):
        super().__init__()
        self.seq = 0
        self.seq_ack = 0

    def connect(self, address):
        self.setblocking(False)
        self.client = True
        header_1 = produce_packets(header_format, SYN_bit, self.seq, self.seq_ack)
        self.sendto(header_1, address)
        print("send syn finish")
        time.sleep(1)
        try:
            data, addr_1 = self.recvfrom(data_length)
        except BlockingIOError:
            time.sleep(1)
            print("line 34")
            self.connect(address)
            return
        except TypeError:
            time.sleep(1)
            print("line 39")
            self.connect(address)
            return
        print("recieve syn ack finish")
        header_2 = struct.unpack(header_format, data[0:15])
        if header_2[0] != SYN_bit + ACK_bit or header_2[2] != self.seq + 1 or check_sum(data):
            time.sleep(1)
            print("line 46")
            self.connect(address)
            return
        self.seq += 1
        self.seq_ack = header_2[1] + 1
        header_3 = produce_packets(header_format, ACK_bit, self.seq, self.seq_ack)
        self.sendto(header_3, address)
        print("send ack finish")
        self.client_address = address
        # send syn; receive syn, ack; send ack
        # your code here
        self.setblocking(True)
        print("coneect finish ")
        return

    def accept(self):
        print("now is {}".format(time.time()))
        self.setblocking(True)
        self.client = False
        '''
        相当于这玩意的作用是
        socket本身接受一个,
        发送一个
        接受一个socket,然后new一个socket with recieve 地址返回.
        :return:
        '''
        try:
            data, addr = self.recvfrom(data_length)
        except TypeError:
            print("line 72")
            self.accept()
            return
        print("recieve syn data")
        self.setblocking(False)
        header_1 = struct.unpack(header_format, data[0:15])
        if header_1[0] != 1 or check_sum(data):
            print(check_sum(data))
            print("line 82")
            self.accept()
            return
        self.seq_ack = header_1[1] + 1
        header_2 = produce_packets(header_format, SYN_bit + ACK_bit, self.seq, self.seq_ack)
        self.sendto(header_2, addr)
        print("send syn,ack finish")
        time.sleep(1)
        try:
            data_2, addr_2 = self.recvfrom(data_length)
        except BlockingIOError:
            print("line 89")
            self.accept()
            return
        except TypeError:
            print("line 93")
            self.accept()
            return
        print("recieve ack finish")
        header_3 = struct.unpack(header_format, data_2[0:15])
        print( header_3[0])
        print(header_3[2])
        print(self.seq+1)
        if header_3[0] != ACK_bit or header_3[2] != self.seq + 1:
            print("line 102")
            self.accept()
            return
        self.seq += 1
        self.client_address = addr_2
        self.setblocking(True)
        print("accept finish")
        return self, self.getsockname()

        # receive syn ; send syn, ack; receive ack

        # your code here

    def close(self):
        # send fin; receive ack; receive fin; send ack
        # your code here
        if self.client:
            self.send("")
            self.sendto(struct.pack(header_format, 2, self.seq, self.seq_ack, 0, 0), self.client_address)
            header_2, useless_address_3 = self.recvfrom(data_length)
            header_2_unpack = struct.unpack(header_format, header_2[0:15])
            if header_2_unpack[0] != 4 or self.seq + 1 != header_2_unpack[2]:
                return
            header_3, useless_address_4 = self.recvfrom(data_length)
            header_3_unpack = struct.unpack(header_format, header_3[0:15])
            if header_3_unpack[0] != 2 or self.seq != header_3_unpack[2]:
                return
            self.sendto(struct.pack(header_format, 4, self.seq, header_3_unpack[1] + 1, 0, 0), self.client_address)
            print("{} {}".format(self.seq, self.seq_ack))
            time.sleep(1)
            super().close()
        else:
            print("server begin close")
            header_1, useles_address_2 = self.recvfrom(data_length)
            header_1_unpack = struct.unpack(header_format, header_1[0:15])
            if header_1_unpack[0] != 2:
                return
            self.sendto(struct.pack(header_format, 4, header_1_unpack[2], header_1_unpack[1] + 1, 0, 0), self.client_address)
            time.sleep(1)
            self.sendto(struct.pack(header_format, 2, self.seq, header_1_unpack[1], 0, 0), self.client_address)
            header_4, useless_address_5 = self.recvfrom(data_length)
            header_4_unpack = struct.unpack(header_format, header_4[0:15])
            if header_4_unpack[0] != 4 or header_4_unpack[2] != self.seq + 1:
                return
            print("{} {}".format(self.seq, self.seq_ack))
            time.sleep(1)
            self.seq = 0
            self.seq_ack = 0
        return

    def recv(self, buffersize=data_length):
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
        header = struct.pack(header_format, ACK_bit, self.seq, self.seq_ack, len(data), check_sum(data))
        self.sendto(header + data, self.client_address)
        resend = Timer(1.0, self.send, args=[data])
        resend.start()
        data_ack, useless_2 = self.recvfrom(data_length)
        print(data_ack, "this is data_ack")
        data_ack_head = struct.unpack(header_format, data_ack[0:15])
        print(data_ack_head[2], self.seq)
        if data_ack_head[0] == 4 and data_ack_head[2] == self.seq + len(data):
            resend.cancel()
        self.seq += (header[0] & 0x01) + len(data)
        return

    def output_a_long_string(self, a, b):
        print("--------------------------------------------------------------")
        return


def produce_packets(formats, bits, seq, seq_ack, data_str=""):
    try:
        data_bytes = bytes(data_str.encode(data_format))
    except AttributeError:
        pass
    header = struct.pack(formats, bits, seq, seq_ack, len(data_str), 0)
    header += data_bytes
    check_data = check_sum(header)
    willreturn = struct.pack(formats, bits, seq, seq_ack, len(data_str), 256 - check_data)
    willreturn += data_bytes
    return willreturn


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
