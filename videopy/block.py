from abc import abstractmethod

from videopy.clip.empty import EmptyClip
from videopy.compilation import Compilation
from videopy.effect import AbstractBlockEffect
from videopy.exception import NoneValueError, DurationNotMatchedError, InvalidTypeError
from videopy.utils.logger import Logger
from videopy.utils.time import Time


class AbstractBlock:
    def __init__(self, time: Time, position, frame):
        if not time.duration:
            raise ValueError("Block duration is required")
        if position is None:
            raise ValueError("Block position is required")

        self.effects = []

        self.position = position
        self.time = time
        self.frame = frame

    def add_effect(self, effect):
        if effect.time.duration > self.time.duration:
            raise DurationNotMatchedError(f"Effect [{effect.type}] duration [{effect.time.duration}] "
                                          f"exceeds block [{self.get_type()}] duration [{self.time.duration}]")
        if effect.time.start > 0 and effect.time.start + effect.time.duration > self.time.duration:
            raise DurationNotMatchedError(f"Effect [{effect.type}] start time [{effect.time.start}] and duration "
                                          f"[{effect.time.duration}] exceed block [{self.get_type()}] "
                                          f"duration [{self.time.duration}]")

        self.effects.append(effect)

    @abstractmethod
    def render(self, clip):
        pass

    @abstractmethod
    def get_type(self):
        pass

    def do_render(self):
        clip = None

        if not self.effects:
            raise ValueError(f"Block of type {self.get_type()} is used without any effects")

        for effect in self.effects:
            if issubclass(type(effect), AbstractBlockEffect):
                compilation = effect.render(self, clip)

                if not issubclass(type(compilation), Compilation):
                    raise InvalidTypeError(f"Effect of type [{effect.type}] did not return a compilation")

                result = self.frame.scenario.get_compiler(compilation.mode).compile(compilation)

                Logger.debug(f"Rendering <<effect>> of type <<{effect.type}>> "
                             f"on <<block>> of type <<{self.get_type()}>>")

                if result is None:
                    raise NoneValueError(f"Compilation of effect [{effect.type}] returned None")
                if isinstance(result, EmptyClip):
                    continue
                if result.duration > self.time.duration:
                    raise DurationNotMatchedError(f"Effect [{effect.type}] duration [{result.duration}] "
                                                  f"does not match the clip duration [{effect.time.duration}]")

                clip = result
            else:
                raise InvalidTypeError(f"Trying to use effect of type [{effect.type}] on block")

        return self.render(clip)


class AbstractBlockFactory:

    @abstractmethod
    def from_yml(self, block_yml, module_yml, frame):
        pass
