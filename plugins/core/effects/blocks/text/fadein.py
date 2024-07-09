from videopy.compilation import Compilation
from videopy.effect import AbstractEffectFactory, AbstractBlockEffect
from videopy.module import AbstractModuleDefinition
from videopy.utils.logger import Logger
from videopy.utils.time import Time
from moviepy.video.compositing.transitions import crossfadein


class Effect(AbstractBlockEffect):

    def __init__(self, time, initial_color):
        super().__init__("fadein", time)

        self.initial_color = initial_color

    def render_on_block(self, clip):
        if clip is None:
            raise ValueError("fadein effect requires something to fade in (can't be first effect)")

        return Compilation(source=crossfadein(clip, self.time.duration), mode="use_source")


class EffectFactory(AbstractEffectFactory):
    def from_yml(self, effect_yml):
        configuration = effect_yml.get('configuration', {})
        time = effect_yml.get('time', {})

        if time.get('start', 0) > 0:
            Logger.warn(f"The <<time.start>> parameter for <<fadein>> effect is useless and will be ignored")

        return Effect(Time(time.get('start', 0), time.get('duration', 0)),
                      configuration.get('initial_color', [0, 0, 0]))


class TextFadeInEffectModuleDefinition(AbstractModuleDefinition):
    PLUGIN_PREFIX = "plugins.core"
    PLUGIN_PREFIX_INDEX = PLUGIN_PREFIX.replace(".", "")

    EXAMPLE_DURATION = 1

    @staticmethod
    def get_description():
        return "Fade in the text block."

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
                "name": "Fade in effect.",
                "description": "This effect will slowly fade in the text block.",
                "scenario": {
                    "width": 640, "height": 240, "fps": 24,
                    "frames": [
                        {
                            "type": f"{TextFadeInEffectModuleDefinition.PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": TextFadeInEffectModuleDefinition.EXAMPLE_DURATION},
                            "configuration": {"file_path": "example/assets/image/1.jpg"},
                            "effects": [
                                {"type": f"{TextFadeInEffectModuleDefinition.PLUGIN_PREFIX}.effects.frames.resize",
                                 "configuration": {"mode": "center_crop"}}],
                            "blocks": [
                                {
                                    "type": f"{TextFadeInEffectModuleDefinition.PLUGIN_PREFIX}.blocks.text",
                                    "time": {"duration": TextFadeInEffectModuleDefinition.EXAMPLE_DURATION},
                                    "position": ["center", "center"],
                                    "configuration": {"content": "Hello, World!", "color": "white"},
                                    "effects": [
                                        {
                                            "type": f"{TextFadeInEffectModuleDefinition.PLUGIN_PREFIX}.effects.blocks.text.write",
                                            "time": {"duration": TextFadeInEffectModuleDefinition.EXAMPLE_DURATION}
                                        },
                                        {
                                            "type": f"{TextFadeInEffectModuleDefinition.PLUGIN_PREFIX}.effects.blocks.text.fadein",
                                            "time": {"duration": TextFadeInEffectModuleDefinition.EXAMPLE_DURATION},
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
            },
            {
                "name": "Fade in effect with delay.",
                "description": "This effect will slowly fade in the text block.",
                "scenario": {
                    "width": 640, "height": 240, "fps": 24,
                    "frames": [
                        {
                            "type": f"{TextFadeInEffectModuleDefinition.PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": 5},
                            "configuration": {"file_path": "example/assets/image/1.jpg"},
                            "effects": [
                                {"type": f"{TextFadeInEffectModuleDefinition.PLUGIN_PREFIX}.effects.frames.resize",
                                 "configuration": {"mode": "center_crop"}}],
                            "blocks": [
                                {
                                    "type": f"{TextFadeInEffectModuleDefinition.PLUGIN_PREFIX}.blocks.text",
                                    "time": {"duration": 2.5, "start": 2.5},
                                    "position": ["center", "center"],
                                    "configuration": {"content": "Hello, World!", "color": "white"},
                                    "effects": [
                                        {
                                            "type": f"{TextFadeInEffectModuleDefinition.PLUGIN_PREFIX}.effects.blocks.text.write",
                                            "time": {"duration": 2.5}
                                        },
                                        {
                                            "type": f"{TextFadeInEffectModuleDefinition.PLUGIN_PREFIX}.effects.blocks.text.fadein",
                                            "time": {"duration": 1},
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
            }
        ]
