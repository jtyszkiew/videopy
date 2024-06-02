from moviepy.editor import CompositeVideoClip, TextClip

from videopy.compilation import Compilation
from videopy.effect import AbstractEffectFactory, AbstractBlockEffect
from videopy.utils import rounded_background
from videopy.utils.time import Time
from videopy.utils.utils import get_position_with_padding


class Effect(AbstractBlockEffect):

    def __init__(self, time, configuration):
        super().__init__("background", time)

        self.configuration = configuration

    def render_on_block(self, clip):
        content = self.block.configuration['content']
        font = self.block.configuration['font']
        size = self.block.configuration['size']
        color = self.block.configuration['color']
        padding = self.configuration['padding']

        txt_width, txt_height = TextClip(txt=content, font=font, fontsize=size, color=color).size

        # Internal padding for text
        bg_width = txt_width + 2 * padding
        bg_height = txt_height + 2 * padding  # Changed from margin to padding for consistency

        position = get_position_with_padding(
            position=self.block.position,
            clip_size=(self.block.frame.scenario.width, self.block.frame.scenario.height),
            padding_percent=padding,
            bg_width=bg_width,
            bg_height=bg_height
        )

        bg_color = tuple(self.configuration['background_color'])  # Ensure color is a tuple
        radius = self.configuration['border_radius']
        bg_clip = rounded_background(bg_width, bg_height, bg_color, radius).set_duration(self.time.duration)
        bg_clip = bg_clip.set_position(position).set_start(self.time.start)

        return Compilation(bg_clip, clip, "compose",
                           {"size": (self.block.frame.scenario.width, self.block.frame.scenario.height)})


class EffectFactory(AbstractEffectFactory):
    def from_yml(self, effect_yml):
        configuration = effect_yml.get('configuration', {})
        time = effect_yml.get('time', {})

        return Effect(Time(time.get('start', 0), time.get('duration', 0)), configuration)
