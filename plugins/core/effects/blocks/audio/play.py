from moviepy.editor import AudioFileClip

from videopy.compilation import Compilation
from videopy.effect import AbstractEffectFactory, AbstractBlockEffect
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
