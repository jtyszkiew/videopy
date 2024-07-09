from videopy.compilation import Compilation
from videopy.effect import AbstractFrameEffect, AbstractEffectFactory
from videopy.module import AbstractModuleDefinition
from videopy.utils.logger import Logger
from videopy.utils.time import Time


class Effect(AbstractFrameEffect):

    def __init__(self, time, final_color):
        super().__init__("fadeout", time)

        self.final_color = final_color

    def render_on_frame(self, clip):
        return Compilation(clip.crossfadeout(self.time.duration), mode="use_source")


class EffectFactory(AbstractEffectFactory):
    def from_yml(self, effect_yml):
        configuration = effect_yml.get('configuration', {})
        time = effect_yml.get('time', {})

        if time.get('start', 0) > 0:
            Logger.warn(f"The <<time.start>> parameter for <<fadeout>> effect is useless and will be ignored")

        return Effect(Time(time.get('start', 0), time.get('duration', 0)),
                      configuration.get('final_color', [0, 0, 0]))


class FrameFadeOutEffectModuleDefinition(AbstractModuleDefinition):
    PLUGIN_PREFIX = "plugins.core"
    PLUGIN_PREFIX_INDEX = PLUGIN_PREFIX.replace(".", "")

    EXAMPLE_DURATION = 1

    @staticmethod
    def get_description():
        return "Fade out the frame."

    @staticmethod
    def get_configuration():
        return {}

    @staticmethod
    def get_renders_on() -> dict:
        return {
            "frame": ["image"]
        }

    @staticmethod
    def get_examples():
        return [
            {
                "name": "Fade Out effect on frame",
                "description": "Effect will slowly fade out the frame content.",
                "tips": [f"This effect ignores the `time.start` parameter, as it always starts from the "
                         f"(`frame.time.duration` - `effect.time.duration`) (right side) of the frame."],
                "scenario": {
                    "width": 640, "height": 240, "fps": 24,
                    "frames": [
                        {
                            "type": f"{FrameFadeOutEffectModuleDefinition.PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": 1},
                            "configuration": {"file_path": "example/assets/image/1.jpg"},
                            "effects": [
                                {"type": f"{FrameFadeOutEffectModuleDefinition.PLUGIN_PREFIX}.effects.frames.resize",
                                 "configuration": {"mode": "center_crop"}},
                                {"type": f"{FrameFadeOutEffectModuleDefinition.PLUGIN_PREFIX}.effects.frames.fadeout",
                                 "time": {"duration": 0.5}}
                            ]
                        }
                    ]
                },
            }
        ]
