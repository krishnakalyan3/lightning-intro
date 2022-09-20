import lightning as L

class HelloWork(L.LightningWork):
    def __init__(self):
        super().__init__()

    def run(self):
        print("Hello")


class RootFlow(L.LightningFlow):
    def __init__(self):
        super().__init__()
        self.hello_work = HelloWork()
        self.command = None

    def add_command(self, cmd: str):
        print(f"Received cmd: {cmd}")
        self.command = cmd

    def configure_commands(self):
        commands = [
            {"add": self.add_command},
        ]
        return commands

    def run(self):
        if self.command == "hello":
            self.hello_work.run()

app = L.LightningApp(RootFlow())
