from moviepy.editor import TextClip

from videopy.compilation import Compilation
from videopy.effect import AbstractEffectFactory, AbstractBlockEffect
from videopy.utils.time import Time


class Effect(AbstractBlockEffect):

    def __init__(self, time):
        super().__init__("write", time)

    def render_on_block(self, clip):
        if self.block.get_type() != "text":
            raise ValueError(f"Effect [{self.type}] can only be used with a block of type [text]")

        clip = TextClip(
            txt=self.block.configuration['content'],
            font=self.block.configuration['font'],
            fontsize=self.block.configuration['size'],
            color=self.block.configuration['color']
        )

        position = self.block.get_text_position()

        clip = clip \
            .set_duration(self.time.duration) \
            .set_start(self.block.time.start + self.time.start) \
            .set_position((position[0], position[1]))

        return Compilation(clip, mode="use_source")


class EffectFactory(AbstractEffectFactory):

    def from_yml(self, effect_yml):
        time = effect_yml.get('time', {})

        return Effect(Time(time.get('start', 0), time.get('duration', 5)))
