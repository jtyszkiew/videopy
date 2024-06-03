from abc import abstractmethod

import typer

from videopy.hooks import Hooks
from videopy.utils.logger import Logger


class AbstractScript:

    def __init__(self, scenario_yml):
        self.scenario_yml = scenario_yml

    def ask(self, question, default=None):
        return typer.prompt(f"{question}", default=default)

    def say_warn(self, message):
        Logger.warn(message)

    def say_error(self, message):
        Logger.error(message)

    def say_info(self, message):
        Logger.info(message)

    def set_width(self, width):
        self.scenario_yml['width'] = width

    def set_height(self, height):
        self.scenario_yml['height'] = height

    def set_fps(self, fps):
        self.scenario_yml['fps'] = fps

    def set_output_path(self, output_path):
        self.scenario_yml['output_path'] = output_path

    def do_run(self, hooks, data):
        self.scenario_yml['frames'] = []

        self.run(hooks, data)

    @abstractmethod
    def run(self, hooks: Hooks, data: dict):
        pass

    @abstractmethod
    def collect_data(self, data):
        pass
