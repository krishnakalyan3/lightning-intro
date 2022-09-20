#!/usr/bin/env python3

import lightning as L
from lightning.app.components.python.tracer import TracerPythonScript
from components.gradio_app import ImageServeGradio
from typing import Optional


class RootFlow(L.LightningFlow):
    def __init__(self) -> None:
        super().__init__()
        self.train_work = TracerPythonScript(
            "train.py",
            cloud_compute=L.CloudCompute("gpu"),
        )
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


app = L.LightningApp(RootFlow())