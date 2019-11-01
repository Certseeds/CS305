from rdt import socket
import time
SERVER_ADDR = "127.0.0.1"
SERVER_PORT = 23579
MESSAGE = "Hello,World"
BUFFer_size = 2048
client = socket()
client.connect((SERVER_ADDR, SERVER_PORT))
time.sleep(100)
client.send(MESSAGE)
print("send finish")
data = client.recv(BUFFer_size)
print("recieve finish")
print(data)
print(data == MESSAGE)
assert data == MESSAGE
print("1 circle over")

client.close()