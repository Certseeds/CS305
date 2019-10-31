from rdt import socket

SERVER_ADDR = "127.0.0.1"
SERVER_PORT = 23579
server = socket()
server.bind((SERVER_ADDR, SERVER_PORT))
while True:
    conn, client = server.accept()
    print("process1 finish")
    while True:
        data = conn.recv(2048)
        print("recieved")
        print(data)
        if not data:
            break
        conn.send(data)
        print("1 circle over")
    conn.close()
