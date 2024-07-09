from videopy.compilation import Compilation
from videopy.effect import AbstractFrameEffect, AbstractEffectFactory
from videopy.module import AbstractModuleDefinition
from videopy.utils.time import Time


class Effect(AbstractFrameEffect):

    def __init__(self, time, configuration):
        super().__init__("resize", time)

        self.configuration = configuration

    def render_on_frame(self, clip):
        clip = self.frame.clip

        resizers = {
            'fit': {
                'handler': fit
            },
            'center_crop': {
                'handler': center_crop
            },
            'default': {
                'handler': default
            }
        }

        self.frame.scenario.hooks.run_hook("scenario.frame.effects.resize.register", resizers)

        if resizers[self.configuration['mode']] is None:
            raise ValueError(f"Unknown resizer mode: {self.configuration['mode']}")

        resizer = resizers.get(self.configuration['mode'], None)

        if resizer['handler'] is None:
            raise ValueError(f"Unknown resizer mode: {self.configuration['mode']}")

        result = resizer['handler'](self, clip)

        if result is None:
            raise ValueError(f"Resizer {self.configuration['mode']} did not return a result")

        return Compilation(result, mode="use_source")


class EffectFactory(AbstractEffectFactory):

    def from_yml(self, effect_yml):
        configuration = effect_yml.get('configuration', {})

        return Effect(Time(0, 0), configuration)


def fit(effect, clip):
    width, height = effect.frame.scenario.size

    return clip.resize(newsize=[width, height])  # Shrink to fit


def center_crop(effect, clip):
    width, height = effect.frame.scenario.size

    # Resize while maintaining aspect ratio, then crop to fill the size
    aspect_ratio_clip = clip.w / clip.h
    aspect_ratio_video = width / height

    if aspect_ratio_clip > aspect_ratio_video:
        # Clip is wider than the target aspect ratio, resize by height
        clip = clip.resize(height=height)
    else:
        # Clip is taller than the target aspect ratio, resize by width
        clip = clip.resize(width=width)

    return clip.crop(x_center=clip.w / 2, y_center=clip.h / 2, width=width, height=height)


def default(effect, clip):
    return clip.resize(effect.frame.scenario.size)


class FrameResizeEffectModuleDefinition(AbstractModuleDefinition):
    PLUGIN_PREFIX = "plugins.core"
    PLUGIN_PREFIX_INDEX = PLUGIN_PREFIX.replace(".", "")

    EXAMPLE_DURATION = 1

    @staticmethod
    def get_description():
        return "Resize the frame with given mode."

    @staticmethod
    def get_configuration():
        return {
            "mode": {
                "description": "Mode of the resize effect.",
                "type": "str",
                "required": False,
                "default": "default",
            },
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
                "name": "Resize Effect - Fit",
                "description": "This example shows how to add 'fit' resize effect on frame.",
                "scenario": {
                    "width": 640, "height": 240, "fps": 24,
                    "frames": [
                        {
                            "type": f"{FrameResizeEffectModuleDefinition.PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": FrameResizeEffectModuleDefinition.EXAMPLE_DURATION},
                            "configuration": {"file_path": "example/assets/image/1.jpg"},
                            "effects": [
                                {"type": f"{FrameResizeEffectModuleDefinition.PLUGIN_PREFIX}.effects.frames.resize",
                                 "configuration": {"mode": "fit"}},
                            ]
                        }
                    ]
                },
            },
            {
                "name": "Resize Effect - Center crop",
                "description": "This example shows how to add 'center_crop' resize effect on frame.",
                "scenario": {
                    "width": 640, "height": 240, "fps": 24,
                    "frames": [
                        {
                            "type": f"{FrameResizeEffectModuleDefinition.PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": FrameResizeEffectModuleDefinition.EXAMPLE_DURATION},
                            "configuration": {"file_path": "example/assets/image/1.jpg"},
                            "effects": [
                                {"type": f"{FrameResizeEffectModuleDefinition.PLUGIN_PREFIX}.effects.frames.resize",
                                 "configuration": {"mode": "center_crop"}},
                            ]
                        }
                    ]
                },
            }
        ]
