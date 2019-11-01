from rdt import socket
import time
SERVER_ADDR = "127.0.0.1"
SERVER_PORT = 23579
server = socket()
server.bind((SERVER_ADDR, SERVER_PORT))
count = 0
while True:
    conn, client = server.accept()
    time.sleep(100)
    print("process1 finish")
    while True:
        print("{}-------------------".format(count))
        count += 1
        data = conn.recv(2048)
        print("recieved")
        print(data)
        if not data:
            # 这里指发空包
            print("break now------------------------------------")
            break
        conn.send(data)
        print("1 circle over")
    conn.close()
