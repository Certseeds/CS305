import asyncio
async def thinkpeach(reader, writer):
    data = await reader.readline()
    '''message = data.decode().split(' ')
    print(data)
    if data == b'\r\n':
       break
    writer.writelines([ b'HTTP/1.0 200 OK\r\n',
                                 b'Content-Type:text/html; charset=utf-8\r\n,'
                                  b'Connection: close\r\n', b'\r\n',
                                  b'<html><body>Hello World!<body></html>\r\n', b'\r\n' ])
    await writer.drain()
    writer.close()'''
    message = data.decode()
    addr = writer.get_extra_info('peername')
    writer.weiter(data)
    await writer.drain()
    writer.close()

# if __name__ == "__main__":
async def main():
    # loop = asyncio.get_event_loop()
    server_address='127.0.0.1'
    server_port = 1145
    server = await asyncio.start_server(thinkpeach, server_address, server_port)
    # server = loop.run_until_complete(coro)
    print("server begin to run")

    async with server:
        await server.serve_forever()

asyncio.run(main)
''' try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
loop.close()'''
