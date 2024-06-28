from moviepy.editor import ImageClip

from videopy.compilation import Compilation
from videopy.effect import AbstractEffectFactory, AbstractBlockEffect
from videopy.utils.time import Time

from PIL import Image


class Effect(AbstractBlockEffect):

    def __init__(self, time):
        super().__init__("display", time)

    def render_on_block(self, clip):
        if self.block.get_type() != "image":
            raise ValueError(f"Effect [{self.type}] can only be used with a block of type [image]")

        width = self.block.configuration['width']
        height = self.block.configuration['height']

        if width == -1 or height == -1:
            with Image.open(self.block.configuration['file_path']) as img:
                width = img.width if width == -1 else width
                height = img.height if height == -1 else height

        image = ImageClip(
            self.block.configuration['file_path'],
            duration=self.time.duration,
        )

        image = image.resize(width=width, height=height)
        image = image.set_position(self.block.position)
        image = image.set_duration(self.time.duration if self.time.duration > 0 else self.block.time.duration)

        return Compilation(source=clip, target=image, mode="use_target")


class EffectFactory(AbstractEffectFactory):

    def from_yml(self, effect_yml):
        time = effect_yml.get('time', {})

        return Effect(Time(time.get('start', 0), time.get('duration', 0)))
