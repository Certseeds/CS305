import struct
import random
import socket
import time

def check_sum(data):
    sum = 0
    for byte in data:
        print(byte)
        sum += byte
    print(sum)
    sum = --(sum % 256)
    print(sum == 0)
    return sum & 0xFF

def produce_check_sum(format, bits, seq, seq_ack, data_str):
    try:
        data_bytes = bytes(data_str.encode("UTF-8"))
    except AttributeError:
        pass
    header = struct.pack(format, bits, seq, seq_ack, len(data_str), 0)
    header +=  data_bytes
    check_data = check_sum(header)
    willreturn = struct.pack(format, bits, seq, seq_ack, len(data_str), 256 - check_data)
    willreturn +=  data_bytes
    print("this is willreturn",willreturn)
    print("this is checksum of willreturn",check_sum(willreturn))
    return willreturn

def echo():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 5555))
    sock.listen(10)
    while True:
        conn, address = sock.accept()
        while True:
            data = conn.recv(2048)
            if data and data != b'exit\r\n':
                conn.send(data)
                print(data)
            else:
                conn.close()
            break


if __name__ == "__main__":
    try:
        pass
        # echo()
    except KeyboardInterrupt:
        pass
socks = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socks.bind(('127.0.0.1', 5555))
time_now = time.time()
for i in range(0,100,1):
    socks.sendto(b'J7D7t1wB9jdpD5ifeb9SBVAy4jrxb6cEXLKhxBQRI5EZOxbH9IcD4unhRGWHKuClXinCSUeKZGRgqKWRInJilOsteqpOsDXeiR34BI3gq2QaAya3ZDiQ8ongdBN6srGDXHs8eU6yJGvHyDkTGsSR7ux1nNHb1rfMA5pP6vBIIBtIfGu6xWWPNRorlBTarb7TLNus6pPnh1haybj33mtv3bFbCIJMuCExGkHRtWNEsFngCjfhRCqTQxKPreiUfFRSiunLEYBG49KGRCDThKSRW7InmZsO1gU1FF9oPput17bYmfT1swNH5Ca9g1LRitEmDkxaoEhxCRfCNNxjMFVRiyaw6VZygOgkxMAjfFCBsvkzL88L5FREXrniqxIDi2L3kbEH6TLkv7WbXhm6nGDf3Up2bZOBd7idYWVy87iH1OacEle7PiBGCaj3STLBDZ54pLggzeXWAAtxcrS9AZyPoZep6mpDsuk2sv6uN5WuvevBduKmHpskmaUc2mZebUzIW5y9FTs2'\
                 ,('127.0.0.1',11451))
print(time.time()- time_now)