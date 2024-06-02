from moviepy.editor import CompositeVideoClip
from abc import abstractmethod

from videopy.clip.empty import EmptyClip
from videopy.compilation import Compilation
from videopy.effect import AbstractFrameEffect
from videopy.exception import DurationNotMatchedError, NoneValueError, InvalidTypeError
from videopy.utils.logger import Logger
from videopy.utils.time import Time


class AbstractFrame:
    def __init__(self, time, scenario):
        if not isinstance(time, Time):
            raise ValueError("Step duration is required")

        self.clip = None

        self.blocks = []
        self.effects = []

        self.time = time
        self.scenario = scenario

    @abstractmethod
    def get_type(self):
        pass

    @abstractmethod
    def render(self, relative_start_time):
        pass

    def add_block(self, block):
        if block.time.duration > self.time.duration:
            raise DurationNotMatchedError(f"Block duration [{block.time.duration}] "
                                          f"exceeds frame duration [{self.time.duration}]")
        if block.time.start > 0 and block.time.start + block.time.duration > self.time.duration:
            raise DurationNotMatchedError(f"Block start time [{block.time.start}] and duration [{block.time.duration}] "
                                          f"exceed frame duration [{self.time.duration}]")

        self.blocks.append(block)

    def add_effect(self, effect):
        if effect.time.duration > self.time.duration:
            raise DurationNotMatchedError(f"Effect duration [{effect.time.duration}] "
                                          f"exceeds frame duration [{self.time.duration}]")
        if effect.time.start > 0 and effect.time.start + effect.time.duration > self.time.duration:
            raise DurationNotMatchedError(f"Effect start time [{effect.time.start}] and duration "
                                          f"[{effect.time.duration}] exceed frame duration [{self.time.duration}]")

        self.effects.append(effect)

    def do_render(self, relative_start_time):
        clip = self.render(relative_start_time)

        self.clip = clip

        if clip is None:
            raise NoneValueError(f"Frame of type {self.get_type()} did not return a clip")

        self.scenario.hooks.run_hook("videopy.scenario.frame.effects.before_load", self.effects)

        for effect in self.effects:
            Logger.debug(f"Rendering <<effect>> of type <<{effect.type}>>")

            if issubclass(type(effect), AbstractFrameEffect):
                compilation = effect.render(self, clip)

                if not issubclass(type(compilation), Compilation):
                    raise InvalidTypeError(f"Effect of type [{effect.type}] did not return a compilation")

                result = self.scenario.get_compiler(compilation.mode).compile(compilation)

                if result is None:
                    raise NoneValueError(f"Effect of type [{effect.type}] did not return a clip")
                if isinstance(result, EmptyClip):
                    continue
                if result.duration > self.time.duration:
                    raise DurationNotMatchedError(f"Effect duration [{result.duration}] does not match "
                                                  f"the clip duration [{effect.time.duration}]")

                clip = result
            else:
                raise InvalidTypeError(f"Trying to use effect of type [{effect.type}] on frame")

        for block in self.blocks:
            Logger.debug(f"Rendering <<block>> of type <<{block.get_type()}>>")
            compilation = block.do_render()

            if not issubclass(type(compilation), Compilation):
                raise InvalidTypeError(f"Block of type [{block.get_type()}] did not return a compilation")

            result = self.scenario.get_compiler(compilation.mode).compile(compilation)

            if result is None:
                raise NoneValueError(f"Block of type [{block.get_type()}] did not return a clip")
            if isinstance(result, EmptyClip):
                continue
            if result.duration > self.time.duration:
                raise DurationNotMatchedError(f"Block duration [{result.duration}] does not match "
                                              f"the clip duration [{block.time.duration}]")

            clip = CompositeVideoClip([clip, result])

        return clip


class AbstractFrameFactory:

    @abstractmethod
    def from_yml(self, frame_yml, scenario):
        pass
