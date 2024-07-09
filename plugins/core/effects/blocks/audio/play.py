from moviepy.editor import AudioFileClip

from videopy.compilation import Compilation
from videopy.effect import AbstractEffectFactory, AbstractBlockEffect
from videopy.module import AbstractModuleDefinition
from videopy.utils.time import Time


class Effect(AbstractBlockEffect):

    def __init__(self, time, configuration):
        super().__init__("play", time)

        self.configuration = configuration

    def render_on_block(self, clip):
        if self.block.get_type() != "audio":
            raise Exception(f"Effect [play] can only be applied to audio blocks, not [{self.block.get_type()}]")
        if self.block.get_audio() is None:
            self.block.set_audio(AudioFileClip(self.block.configuration["file_path"]))

        audio = None
        subclip_start = self.configuration.get('subclip_start', None)

        if subclip_start is None or subclip_start == 0:
            audio = self.block.get_audio().set_start(self.time.start).set_duration(self.time.duration)
        elif subclip_start is not None and subclip_start > 0:
            audio = self.block.get_audio().subclip(subclip_start, subclip_start + self.time.duration)

        if audio.duration > self.block.time.duration and self.configuration['cut_to_block_duration']:
            audio = audio.set_duration(self.block.time.duration)

        self.block.frame.scenario.add_audio(audio)

        return Compilation(audio, mode="ignore")


class EffectFactory(AbstractEffectFactory):

    def from_yml(self, effect_yml):
        time = effect_yml.get('time', {})
        configuration = effect_yml.get('configuration', {})

        return Effect(Time(time.get('start', 0), time.get('duration', 0)), configuration)


class AudioPlayEffectModuleDefinition(AbstractModuleDefinition):
    PLUGIN_PREFIX = "plugins.core"
    PLUGIN_PREFIX_INDEX = PLUGIN_PREFIX.replace(".", "")

    EXAMPLE_DURATION = 1

    @staticmethod
    def get_description():
        return "Play audio on block."

    @staticmethod
    def get_configuration():
        return {
            "subclip_start": {
                "description": "Setting the subclip will start the audio from the given time.",
                "type": "float",
                "default": 0,
                "required": False,
            },
            "cut_to_block_duration": {
                "description": "If audio is longer than block duration, cut it to block duration.",
                "type": "bool",
                "default": True,
                "required": False
            }
        }

    @staticmethod
    def get_renders_on() -> dict:
        return {
            "block": ["audio"]
        }

    @staticmethod
    def get_examples():
        return [
            {
                "name": "Write Effect On Text Block",
                "description": "This is basic effect to display any text. It will write the text on the block.",
                "tips": [
                    "No configuration is accepted, as this effect inherits the configuration from "
                    f"[{AudioPlayEffectModuleDefinition.PLUGIN_PREFIX}.blocks.text](#{AudioPlayEffectModuleDefinition.PLUGIN_PREFIX_INDEX}blockstext).",
                ],
                "scenario": {
                    "width": 640, "height": 240, "fps": 24,
                    "frames": [
                        {
                            "type": f"{AudioPlayEffectModuleDefinition.PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": AudioPlayEffectModuleDefinition.EXAMPLE_DURATION},
                            "configuration": {"file_path": "example/assets/image/1.jpg"},
                            "effects": [
                                {"type": f"{AudioPlayEffectModuleDefinition.PLUGIN_PREFIX}.effects.frames.resize",
                                 "configuration": {"mode": "center_crop"}}],
                            "blocks": [
                                {
                                    "type": f"{AudioPlayEffectModuleDefinition.PLUGIN_PREFIX}.blocks.text",
                                    "time": {"duration": AudioPlayEffectModuleDefinition.EXAMPLE_DURATION},
                                    "position": ["center", "center"],
                                    "configuration": {"content": "Hello, World!", "color": "white"},
                                    "effects": [{
                                        "type": f"{AudioPlayEffectModuleDefinition.PLUGIN_PREFIX}.effects.blocks.text.write",
                                        "time": {"duration": AudioPlayEffectModuleDefinition.EXAMPLE_DURATION}
                                    }]
                                }
                            ]
                        }
                    ]
                },
            }
        ]
