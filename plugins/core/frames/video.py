from videopy.frame import AbstractFrame, AbstractFrameFactory
from videopy.module import AbstractModuleDefinition
from videopy.utils.time import Time
from moviepy.editor import VideoFileClip


class Frame(AbstractFrame):

    def __init__(self, time, configuration, scenario):
        super().__init__(time, scenario)

        self.file_path = configuration["file_path"]
        self.mute = configuration.get("mute", False)
        self.subclip_start = configuration.get("subclip_start", 0)
        self.cut_to_frame_duration = configuration.get("cut_to_frame_duration", True)

    def get_type(self):
        return "video"

    def render(self, relative_start_time):
        clip = VideoFileClip(
            filename=self.file_path,
            audio=(not self.mute),
        )

        if self.subclip_start:
            clip = clip.subclip(self.subclip_start, self.subclip_start + self.time.duration)
        if self.time.duration < clip.duration and self.cut_to_frame_duration:
            clip = clip.set_duration(self.time.duration)

        return clip


class FrameFactory(AbstractFrameFactory):
    def from_yml(self, frame_yml, scenario):
        time_yml = frame_yml.get("time", {})

        return Frame(Time(time_yml.get("start", 0), time_yml.get("duration", 1)), frame_yml['configuration'], scenario)


class VideoFrameModuleDefinition(AbstractModuleDefinition):
    PLUGIN_PREFIX = "plugins.core"
    PLUGIN_PREFIX_INDEX = PLUGIN_PREFIX.replace(".", "")

    EXAMPLE_DURATION = 1

    @staticmethod
    def get_description():
        return "This frame will display an video."

    @staticmethod
    def get_configuration():
        return {
            "file_path": {
                "description": "The path to the video.",
                "type": "str",
                "required": True
            },
            "mute": {
                "description": "Mute the source video (for example if you want to compose the sound differently).",
                "type": "bool",
                "default": False,
                "required": False
            },
            "subclip_start": {
                "description": "Setting the subclip will start the video from the given time.",
                "type": "float",
                "default": 0,
                "required": False,
            },
            "cut_to_frame_duration": {
                "description": "If video is longer than frame duration, cut it to frame duration.",
                "type": "bool",
                "default": True,
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
                "name": "Showing Video as Frame",
                "description": f"Example is showing how to set video as a frame, as the video size don't match the "
                               f"scenario size (640x240), "
                               f"it will additionally use the "
                               f"[{VideoFrameModuleDefinition.PLUGIN_PREFIX}.effects.frames.resize](#{VideoFrameModuleDefinition.PLUGIN_PREFIX_INDEX}effectsframesresize)"
                               f" effect to center crop it.",
                "tips": [f"Example have a duration of 1 seconds for test purposes and generation speed. In real life "
                         f"you probably want a longer duration."],
                "scenario": {
                    "width": 640, "height": 240, "fps": 24,
                    "frames": [
                        {
                            "type": f"{VideoFrameModuleDefinition.PLUGIN_PREFIX}.frames.video",
                            "time": {"duration": 1},
                            "configuration": {"file_path": "example/assets/video/BigBuckBunny_640x240.mp4"},
                            "effects": [{"type": f"{VideoFrameModuleDefinition.PLUGIN_PREFIX}.effects.frames.resize",
                                        "configuration": {"mode": "center_crop"}}]
                        }
                    ]
                },
            }
        ]
