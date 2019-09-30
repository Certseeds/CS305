import asyncio


def echo():
    server_address = '127.0.0.1'
    server_port = 5555
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
    while True:
        data = await reader.read(11451)
        datas = data.decode().split('\r\n')
        print(datas[0].split(' ')[0] in ('GET', 'HEAD'))
        print(datas[0].split(' ')[1])
        if data and data != b'exit':
            writer.write(data)
            for i in datas:
                print(i)
            await writer.drain()
        else:
            writer.close()
            print("this process jump out")
            return


if __name__ == "__main__":
    try:
        echo()
    except KeyboardInterrupt:
        exit()
