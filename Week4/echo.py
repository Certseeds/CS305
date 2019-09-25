import socket
def echo():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 5555))
    sock.listen(10)
    while True:
        print('outer')
        conn, address = sock.accept()
        echo_in(conn, address)
        break
def echo_in(conn,address):
    data ='begin'
    while data != b'' and data != b'exit':
        data = conn.recv(2048)
        conn.send(data)
        print(data)
    conn.close()
if __name__ == "__main__":
    try:
        echo()
    except KeyboardInterrupt:
        exit()