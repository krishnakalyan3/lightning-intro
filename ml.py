#!/usr/bin/env python3

import lightning as L
from lightning.app.components.python.tracer import TracerPythonScript
from components.gradio_app import ImageServeGradio
from typing import Optional
import os

class TrainingWork(L.LightningWork):
    def __init__(self, cloud_compute: Optional[L.CloudCompute] = None):
        super().__init__(cloud_compute=cloud_compute,  parallel=True)

    def run(self):
        os.system(f"python3 train_pets.py")


class RootFlow(L.LightningFlow):
    def __init__(self) -> None:
        super().__init__()
        self.train_work = TrainingWork(cloud_compute=L.CloudCompute("gpu", shm_size=4096))
        self.gradio_work = ImageServeGradio(L.CloudCompute("cpu"))
        self.command = None

    def app_command(self, cmd: str):
        print(f"Received cmd: {cmd}")
        self.command = cmd

    def configure_commands(self):
        commands = [
            {"av": self.app_command},
        ]
        return commands

    def run(self):
        if self.command == "train":
            self.train_work.run()
        if self.command == "deploy":
            self.gradio_work.run()
        if self.command == "stop":
            self.train_work.stop()
            self.gradio_work.stop()

    def configure_layout(self):
        tab = {"name": "Grado EDA", "content": self.gradio_work}
        return tab

app = L.LightningApp(RootFlow())