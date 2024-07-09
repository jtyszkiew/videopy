from videopy.block import AbstractBlock, AbstractBlockFactory
from videopy.compilation import Compilation
from videopy.module import AbstractModuleDefinition
from videopy.utils.time import Time


class Block(AbstractBlock):

    def get_type(self):
        return "image"

    def __init__(self, time, position, configuration, frame):
        super().__init__(time, position, frame)

        self.configuration = configuration

    def __str__(self):
        return f"Block(time={self.time}, position={self.position}, configuration={self.configuration})"

    def render(self, clip):
        return Compilation(clip, mode="use_source")


class BlockFactory(AbstractBlockFactory):

    def from_yml(self, block_yml, module_yml, frame):
        time = block_yml.get('time', {})

        return Block(
            Time(time.get('start', 0), time['duration']),
            block_yml['position'],
            block_yml['configuration'],
            frame
        )


class ImageBlockModuleDefinition(AbstractModuleDefinition):
    PLUGIN_PREFIX = "plugins.core"
    PLUGIN_PREFIX_INDEX = PLUGIN_PREFIX.replace(".", "")

    EXAMPLE_DURATION = 1

    @staticmethod
    def get_description():
        return "This block will display image."

    @staticmethod
    def get_configuration():
        return {
            "file_path": {
                "description": "Path to the image file to show.",
                "type": "str",
                "required": True
            },
            "width": {
                "description": "Width of the image. Use -1 to keep the original width.",
                "type": "int",
                "default": -1,
                "required": False
            },
            "height": {
                "description": "Height of the image. Use -1 to keep the original height.",
                "type": "int",
                "default": -1,
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
                "name": "Showing Image",
                "description": "This example shows how to display image as a block.",
                "tips": [
                    "This block doesn't show anything by default.",
                    "Don't forget to use some display effect on text block to make it visible. "
                    f"([{ImageBlockModuleDefinition.PLUGIN_PREFIX}.effects.block.image.display]({ImageBlockModuleDefinition.PLUGIN_PREFIX_INDEX}effectsblockimagedisplay)"
                ],
                "scenario": {
                    "width": 640, "height": 240, "fps": 24,
                    "frames": [
                        {
                            "type": f"{ImageBlockModuleDefinition.PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": ImageBlockModuleDefinition.EXAMPLE_DURATION},
                            "configuration": {"file_path": "example/assets/image/1.jpg"},
                            "effects": [
                                {"type": f"{ImageBlockModuleDefinition.PLUGIN_PREFIX}.effects.frames.resize",
                                 "configuration": {"mode": "center_crop"}}
                            ],
                            "blocks": [
                                {
                                    "type": f"{ImageBlockModuleDefinition.PLUGIN_PREFIX}.blocks.image",
                                    "time": {"duration": ImageBlockModuleDefinition.EXAMPLE_DURATION},
                                    "position": ["center", "center"],
                                    "configuration": {"file_path": "example/assets/image/logo.png", "width": 40,
                                                      "height": 40},
                                    "effects": [{
                                                    "type": f"{ImageBlockModuleDefinition.PLUGIN_PREFIX}.effects.blocks.image.display",
                                                    "time": {"duration": ImageBlockModuleDefinition.EXAMPLE_DURATION}}]
                                },
                                {
                                    "type": f"{ImageBlockModuleDefinition.PLUGIN_PREFIX}.blocks.image",
                                    "time": {"duration": ImageBlockModuleDefinition.EXAMPLE_DURATION},
                                    "position": ["left", "top"],
                                    "configuration": {"file_path": "example/assets/image/logo.png", "width": 100,
                                                      "height": 100},
                                    "effects": [{
                                                    "type": f"{ImageBlockModuleDefinition.PLUGIN_PREFIX}.effects.blocks.image.display",
                                                    "time": {"duration": ImageBlockModuleDefinition.EXAMPLE_DURATION}}]
                                },
                                {
                                    "type": f"{ImageBlockModuleDefinition.PLUGIN_PREFIX}.blocks.image",
                                    "time": {"duration": ImageBlockModuleDefinition.EXAMPLE_DURATION},
                                    "position": ["right", "top"],
                                    "configuration": {"file_path": "example/assets/image/logo.png", "width": 100,
                                                      "height": 100},
                                    "effects": [{
                                                    "type": f"{ImageBlockModuleDefinition.PLUGIN_PREFIX}.effects.blocks.image.display",
                                                    "time": {"duration": ImageBlockModuleDefinition.EXAMPLE_DURATION}}]
                                },
                                {
                                    "type": f"{ImageBlockModuleDefinition.PLUGIN_PREFIX}.blocks.image",
                                    "time": {"duration": ImageBlockModuleDefinition.EXAMPLE_DURATION},
                                    "position": ["center", "top"],
                                    "configuration": {"file_path": "example/assets/image/logo.png", "width": 100,
                                                      "height": 100},
                                    "effects": [{
                                                    "type": f"{ImageBlockModuleDefinition.PLUGIN_PREFIX}.effects.blocks.image.display",
                                                    "time": {"duration": ImageBlockModuleDefinition.EXAMPLE_DURATION}}]
                                },
                                {
                                    "type": f"{ImageBlockModuleDefinition.PLUGIN_PREFIX}.blocks.image",
                                    "time": {"duration": ImageBlockModuleDefinition.EXAMPLE_DURATION},
                                    "position": ["left", "bottom"],
                                    "configuration": {"file_path": "example/assets/image/logo.png", "width": 100,
                                                      "height": 100},
                                    "effects": [{
                                                    "type": f"{ImageBlockModuleDefinition.PLUGIN_PREFIX}.effects.blocks.image.display",
                                                    "time": {"duration": ImageBlockModuleDefinition.EXAMPLE_DURATION}}]
                                },
                                {
                                    "type": f"{ImageBlockModuleDefinition.PLUGIN_PREFIX}.blocks.image",
                                    "time": {"duration": ImageBlockModuleDefinition.EXAMPLE_DURATION},
                                    "position": ["right", "bottom"],
                                    "configuration": {"file_path": "example/assets/image/logo.png", "width": 100,
                                                      "height": 100},
                                    "effects": [{
                                                    "type": f"{ImageBlockModuleDefinition.PLUGIN_PREFIX}.effects.blocks.image.display",
                                                    "time": {"duration": ImageBlockModuleDefinition.EXAMPLE_DURATION}}]
                                },
                                {
                                    "type": f"{ImageBlockModuleDefinition.PLUGIN_PREFIX}.blocks.image",
                                    "time": {"duration": ImageBlockModuleDefinition.EXAMPLE_DURATION},
                                    "position": ["center", "bottom"],
                                    "configuration": {"file_path": "example/assets/image/logo.png", "width": 100,
                                                      "height": 100},
                                    "effects": [{
                                                    "type": f"{ImageBlockModuleDefinition.PLUGIN_PREFIX}.effects.blocks.image.display",
                                                    "time": {"duration": ImageBlockModuleDefinition.EXAMPLE_DURATION}}]
                                },
                            ]
                        },
                    ]
                },
            }
        ]
