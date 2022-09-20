import lightning as L

class SingleWorkFlow(L.LightningWork):
    def __init__(self):
        super().__init__()

    def run(self):
        print("Hello")


class RootFlow(L.LightningFlow):
    def __init__(self):
        super().__init__()
        self.single_work = SingleWorkFlow()
        self.names = []

    def add_name(self, name: str):
        print(f"Received name: {name}")
        self.names.append(name)

    def configure_commands(self):
        commands = [
            {"add": self.add_name},
        ]
        return commands

    def run(self):
        if "addverb" in self.names:
            self.single_work.run()

app = L.LightningApp(RootFlow())
