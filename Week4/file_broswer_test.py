import asyncio
import os
import mimetypes

head = [b'HTTP/1.0 200 OK\r\n',
        b'Connection: close'
        b'Content-Type:text/html; charset=utf-8\r\n',
        b'\r\n',
        b'<html><body>There just include HEAD message<body></html>\r\n',
        b'\r\n']
err404 = [b'HTTP/1.0 404 Not Found\r\n',
          b'Connection: close'
          b'Content-Type:text/html; charset=utf-8\r\n',
          b'\r\n',
          b'<html><body>404 Not Found<body></html>\r\n',
          b'\r\n']
err405 = [b'HTTP/1.0 405 Method Not Allowed\r\n',
          b'Connection: close'
          b'Content-Type:text/html; charset=utf-8\r\n',
          b'\r\n',
          b'<html><body>405 Method Not Allowed<body></html>\r\n',
          b'\r\n']
list_file = [b'HTTP/1.0 200 OK\r\n',
             b'Connection: close\r\n'
             b'Content-Type:text/html; charset=utf-8\r\n',
             b'\r\n',
             b'<html><head><title>Index of .//</title></head>',
             b'<body bgcolor="white"> ',
             b'<h1>Index of .//</h1><hr> ',
             b'<pre>',

             b'</pre> ',
             b'<hr> ',
             b'\r\n']
list_files = [
    b'HTTP/1.0 200 OK\r\n',
    b'Connection: close\r\n',
    b'Content-Type:text/html; charset=utf-8\r\n',
    b'\r\n',
    b'<html>',
    b'<h1>This is a biaoti</h1>',
    b'<body>',
    b'\r\n',
    b'<p>123132564564</p>\r\n',
    b'\r\n',
    b'</body> ',
    b'</html> ',
    b'\r\n'
]
server_address = '127.0.0.1'
server_port = 11223


def echo():
    echo_loop = asyncio.get_event_loop()
    server = asyncio.start_server(thinkpeach, server_address, server_port, loop=echo_loop)
    serv = echo_loop.run_until_complete(server)
    try:
        echo_loop.run_forever()
    except KeyboardInterrupt:
        pass

    serv.close()
    echo_loop.run_until_complete(serv.wait_closed())
    echo_loop.close()


async def thinkpeach(reader, writer):
    data = await reader.read(11451)
    writer.writelines(list_files)
    await writer.drain()
    writer.close()
    print("this process jump out")
    return


async def get_body(path_list, willreturn):
    dir_path = []
    file_path = []
    for i in path_list:
        if os.path.isfile(i):
            file_path.append("<a href=\"{}\">{}/</a><br>".format(i, i).encode('utf-8'))
        elif os.path.isdir(i):
            dir_path.append("<a href=\"{}\">{}</a><br>".format(i, i).encode('utf-8'))
    for i in dir_path:
        willreturn.insert(-3, i)
    for i in file_path:
        willreturn.insert(-3, i)
    return willreturn


if __name__ == "__main__":
    try:
        echo()
    except KeyboardInterrupt:
        exit()
