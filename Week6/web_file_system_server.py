import asyncio
from http_Response import *
import urllib.parse
import time

path_origin = os.path.dirname(__file__)
server_address = '127.0.0.1'
server_port = 8080
cookie_loca = {}


def delete_spcae(str):
    begin = 0
    end = len(str)
    while str[begin] == " ":
        begin += 1
    while str[end - 1] == " ":
        end -= 1
    return str[begin:end]


async def thinkpeach(reader, writer):
    data = await reader.read(0x3f3f)
    datas = data.decode().split('\r\n')
    msg = datas[0].split(' ')
    print(msg)
    print(datas)
    begin = 0
    length = 0
    use_range = False
    have_cookie = False
    cookie = "0"
    for i in datas:
        if i.split(':')[0] == 'Range':
            # 处理Range
            use_range = True
            range_bytes_1 = delete_spcae(i.split(':')[1])[6:]
            begin = int(range_bytes_1.split('-')[0])
            try:
                length = int(range_bytes_1.split('-')[1])-begin + 1
            except ValueError:
                length = -1
        elif i.split(':')[0] == 'Cookie':
            cookie = str(delete_spcae(i.split(':')[1]))
            have_cookie = True
    print(cookie, "is the cookie")
    method = urllib.parse.unquote(msg[0])  # 避免被空格等干扰
    path = urllib.parse.unquote(msg[1])
    path += ('/' if path[-1] != '/' else '')
    root_path = '.' + path
    willreturn = http_Response(root_path)
    wrong = False
    if data:
        # 本处逻辑为先判断state,然后按类别分别处理,最后统一返回
        if method not in ('GET', 'HEAD'):
            willreturn.set_state_code_msg(405)
            wrong = True
        else:
            if cookie == "0":
                cookie = str(hash(time.time()))
                willreturn.set_headers("Set-Cookie", str(cookie))
            else:
                willreturn.set_headers("Cookie", str(cookie))
            if root_path == './':  # self
                insides = os.listdir()
                willreturn.fill_file_dir(insides)
                if have_cookie:
                    print(cookie_loca)
                    try:
                        last_time = cookie_loca[str(cookie)]
                    except KeyError:
                        last_time = "/"
                    if last_time != "/":
                        willreturn.head_normal[0] = "HTTP/1.0 {} {}\r\n".format(302, "Found")
                        willreturn.set_headers("Location", "{}".format(last_time))
            elif os.path.isdir(root_path):  # isdir
                cookie_loca[cookie] = path
                os.chdir(root_path)
                insides = os.listdir()
                willreturn.fill_file_dir(insides)
                willreturn.dir.insert(0, "<a href=\"{}\">{}</a><br\r\n>".format('../', "../"))
                os.chdir(path_origin)
            elif os.path.isfile(root_path[0:-1]):  # is file
                file_type = mimetypes.guess_type(root_path[0:-1])[0]
                if file_type is None:
                    file_type = 'application/octet-stream'
                willreturn.body_head = []
                willreturn.body_default = []
                willreturn.set_headers('Content-Type', file_type)
                if str(file_type[0:4]) != "text":
                    willreturn.delete_charset('; charset=utf-8\r\n')
                    willreturn.set_headers('Content-Type', file_type+'\r\n')
                willreturn.set_headers('Accept-Ranges', 'bytes')
                willreturn.msg = willreturn.get_file(root_path[0:-1], begin, length, use_range)
            else:
                wrong = True
                willreturn.set_state_code_msg(404)
        if method == 'HEAD' and wrong is False:
            writer.write(willreturn.get_head())
        elif method == 'GET' and wrong is False:
            writer.write(willreturn.get_response())
            #print(willreturn.get_response())
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
