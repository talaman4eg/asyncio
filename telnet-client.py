import asyncio, telnetlib3

class TelnetClient:
    def __init__(self) -> None:
        self.loop = None
        self.commands = []
        self.responses = {}
        self.quit = False
        self.wait_time = 0.01

    def connect(self, ip, port):
        print("Connecting to %s %s..." % (ip, port))
        self.loop = asyncio.get_event_loop()

    async def shell(self, reader, writer):
        print("Starting shell...")
        outp = await reader.read(1024)
        print(outp)
        while True:
            if len(self.commands) > 0:
                cmd = self.commands.pop(0)
                writer.write(cmd+"\r\n")
                outp = await reader.read(1024)
                self.responses[cmd] = outp
            if self.quit:
                break
            await asyncio.wait(self.wait_time)

        # EOF
        print()

    def quit(self):
        self.quit = True
    

    def cmd(self, cmd) -> str:
        self.commands.append(cmd)
        coro = telnetlib3.open_connection(ip, port, shell=self.shell)
        reader, writer = self.loop.run_until_complete(coro)
        self.loop.run_until_complete(writer.protocol.waiter_closed)
        res = self.responses[cmd]
        del self.responses[cmd]
        return res 

if __name__ == "__main__":
    client = TelnetClient()
    client.connect("localhost", 6023)
    print(client.cmd("status"))
    client.quit()