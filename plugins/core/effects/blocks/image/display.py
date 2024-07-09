from moviepy.editor import ImageClip

from videopy.compilation import Compilation
from videopy.effect import AbstractEffectFactory, AbstractBlockEffect
from videopy.module import AbstractModuleDefinition
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


class ImageDisplayEffectModuleDefinition(AbstractModuleDefinition):
    PLUGIN_PREFIX = "plugins.core"
    PLUGIN_PREFIX_INDEX = PLUGIN_PREFIX.replace(".", "")

    EXAMPLE_DURATION = 1

    @staticmethod
    def get_description():
        return "This is basic effect for displaying image."

    @staticmethod
    def get_configuration():
        return {}

    @staticmethod
    def get_renders_on() -> dict:
        return {
            "block": ["image"]
        }

    @staticmethod
    def get_examples():
        return [
            {
                "name": "Write Effect On Text Block",
                "description": "This is basic effect to display any text. It will write the text on the block.",
                "tips": [
                    "No configuration is accepted, as this effect inherits the configuration from "
                    f"[{ImageDisplayEffectModuleDefinition.PLUGIN_PREFIX}.blocks.text](#{ImageDisplayEffectModuleDefinition.PLUGIN_PREFIX_INDEX}blockstext).",
                ],
                "scenario": {
                    "width": 640, "height": 240, "fps": 24,
                    "frames": [
                        {
                            "type": f"{ImageDisplayEffectModuleDefinition.PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": ImageDisplayEffectModuleDefinition.EXAMPLE_DURATION},
                            "configuration": {"file_path": "example/assets/image/1.jpg"},
                            "effects": [
                                {"type": f"{ImageDisplayEffectModuleDefinition.PLUGIN_PREFIX}.effects.frames.resize",
                                 "configuration": {"mode": "center_crop"}}],
                            "blocks": [
                                {
                                    "type": f"{ImageDisplayEffectModuleDefinition.PLUGIN_PREFIX}.blocks.image",
                                    "time": {"duration": ImageDisplayEffectModuleDefinition.EXAMPLE_DURATION},
                                    "position": ["center", "center"],
                                    "configuration": {"file_path": "example/assets/image/logo.png", "width": 100,
                                                      "height": 100},
                                    "effects": [{
                                        "type": f"{ImageDisplayEffectModuleDefinition.PLUGIN_PREFIX}.effects.blocks.image.display",
                                        "time": {"duration": ImageDisplayEffectModuleDefinition.EXAMPLE_DURATION}
                                    }]
                                }
                            ]
                        }
                    ]
                },
            }
        ]
