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
         b'Connection: close'
         b'Content-Type:text/html; charset=utf-8\r\n',
         b'\r\n',
             b'<html><head><title>Index of .//</title></head>',
             b'<body bgcolor="white"> ',
             b'<h1>Index of .//</h1><hr> ',
             b'<pre>',
             b'</pre> ',
             b'<hr> ',
             b'\r\n']
server_address = '127.0.0.1'
server_port = 11451

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
    data = await reader.readline(11451)
    msg = data.decode().split(' ')
    dir_list = os.listdir()
    method = msg[0][0]
    willreturn = list_file.copy()
    if data:
        if method not in ('GET', 'HEAD'):
            writer.writelines(err405)
            writer.close
            return
        path = msg[0][1]
        if path != '/' and path[1:] not in dir_list:
            writer.writelines(err404)
            await writer.drain()
            writer.close()
        else:
            os.chdir(path[1:])
            new_path_list = os.listdir()
            dir_path = []
            file_path = []
            for i in new_path_list:
                if os.path.isfile(i):
                    file_path.append("<a href=\"{}\">{}/</a><br>".format(i,i).encode('utf-8'))
                if os.path.isdir(i):
                    dir_path.append("<a href=\"{}\">{}</a><br>".format(i,i).encode('utf-8'))
            for i in dir_path:
                willreturn.insert(i, -3)
            for i in file_path:
                willreturn.insert(i, -3)



        writer.writelines()
        print(data)
        await writer.drain()
    else:
        writer.close()
        print("this process jump out")
        return


async def collcet():
    list = os.listdir()
    for i in list:
        i = '.'+i
    return list
if __name__ == "__main__":
    try:
        echo()
    except KeyboardInterrupt:
        exit()
