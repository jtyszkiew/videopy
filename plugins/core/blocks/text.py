from moviepy.editor import TextClip

from videopy.block import AbstractBlock, AbstractBlockFactory
from videopy.compilation import Compilation
from videopy.module import AbstractModuleDefinition
from videopy.utils.time import Time
from videopy.utils.utils import transform_position


class Block(AbstractBlock):

    def get_type(self):
        return "text"

    def __init__(self, time, position, configuration, frame):
        super().__init__(time, position, frame)

        self.configuration = configuration

    def __str__(self):
        return f"Block(time={self.time}, position={self.position}, configuration={self.configuration})"

    def get_text_size(self):
        clip = TextClip(
            txt=self.configuration['content'],
            font=self.configuration['font'],
            fontsize=self.configuration['size']
        )

        return clip.size

    def get_text_position(self):
        """This method will calculate the text position based on the block position and padding."""
        x, y = transform_position(
            position=self.position,
            frame=self.frame.scenario.size,
            block=self.get_text_size(),
            margin=self.configuration['margin']
        )

        return x, y

    def render(self, clip):
        return Compilation(clip, mode="use_source")


class BlockFactory(AbstractBlockFactory):

    def from_yml(self, block_yml, module_yml, frame):
        time = block_yml.get('time', {})

        return Block(Time(time.get('start', 0), time['duration']),
                     block_yml['position'], block_yml['configuration'], frame)


class TextBlockModuleDefinition(AbstractModuleDefinition):
    PLUGIN_PREFIX = "plugins.core"
    PLUGIN_PREFIX_INDEX = PLUGIN_PREFIX.replace(".", "")

    EXAMPLE_DURATION = 1

    @staticmethod
    def get_description():
        return "This block will display text."

    @staticmethod
    def get_configuration():
        return {
            "content": {
                "description": "The text content.",
                "type": "str",
                "required": True
            },
            "font": {
                "description": "The font of the text.",
                "type": "str",
                "default": "Roboto-Bold",
                "required": False
            },
            "size": {
                "description": "The size of the text.",
                "type": "int",
                "default": 50,
                "required": False
            },
            "color": {
                "description": "The color of the text.",
                "type": "str",
                "default": "black",
                "required": False
            },
            "margin": {
                "description": "The margin of the text.",
                "type": "float",
                "default": 30,
                "required": False
            },
            "padding": {
                "description": "The padding of the text.",
                "type": "float",
                "default": 20,
                "required": False
            }
        }

    @staticmethod
    def get_renders_on() -> dict:
        return {}

    @staticmethod
    def get_examples():
        return [
            {
                "name": "Showing Text",
                "description": "This example shows how to display text as a block.",
                "tips": [
                    "This block doesn't show anything by default.",
                    "Don't forget to use some display effect on text block to make it visible. "
                    f"([{TextBlockModuleDefinition.PLUGIN_PREFIX}.effects.block.text.write]({TextBlockModuleDefinition.PLUGIN_PREFIX_INDEX}effectsblocktextwrite), "
                    f"[{TextBlockModuleDefinition.PLUGIN_PREFIX}.effects.block.text.typewrite]({TextBlockModuleDefinition.PLUGIN_PREFIX_INDEX}effectsblocktexttypewrite))."
                ],
                "scenario": {
                    "width": 640, "height": 240, "fps": 24,
                    "frames": [
                        {
                            "type": f"{TextBlockModuleDefinition.PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": TextBlockModuleDefinition.EXAMPLE_DURATION},
                            "configuration": {"file_path": "example/assets/image/1.jpg"},
                            "effects": [
                                {"type": f"{TextBlockModuleDefinition.PLUGIN_PREFIX}.effects.frames.resize",
                                 "configuration": {"mode": "center_crop"}}
                            ],
                            "blocks": [
                                {
                                    "type": f"{TextBlockModuleDefinition.PLUGIN_PREFIX}.blocks.text",
                                    "time": {"duration": TextBlockModuleDefinition.EXAMPLE_DURATION},
                                    "position": ["center", "center"],
                                    "configuration": {"content": "Hello, World!", "color": "white"},
                                    "effects": [{
                                        "type": f"{TextBlockModuleDefinition.PLUGIN_PREFIX}.effects.blocks.text.write",
                                        "time": {"duration": TextBlockModuleDefinition.EXAMPLE_DURATION}
                                    }]
                                }
                            ]
                        },
                    ]
                },
            }
        ]
