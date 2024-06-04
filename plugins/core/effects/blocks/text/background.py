from videopy.compilation import Compilation
from videopy.effect import AbstractEffectFactory, AbstractBlockEffect
from videopy.utils import rounded_background
from videopy.utils.time import Time


class Effect(AbstractBlockEffect):

    def __init__(self, time, configuration):
        super().__init__("background", time)

        self.configuration = configuration

    def render_on_block(self, clip):
        txt_width, txt_height = self.block.get_text_size()
        position = self.block.get_text_position()

        bg_width = txt_width + 2 * self.block.configuration['padding']
        bg_height = txt_height + 2 * self.block.configuration['padding']

        bg_color = tuple(self.configuration['background_color'])  # Ensure color is a tuple
        radius = self.configuration['border_radius']
        bg_clip = rounded_background(bg_width, bg_height, bg_color, radius).set_duration(self.time.duration)
        bg_clip = (bg_clip.set_position((position[0] - self.block.configuration['padding'],
                                        position[1] - self.block.configuration['padding']))
                   .set_start(self.block.time.start + self.time.start))

        return Compilation(bg_clip, clip, "compose", {"size": self.block.frame.scenario.size})


class EffectFactory(AbstractEffectFactory):
    def from_yml(self, effect_yml):
        configuration = effect_yml.get('configuration', {})
        time = effect_yml.get('time', {})

        return Effect(Time(time.get('start', 0), time.get('duration', 0)), configuration)
