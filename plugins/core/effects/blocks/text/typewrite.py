from moviepy.editor import TextClip, CompositeVideoClip

from videopy.compilation import Compilation
from videopy.effect import AbstractEffectFactory, AbstractBlockEffect
from videopy.utils.time import Time
from videopy.utils.utils import get_position_with_padding


class Effect(AbstractBlockEffect):

    def __init__(self, time, configuration):
        super().__init__("typewrite", time)

        self.configuration = configuration

    def render_on_block(self, clip):
        if self.block.get_type() != "text":
            raise ValueError(f"Effect [{self.type}] can only be used with a block of type [text]")

        content = self.block.configuration['content']
        font = self.block.configuration['font']
        size = self.block.configuration['size']
        color = self.block.configuration['color']
        padding = self.block.configuration['padding']
        duration_per_char = self.configuration['duration_per_char']

        clip = TextClip(txt=content, font=font, fontsize=size, color=color)

        if self.time.duration > 0 and duration_per_char == 0:
            duration_per_char = self.time.duration / len(content)
        if self.time.duration == 0 and duration_per_char == 0:
            raise ValueError("You need to provide either a duration or a duration per character")
        if self.time.duration < len(content) * duration_per_char:
            raise ValueError("Duration is too short to display all text")

        txt_width, txt_height = clip.size
        bg_width = txt_width + 2 * padding
        bg_height = txt_height + 2 * padding  # Changed from margin to padding for consistency

        position = get_position_with_padding(
            position=self.block.position,
            clip_size=(self.block.frame.scenario.width, self.block.frame.scenario.height),
            padding_percent=padding,
            bg_width=bg_width,
            bg_height=bg_height
        )

        clips = []
        for i in range(1, len(content) + 1):
            txt_clip = TextClip(content[:i], font=font, fontsize=size, color=color)
            start = self.time.start + (i - 1) * duration_per_char

            txt_clip = txt_clip \
                .set_duration(self.time.duration - start) \
                .set_start(start) \
                .set_position((position[0] + padding, position[1] + padding))

            clips.append(txt_clip)

        return Compilation(
            source=clips,
            mode="compose",
            configuration={"size": (self.block.frame.scenario.width, self.block.frame.scenario.height)}
        )


class EffectFactory(AbstractEffectFactory):
    def from_yml(self, effect_yml):
        configuration = effect_yml.get('configuration', {})
        time = effect_yml.get('time', {})

        return Effect(Time(time.get('start', 0), time.get('duration', 0)), configuration)
