from moviepy.editor import ImageClip

from videopy.frame import AbstractFrame, AbstractFrameFactory
from videopy.module import AbstractModuleDefinition
from videopy.utils.time import Time


class Frame(AbstractFrame):

    def __init__(self, time, configuration, scenario):
        super().__init__(time, scenario)

        self.configuration = configuration

    def get_type(self):
        return 'image'

    def render(self, relative_start_time):
        return ImageClip(self.configuration['file_path'], duration=self.time.duration)


class FrameFactory(AbstractFrameFactory):

    def from_yml(self, frame_yml, scenario):
        configuration = frame_yml['configuration']
        time_yml = frame_yml.get('time', {})

        return Frame(Time(time_yml.get('start', 0), time_yml.get('duration', 1)), configuration, scenario)


class ImageFrameModuleDefinition(AbstractModuleDefinition):
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
                "description": "The path to the image.",
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
                "name": "Showing Image as Frame",
                "description": f"Example is showing how to set image as a frame, as the image size don't match the "
                               f"scenario size (640x240), "
                               f"it will additionally use the "
                               f"[{ImageFrameModuleDefinition.PLUGIN_PREFIX}.effects.frames.resize](#{ImageFrameModuleDefinition.PLUGIN_PREFIX_INDEX}effectsframesresize)"
                               f" effect to center crop it.",
                "tips": [f"Example have a duration of {ImageFrameModuleDefinition.EXAMPLE_DURATION} seconds for test "
                         f"purposes and generation speed. In real life you probably want a longer duration."],
                "scenario": {
                    "width": 640, "height": 240, "fps": 24,
                    "frames": [
                        {
                            "type": f"{ImageFrameModuleDefinition.PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": ImageFrameModuleDefinition.EXAMPLE_DURATION},
                            "configuration": {"file_path": "example/assets/image/1.jpg"},
                            "effects": [
                                {"type": f"{ImageFrameModuleDefinition.PLUGIN_PREFIX}.effects.frames.resize",
                                 "configuration": {"mode": "center_crop"}}
                            ]
                        }
                    ]
                },
            }
        ]
