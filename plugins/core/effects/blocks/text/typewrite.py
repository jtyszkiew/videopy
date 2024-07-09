from moviepy.editor import TextClip, CompositeVideoClip

from videopy.compilation import Compilation
from videopy.effect import AbstractEffectFactory, AbstractBlockEffect
from videopy.module import AbstractModuleDefinition
from videopy.utils.time import Time


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
        duration_per_char = self.configuration['duration_per_char']

        if self.time.duration > 0 and duration_per_char == 0:
            duration_per_char = self.time.duration / len(content)
        if self.time.duration == 0 and duration_per_char == 0:
            raise ValueError("You need to provide either a duration or a duration per character")
        if self.time.duration < len(content) * duration_per_char:
            raise ValueError("Duration is too short to display all text")

        position = self.block.get_text_position()

        clips = []
        for i in range(1, len(content) + 1):
            txt_clip = TextClip(content[:i], font=font, fontsize=size, color=color, bg_color='transparent')
            start = self.block.time.start + self.time.start + (i - 1) * duration_per_char

            txt_clip = txt_clip \
                .set_duration(self.time.duration - start) \
                .set_start(start) \
                .set_position((position[0], position[1]))

            clips.append(txt_clip)

        composite_clip = CompositeVideoClip(clips, size=self.block.frame.scenario.size)

        return Compilation(source=composite_clip, mode="use_source")


class EffectFactory(AbstractEffectFactory):
    def from_yml(self, effect_yml):
        configuration = effect_yml.get('configuration', {})
        time = effect_yml.get('time', {})

        return Effect(Time(time.get('start', 0), time.get('duration', 0)), configuration)


class TextTypewriteEffectModuleDefinition(AbstractModuleDefinition):
    PLUGIN_PREFIX = "plugins.core"
    PLUGIN_PREFIX_INDEX = PLUGIN_PREFIX.replace(".", "")

    EXAMPLE_DURATION = 1

    @staticmethod
    def get_description():
        return "Type write text on a block. This is a base effect if you want to display text."

    @staticmethod
    def get_configuration():
        return {
            "duration_per_char": {
                "type": "float",
                "description": "Duration in seconds to display each character",
                "default": 0,
                "required": False
            }
        }

    @staticmethod
    def get_renders_on() -> dict:
        return {
            "block": ["text"]
        }

    @staticmethod
    def get_examples() -> list:
        return [
            {
                "name": "Typewrite Effect On Text Block",
                "description": "This example shows how to add typewrite effect on text block.",
                "scenario": {
                    "width": 640, "height": 240, "fps": 24,
                    "frames": [
                        {
                            "type": f"{TextTypewriteEffectModuleDefinition.PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": TextTypewriteEffectModuleDefinition.EXAMPLE_DURATION},
                            "configuration": {"file_path": "example/assets/image/1.jpg"},
                            "effects": [
                                {"type": f"{TextTypewriteEffectModuleDefinition.PLUGIN_PREFIX}.effects.frames.resize",
                                 "configuration": {"mode": "center_crop"}}],
                            "blocks": [
                                {
                                    "type": f"{TextTypewriteEffectModuleDefinition.PLUGIN_PREFIX}.blocks.text",
                                    "time": {"duration": TextTypewriteEffectModuleDefinition.EXAMPLE_DURATION},
                                    "position": ["center", "center"],
                                    "configuration": {"content": "Hello, World!", "color": "white"},
                                    "effects": [{
                                        "type": f"{TextTypewriteEffectModuleDefinition.PLUGIN_PREFIX}.effects.blocks.text.typewrite",
                                        "time": {"duration": TextTypewriteEffectModuleDefinition.EXAMPLE_DURATION},
                                    }]
                                }
                            ]
                        }
                    ]
                },
            }
        ]
