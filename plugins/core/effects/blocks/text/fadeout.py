from videopy.compilation import Compilation
from videopy.effect import AbstractEffectFactory, AbstractBlockEffect
from videopy.utils.logger import Logger
from videopy.utils.time import Time


class Effect(AbstractBlockEffect):

    def __init__(self, time, final_color):
        super().__init__("fadeout", time)

        self.final_color = final_color

    def render_on_block(self, clip):
        return Compilation(clip.crossfadeout(self.time.duration), mode="use_source")


class EffectFactory(AbstractEffectFactory):
    def from_yml(self, effect_yml):
        configuration = effect_yml.get('configuration', {})
        time = effect_yml.get('time', {})

        if time.get('start', 0) > 0:
            Logger.warn(f"The <<time.start>> parameter for <<fadeout>> effect is useless and will be ignored")

        return Effect(Time(time.get('start', 0), time.get('duration', 0)),
                      configuration.get('final_color', [0, 0, 0]))
