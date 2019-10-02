import asyncio
import os
import mimetypes
from http_Response import *
import urllib.parse
import pathlib

path_origin = os.path.dirname(__file__)
server_address = '127.0.0.1'
server_port = 11451


async def thinkpeach(reader, writer):
    data = await reader.read(0x3f3f)
    datas = data.decode().split('\r\n')
    msg = datas[0].split(' ')
    method = urllib.parse.unquote(msg[0])
    path = urllib.parse.unquote(msg[1])
    path += ('/' if path[-1] != '/' else '')
    root_path = '.' + path
    willreturn = http_Response(path, root_path)
    wrong = False
    if data:
        if method not in ('GET', 'HEAD'):
            willreturn.set_wrong_msg(405)
            wrong = True
        else:
            if root_path == './':  # self
                insides = os.listdir()
                willreturn.fill_file_dir(insides)
            elif os.path.isdir(root_path):  # isdir
                os.chdir(root_path)
                insides = os.listdir()
                willreturn.fill_file_dir(insides)
                willreturn.dir.insert(0, "<a href=\"{}\">{}</a><br\r\n>".format('../', "../"))
                os.chdir(path_origin)
            elif os.path.isfile(root_path[0:-1]):  # is file
                file_type = mimetypes.guess_type(root_path[0:-1])[0]
                if file_type is None:
                    file_type = 'application/octet-stream'
                    willreturn.set_headers('Accept-Ranges', 'bytes')
                willreturn.body_head = []
                willreturn.set_headers('Content-Type', file_type)
                willreturn.set_headers('Content-Length', str(os.path.getsize(root_path[0:-1])))
                willreturn.msg = willreturn.get_file(root_path[0:-1])
            else:
                wrong = True
                willreturn.set_wrong_msg(404)
        if method == 'HEAD' and wrong is False:
            writer.write(willreturn.get_head())
        elif method == 'GET' and wrong is False:
            writer.write(willreturn.get_response())
        else:
            writer.write(willreturn.get_response_wrong())
        try:
            await writer.drain()
        except BrokenPipeError:
            pass
        writer.close()


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


if __name__ == "__main__":
    try:
        echo()
    except KeyboardInterrupt:
        exit()
