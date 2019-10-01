import asyncio
import os
import mimetypes
import urllib.parse
import codecs

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
             b'Connection: close\r\n',
             b'Content-Type:text/html; charset=utf-8\r\n',
             b'\r\n',
             b'<!DOCTYPE html>\r\n<html><head><title>Index of .//</title></head>\r\n',
             b'<body bgcolor="white"> \r\n',
             b'<h1>Index of .//</h1><hr>\r\n ',
             b'<pre>\r\n',
             b'</pre>\r\n ',
             b'<hr> \r\n',
             b'\r\n']
files = [b'HTTP/1.0 200 OK\r\n',
         b'Connection: close\r\n',
         b'Content-Type:text/html; charset=utf-8\r\n',
         b'\r\n',
         b'\r\n']
image = [b'HTTP/1.0 200 OK\r\n',
         b'Connection: close\r\n',
         b'Content-Type:text/html; charset=utf-8\r\n',
         b'\r\n',
         b'\r\n']
path_origin = os.path.dirname(__file__)
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
    print("comes!!!")
    data = await reader.read(11451)
    datas = data.decode().split('\r\n')
    msg = datas[0].split(' ')
    method = msg[0]
    path = msg[1]
    if path[len(path)-1]!='/':
        path += '/'
    for i in datas:
       print(i)
    willreturn = list_file.copy()
    if data:
        print(os.getcwd())
        if method not in ('GET', 'HEAD'):
            willreturn = err405
        else:
            if path == '/':  # 本目录
                print("本目录")
                dir_list = os.listdir()
                await get_body(dir_list, willreturn, '')
            elif os.path.isdir(path[1:]):
                domains = path.split("/")
                print("是目录")
                print(path[0:len(path) - len(domains[len(domains)-1])])
                os.chdir('.'+path)
                new_path_list = os.listdir()
                willreturn[4] = "<!DOCTYPE html>\r\n<html><head><title>Index of {}</title></head>".format(path[1:]).encode('utf-8')
                willreturn[6] = "<h1>Index of {}</h1><hr>".format(path[1:]).encode('utf-8')
                willreturn.insert(-3, "<a href=\"{}\">{}</a><br>\r\n".format(path[0:len(path) - len(domains[len(domains)-2]) - 1], "../").encode('utf-8'))
                await get_body(new_path_list, willreturn, path)
                os.chdir(path_origin)
            elif os.path.isfile(path[1:-1]):
                path = path[0:-1]
                print("是文件")
                file = open('.'+path, 'r', encoding='utf-8')
                willreturn = files.copy()
                file_type = mimetypes.guess_type(path[1:])[0]
                if file_type.split("/")[0] == "audio":
                    willreturn[2] = "Content-Type:{}; charset=utf-8; \r\nContent-Length:{}\r\n".format(file_type, os.path.getsize(path[1:])).encode('utf-8')
                    #willreturn.insert(-2, "<embed height=\"50\" width=\"100\" src=\"{}\"\r\n>".format(path[1:]).encode('utf-8'))
                    willreturn.insert(-2, "<audio controls=\"controls\" height=\"100\" width=\"100\" autoplay=\"autoplay\">".encode('utf-8'))
                    willreturn.insert(-2, "<source src=\"{}\" type=\"{}\">".format(path[1:], file_type).encode('utf-8'))
                    willreturn.insert(-2, "</audio>".encode('utf-8'))
                # elif file_type.split("/")[0] == "vedio":
                # elif file_type.split("/")[0] == "audio":
                else:
                    willreturn[2] = "Content-Type:{}; charset=utf-8\r\n ".format(file_type).encode('utf-8')
                    willreturn.insert(2, "Content-Length:{};\r\n".format(os.path.getsize(path[1:])).encode('utf-8'))
                    willreturn.insert(-1, "{}\r\n".format(file.read()).encode('utf-8'))
            else:  # 什么也不是
                print("啥也不是")
                willreturn = err404
        if method == 'HEAD':
            writer.writelines(willreturn[0:4])
        else:
            writer.writelines(willreturn)
        await writer.drain()
        writer.close()
        print("now it is in here")
        return
    else:
        writer.close()
        print("this process jump out")
        return


async def get_body(path_list, willreturn, adden):
    dir_path = []
    file_path = []
    for i in path_list:
        print(i)
        if os.path.isfile(i):
            file_path.append("<a href=\"{}\">{}</a><br\r\n>".format((adden + i), i).encode('utf-8'))
        elif os.path.isdir(i):
            dir_path.append("<a href=\"{}\">{}</a><br>\r\n".format((adden + i+"/"), i+"/").encode('utf-8'))
    for i in file_path:
        willreturn.insert(-3, i)
    for i in dir_path:
        willreturn.insert(-3, i)
    return willreturn


if __name__ == "__main__":
    try:
        echo()
    except KeyboardInterrupt:
        exit()
