from abc import abstractmethod

import typer

from videopy.hooks import Hooks
from videopy.utils.logger import Logger


class AbstractScript:

    def __init__(self, scenario_yml):
        self.scenario_yml = scenario_yml

    def ask(self, question, default=None):
        return typer.prompt(f"{question}", default=default)

    def sayWarn(self, message):
        Logger.warn(message)

    def sayError(self, message):
        Logger.error(message)

    def sayInfo(self, message):
        Logger.info(message)

    def set_width(self, width):
        self.scenario_yml['width'] = width

    def set_height(self, height):
        self.scenario_yml['height'] = height

    def set_fps(self, fps):
        self.scenario_yml['fps'] = fps

    def set_output_path(self, output_path):
        self.scenario_yml['output_path'] = output_path

    def do_run(self, hooks):
        self.scenario_yml['frames'] = []

        self.run(hooks)

    @abstractmethod
    def run(self, hooks: Hooks):
        pass
