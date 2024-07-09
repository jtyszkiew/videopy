from videopy.block import AbstractBlock, AbstractBlockFactory
from videopy.compilation import Compilation
from videopy.module import AbstractModuleDefinition
from videopy.utils.time import Time


class Block(AbstractBlock):

    def __init__(self, time, configuration, frame):
        super().__init__(time, [0, 0], frame)

        self.__audio = None

        self.configuration = configuration
        self.current_time = 0

    def get_type(self):
        return "audio"

    def render(self, clip):
        return Compilation(clip, mode="ignore")

    def set_audio(self, audio):
        if self.__audio is not None:
            raise Exception("Audio is already set")

        self.__audio = audio

    def get_audio(self):
        return self.__audio


class BlockFactory(AbstractBlockFactory):
    def from_yml(self, block_yml, module_yml, frame):
        time = block_yml.get('time', {})

        return Block(Time(time.get('start', 0), time['duration']), block_yml['configuration'], frame)


class AudioBlockModuleDefinition(AbstractModuleDefinition):
    PLUGIN_PREFIX = "plugins.core"
    PLUGIN_PREFIX_INDEX = PLUGIN_PREFIX.replace(".", "")

    EXAMPLE_DURATION = 1

    @staticmethod
    def get_description():
        return "This is base block to manage audio on frame."

    @staticmethod
    def get_configuration():
        return {
            "file_path": {
                "description": "The path to the audio file.",
                "type": "str",
                "required": True
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
                    f"([{AudioBlockModuleDefinition.PLUGIN_PREFIX}.effects.block.text.write]({AudioBlockModuleDefinition.PLUGIN_PREFIX_INDEX}effectsblocktextwrite), "
                    f"[{AudioBlockModuleDefinition.PLUGIN_PREFIX}.effects.block.text.typewrite]({AudioBlockModuleDefinition.PLUGIN_PREFIX_INDEX}effectsblocktexttypewrite))."
                ],
                "scenario": {
                    "width": 640, "height": 240, "fps": 24,
                    "frames": [
                        {
                            "type": f"{AudioBlockModuleDefinition.PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": AudioBlockModuleDefinition.EXAMPLE_DURATION},
                            "configuration": {"file_path": "example/assets/image/1.jpg"},
                            "effects": [
                                {"type": f"{AudioBlockModuleDefinition.PLUGIN_PREFIX}.effects.frames.resize",
                                 "configuration": {"mode": "center_crop"}}
                            ],
                            "blocks": [
                                {
                                    "type": f"{AudioBlockModuleDefinition.PLUGIN_PREFIX}.blocks.text",
                                    "time": {"duration": AudioBlockModuleDefinition.EXAMPLE_DURATION},
                                    "position": ["center", "center"],
                                    "configuration": {"content": "Hello, World!", "color": "white"},
                                    "effects": [{
                                        "type": f"{AudioBlockModuleDefinition.PLUGIN_PREFIX}.effects.blocks.text.write",
                                        "time": {"duration": AudioBlockModuleDefinition.EXAMPLE_DURATION}
                                    }]
                                }
                            ]
                        },
                    ]
                },
            }
        ]
