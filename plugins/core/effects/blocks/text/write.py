from moviepy.editor import TextClip

from videopy.compilation import Compilation
from videopy.effect import AbstractEffectFactory, AbstractBlockEffect
from videopy.module import AbstractModuleDefinition
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


class TextWriteEffectModuleDefinition(AbstractModuleDefinition):
    PLUGIN_PREFIX = "plugins.core"
    PLUGIN_PREFIX_INDEX = PLUGIN_PREFIX.replace(".", "")

    EXAMPLE_DURATION = 0.1

    @staticmethod
    def get_description():
        return "Write text on a block. This is a base effect if you want to display text."

    @staticmethod
    def get_configuration():
        return {}

    @staticmethod
    def get_renders_on() -> dict:
        return {
            "block": ["text"]
        }

    @staticmethod
    def get_examples():
        return [
            {
                "name": "Write Effect On Text Block",
                "description": "This is basic effect to display any text. It will write the text on the block.",
                "tips": [
                    "No configuration is accepted, as this effect inherits the configuration from "
                    f"[{TextWriteEffectModuleDefinition.PLUGIN_PREFIX}.blocks.text](#{TextWriteEffectModuleDefinition.PLUGIN_PREFIX_INDEX}blockstext).",
                ],
                "scenario": {
                    "width": 640, "height": 240, "fps": 24,
                    "frames": [
                        {
                            "type": f"{TextWriteEffectModuleDefinition.PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": TextWriteEffectModuleDefinition.EXAMPLE_DURATION},
                            "configuration": {"file_path": "example/assets/image/1.jpg"},
                            "effects": [
                                {"type": f"{TextWriteEffectModuleDefinition.PLUGIN_PREFIX}.effects.frames.resize",
                                 "configuration": {"mode": "center_crop"}}],
                            "blocks": [
                                {
                                    "type": f"{TextWriteEffectModuleDefinition.PLUGIN_PREFIX}.blocks.text",
                                    "time": {"duration": TextWriteEffectModuleDefinition.EXAMPLE_DURATION},
                                    "position": ["center", "center"],
                                    "configuration": {"content": "Hello, World!", "color": "white"},
                                    "effects": [{
                                        "type": f"{TextWriteEffectModuleDefinition.PLUGIN_PREFIX}.effects.blocks.text.write",
                                        "time": {"duration": TextWriteEffectModuleDefinition.EXAMPLE_DURATION}
                                    }]
                                }
                            ]
                        }
                    ]
                },
            }
        ]
