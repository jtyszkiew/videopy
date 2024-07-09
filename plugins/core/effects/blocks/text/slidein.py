from videopy.compilation import Compilation
from videopy.effect import AbstractEffectFactory, AbstractBlockEffect
from videopy.module import AbstractModuleDefinition
from videopy.utils import rounded_background
from videopy.utils.logger import Logger
from videopy.utils.time import Time
from moviepy.video.compositing.transitions import slide_in
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip


class Effect(AbstractBlockEffect):

    def __init__(self, time, configuration):
        super().__init__("slidein", time)

        self.configuration = configuration

    def render_on_block(self, clip):
        if clip is None:
            raise ValueError("slidein effect requires something to slide in (can't be first effect)")

        # Since the moviepy slidein effect requires a CompositeVideoClip, we need to create one if the clip is not one
        if not isinstance(clip, CompositeVideoClip):
            txt_width, txt_height = self.block.get_text_size()
            position = self.block.get_text_position()

            bg_width = txt_width + 2 * self.block.configuration['padding']
            bg_height = txt_height + 2 * self.block.configuration['padding']

            bg_clip = rounded_background(bg_width, bg_height, (0, 0, 0, 0), 0).set_duration(self.time.duration)
            bg_clip = (bg_clip.set_position((position[0] - self.block.configuration['padding'],
                                             position[1] - self.block.configuration['padding']))
                       .set_start(self.block.time.start + self.time.start))

            clip = CompositeVideoClip([bg_clip, clip], size=self.block.frame.scenario.size)

            return Compilation(source=slide_in(clip, self.time.duration, self.configuration['slide_from']),
                               mode="use_source")

        return Compilation(source=slide_in(clip, self.time.duration, self.configuration['slide_from']),
                           mode="use_source")


class EffectFactory(AbstractEffectFactory):
    def from_yml(self, effect_yml):
        configuration = effect_yml.get('configuration', {})
        time = effect_yml.get('time', {})

        if time.get('start', 0) > 0:
            Logger.warn(f"The <<time.start>> parameter for <<slidein>> effect is useless and will be ignored")

        return Effect(Time(time.get('start', 0), time.get('duration', 0)), configuration)


class TextSlideInEffectModuleDefinition(AbstractModuleDefinition):
    PLUGIN_PREFIX = "plugins.core"
    PLUGIN_PREFIX_INDEX = PLUGIN_PREFIX.replace(".", "")

    EXAMPLE_DURATION = 1

    @staticmethod
    def get_description():
        return "Slide in the text block."

    @staticmethod
    def get_configuration():
        return {
            "slide_from": {
                "description": "The direction of the slide in.",
                "type": "str",
                "default": "left",
                "required": False
            },
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
                "name": "Slide in effect.",
                "description": "This effect will slide in the text block.",
                "scenario": {
                    "width": 640, "height": 240, "fps": 24,
                    "frames": [
                        {
                            "type": f"{TextSlideInEffectModuleDefinition.PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": TextSlideInEffectModuleDefinition.EXAMPLE_DURATION},
                            "configuration": {"file_path": "example/assets/image/1.jpg"},
                            "effects": [
                                {"type": f"{TextSlideInEffectModuleDefinition.PLUGIN_PREFIX}.effects.frames.resize",
                                 "configuration": {"mode": "center_crop"}}],
                            "blocks": [
                                {
                                    "type": f"{TextSlideInEffectModuleDefinition.PLUGIN_PREFIX}.blocks.text",
                                    "time": {"duration": TextSlideInEffectModuleDefinition.EXAMPLE_DURATION},
                                    "position": ["center", "center"],
                                    "configuration": {"content": "Hello, World!", "color": "white"},
                                    "effects": [
                                        {
                                            "type": f"{TextSlideInEffectModuleDefinition.PLUGIN_PREFIX}.effects.blocks.text.write",
                                            "time": {"duration": TextSlideInEffectModuleDefinition.EXAMPLE_DURATION}
                                        },
                                        {
                                            "type": f"{TextSlideInEffectModuleDefinition.PLUGIN_PREFIX}.effects.blocks.text.slidein",
                                            "time": {
                                                "duration": TextSlideInEffectModuleDefinition.EXAMPLE_DURATION / 2},
                                            "configuration": {"slide_from": "top"},
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
            },
            {
                "name": "Slide in effect with background.",
                "description": "This effect will slide in the text block.",
                "scenario": {
                    "width": 640, "height": 240, "fps": 24,
                    "frames": [
                        {
                            "type": f"{TextSlideInEffectModuleDefinition.PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": TextSlideInEffectModuleDefinition.EXAMPLE_DURATION},
                            "configuration": {"file_path": "example/assets/image/1.jpg"},
                            "effects": [
                                {"type": f"{TextSlideInEffectModuleDefinition.PLUGIN_PREFIX}.effects.frames.resize",
                                 "configuration": {"mode": "center_crop"}}],
                            "blocks": [
                                {
                                    "type": f"{TextSlideInEffectModuleDefinition.PLUGIN_PREFIX}.blocks.text",
                                    "time": {"duration": TextSlideInEffectModuleDefinition.EXAMPLE_DURATION},
                                    "position": ["center", "center"],
                                    "configuration": {"content": "Hello, World!", "color": "white"},
                                    "effects": [
                                        {
                                            "type": f"{TextSlideInEffectModuleDefinition.PLUGIN_PREFIX}.effects.blocks.text.write",
                                            "time": {"duration": TextSlideInEffectModuleDefinition.EXAMPLE_DURATION}
                                        },
                                        {
                                            "type": f"{TextSlideInEffectModuleDefinition.PLUGIN_PREFIX}.effects.blocks.text.background",
                                            "time": {"duration": TextSlideInEffectModuleDefinition.EXAMPLE_DURATION},
                                        },
                                        {
                                            "type": f"{TextSlideInEffectModuleDefinition.PLUGIN_PREFIX}.effects.blocks.text.slidein",
                                            "time": {
                                                "duration": TextSlideInEffectModuleDefinition.EXAMPLE_DURATION / 2},
                                            "configuration": {"slide_from": "top"},
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
            },
        ]
