from videopy.compilation import Compilation
from videopy.effect import AbstractEffectFactory, AbstractFrameEffect
from videopy.utils.logger import Logger
from videopy.utils.time import Time


class Effect(AbstractFrameEffect):

    def __init__(self, time, initial_color):
        super().__init__("fadein", time)

        self.initial_color = initial_color

    def render_on_frame(self, clip):
        return Compilation(clip.crossfadein(self.time.duration), mode="use_source")


class EffectFactory(AbstractEffectFactory):
    def from_yml(self, effect_yml):
        configuration = effect_yml.get('configuration', {})
        time = effect_yml.get('time', {})

        if time.get('start', 0) > 0:
            Logger.warn(f"The <<time.start>> parameter for <<fadein>> effect is useless and will be ignored")

        return Effect(Time(time.get('start', 0), time.get('duration', 0)),
                      configuration.get('initial_color', [0, 0, 0]))
