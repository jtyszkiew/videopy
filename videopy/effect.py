from abc import abstractmethod

from videopy.utils.time import Time


class AbstractEffect:
    def __init__(self, effect_type, time):
        if effect_type is None:
            raise ValueError("Effect name is required")
        if not isinstance(time, Time):
            raise ValueError("Effect duration is required")

        self.type = effect_type
        self.time = time


class AbstractFrameEffect(AbstractEffect):
    def __init__(self, effect_type, time):
        super().__init__(effect_type, time)

        self.frame = None

    def render(self, frame, clip=None):
        self.frame = frame

        return self.render_on_frame(clip)

    @abstractmethod
    def render_on_frame(self, clip):
        pass


class AbstractBlockEffect(AbstractEffect):
    def __init__(self, effect_type, time):
        super().__init__(effect_type, time)

        self.block = None

    def render(self, block, clip=None):
        self.block = block

        return self.render_on_block(clip)

    @abstractmethod
    def render_on_block(self, clip):
        pass


class AbstractEffectFactory:

    @abstractmethod
    def from_yml(self, effect_yml):
        pass
