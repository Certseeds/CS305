import struct

v1 = 1
v2 = b'abc'
bytes_2 = struct.pack('i3s', v1, v2)
print(bytes_2)

print(str(1))
Control = 7
seq = 0
seq_ack = 2 ** 32 - 1
length_of_bytes = 2
checksum = 2 ** 16 - 1
Payload = bytes("ab".encode("utf-8"))
formats = "!B3IH{}s".format(str(length_of_bytes))
packet1 = struct.pack(formats, Control, seq, seq_ack, length_of_bytes, checksum, Payload)
print(packet1)
packet2 = struct.unpack("!B3IH", packet1[0:15])
print(packet1[0:15])
print(packet1[15:])
print(packet2)
inside_datas = struct.unpack("{}s".format(str(packet2[3])), packet1[15:])[0]

print("SYN", packet2[0] & 0x01)
print("FIN", (packet2[0] & 0x02) >> 1)
print("ACK", (packet2[0] & 0x04) >> 2)
print("SEQ", packet2[1])
print("SEQ_ACK", packet2[2])
print("LEN", packet2[3])
print("Checksum", packet2[4])
print("datas", inside_datas)
