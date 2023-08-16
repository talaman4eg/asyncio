#!/usr/bin/python

import telnetlib3, asyncio
import time

class TelnetServer:
    def __init__(self):
        self.loop = None
        self.start_time = time.time()
        self.commands = {
            "status": lambda cmd: "Running, uptime {:.2f} sec".format(time.time() - self.start_time),
            "help": lambda cmd: "Available commands: %s" % (", ".join(self.commands.keys()))
        }
        self.history = []

    def start(self, port=6023):
        self.loop = asyncio.get_event_loop()
        coro = telnetlib3.create_server(port=port, shell=self.shell)
        server = self.loop.run_until_complete(coro)
        self.loop.run_until_complete(server.wait_closed())


    async def shell(self, reader: telnetlib3.TelnetReader, writer: telnetlib3.TelnetWriter):
        writer.write('\r\nCustom telnet server running...')
        writer.write('\r\n> ')
        cmd = ""
        while True:
            inp = await reader.read(1)
            if not inp == "\r":
                cmd += inp
                writer.write(inp)
            else:
                writer.write(inp)
                writer.write("\r\n")
                if cmd:
                    print(cmd)
                    cmd = cmd.strip()
                    parts = cmd.split(" ")
                    if parts[0].strip() in self.commands:
                        res = self.commands[parts[0]](cmd)
                    elif cmd == "quit":
                        writer.write("Later...\r\n")
                        break
                    else:
                        res = "\r\nERROR: Unknown command %s\r\n" % cmd
                    writer.echo(res)
                    await writer.drain()
                    writer.write('\r\n> ')
                    cmd = ""
        writer.close()

if __name__ == "__main__":
    server = TelnetServer()
    server.start()