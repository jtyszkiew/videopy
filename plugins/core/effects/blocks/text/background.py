from videopy.compilation import Compilation
from videopy.effect import AbstractEffectFactory, AbstractBlockEffect
from videopy.module import AbstractModuleDefinition
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

        bg_color = tuple(self.configuration['color'])  # Ensure color is a tuple
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


class TextBackgroundEffectModuleDefinition(AbstractModuleDefinition):
    PLUGIN_PREFIX = "plugins.core"
    PLUGIN_PREFIX_INDEX = PLUGIN_PREFIX.replace(".", "")

    EXAMPLE_DURATION = 0.1

    @staticmethod
    def get_description():
        return "Write text on a block. This is a base effect if you want to display text."

    @staticmethod
    def get_configuration():
        return {
            "color": {
                "description": "The color of the background.",
                "type": "str",
                "default": [0, 0, 0],
                "required": False
            },
            "opacity": {
                "description": "The opacity of the background.",
                "type": "float",
                "default": 1,
                "required": False
            },
            "border_radius": {
                "description": "The border radius of the background.",
                "type": "float",
                "default": 10,
                "required": False
            }
        }

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
                    f"[{TextBackgroundEffectModuleDefinition.PLUGIN_PREFIX}.blocks.text](#{TextBackgroundEffectModuleDefinition.PLUGIN_PREFIX_INDEX}blockstext).",
                ],
                "scenario": {
                    "width": 640, "height": 240, "fps": 24,
                    "frames": [
                        {
                            "type": f"{TextBackgroundEffectModuleDefinition.PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": TextBackgroundEffectModuleDefinition.EXAMPLE_DURATION},
                            "configuration": {"file_path": "example/assets/image/1.jpg"},
                            "effects": [
                                {"type": f"{TextBackgroundEffectModuleDefinition.PLUGIN_PREFIX}.effects.frames.resize",
                                 "configuration": {"mode": "center_crop"}}],
                            "blocks": [
                                {
                                    "type": f"{TextBackgroundEffectModuleDefinition.PLUGIN_PREFIX}.blocks.text",
                                    "time": {"duration": TextBackgroundEffectModuleDefinition.EXAMPLE_DURATION},
                                    "position": ["center", "center"],
                                    "configuration": {"content": "Hello, World!", "color": "white"},
                                    "effects": [
                                        {
                                            "type": f"{TextBackgroundEffectModuleDefinition.PLUGIN_PREFIX}.effects.blocks.text.write",
                                            "time": {"duration": TextBackgroundEffectModuleDefinition.EXAMPLE_DURATION}
                                        },
                                        {
                                            "type": f"{TextBackgroundEffectModuleDefinition.PLUGIN_PREFIX}.effects.blocks.text.background",
                                            "time": {"duration": TextBackgroundEffectModuleDefinition.EXAMPLE_DURATION},
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
            }
        ]
