from moviepy.editor import AudioFileClip

from videopy.compilation import Compilation
from videopy.effect import AbstractEffectFactory, AbstractFrameEffect
from videopy.module import AbstractModuleDefinition
from videopy.utils.time import Time


class Effect(AbstractFrameEffect):

    def __init__(self, time, configuration):
        super().__init__("audio", time)

        self.configuration = configuration

    def render_on_frame(self, clip):
        audio_clip = (AudioFileClip(self.configuration["file_path"]))
        subclip_start = self.configuration.get('subclip_start', None)

        if subclip_start is not None:
            audio_clip = audio_clip.subclip(subclip_start, self.time.duration)

        audio_clip = audio_clip.set_start(self.time.start).set_duration(self.time.duration)

        self.frame.scenario.add_audio(audio_clip)

        return Compilation(clip, mode="use_source")


class EffectFactory(AbstractEffectFactory):

    def from_yml(self, effect_yml):
        time = effect_yml.get('time', {})
        configuration = effect_yml.get('configuration', {})

        return Effect(Time(time.get('start', 0), time.get('duration', 0)), configuration)


class FrameAudioEffectModuleDefinition(AbstractModuleDefinition):
    PLUGIN_PREFIX = "plugins.core"
    PLUGIN_PREFIX_INDEX = PLUGIN_PREFIX.replace(".", "")

    EXAMPLE_DURATION = 1

    @staticmethod
    def get_description():
        return "Adds audio effect on frame."

    @staticmethod
    def get_configuration():
        return {
            "file_path": {
                "description": "Path to the audio file.",
                "type": "str",
                "required": True
            },
            "subclip_start": {
                "description": "Setting the subclip will start the audio from the given time.",
                "type": "float",
                "default": 0,
                "required": False,
            }
        }

    @staticmethod
    def get_renders_on() -> dict:
        return {
            "frame": ["image"]
        }

    @staticmethod
    def get_examples():
        return [
            {
                "name": "Fade In effect on frame",
                "description": "Effect will slowly fade in the frame content.",
                "tips": [f"This effect ignores the `time.start` parameter, as it always starts from the beginning "
                         f"of the frame."],
                "scenario": {
                    "width": 640, "height": 240, "fps": 24,
                    "frames": [
                        {
                            "type": f"{FrameAudioEffectModuleDefinition.PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": 1},
                            "configuration": {"file_path": "example/assets/image/1.jpg"},
                            "effects": [
                                {"type": f"{FrameAudioEffectModuleDefinition.PLUGIN_PREFIX}.effects.frames.resize",
                                 "configuration": {"mode": "center_crop"}},
                                {"type": f"{FrameAudioEffectModuleDefinition.PLUGIN_PREFIX}.effects.frames.fadein",
                                 "time": {"duration": 0.5}}
                            ]
                        }
                    ]
                },
            }
        ]
