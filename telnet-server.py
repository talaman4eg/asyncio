#!/usr/bin/python

import telnetlib3, asyncio

class TelnetServer:
    def __init__(self):
        self.loop = None

    async def start(self):
        self.loop = asyncio.get_event_loop()
        coro = telnetlib3.create_server(port=6023, shell=self.shell)
        server = self.loop.run_until_complete(coro)
        self.loop.run_until_complete(server.wait_closed())


    async def shell(self, reader, writer):
        writer.write('\r\nWould you like to play a game? ')
        inp = await reader.read(1)
        if inp:
            writer.echo(inp)
            writer.write('\r\nThey say the only way to win '
                        'is to not play at all.\r\n')
            await writer.drain()
        writer.close()
