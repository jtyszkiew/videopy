from videopy.compilation import Compilation
from videopy.effect import AbstractEffectFactory, AbstractBlockEffect
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

        # Create a clip that fades in from the specified start time
        faded_clip = crossfadein(clip.subclip(self.block.time.start), self.time.duration)
        # Create a clip that plays normally before the start time
        initial_clip = clip.subclip(0, self.block.time.start)

        # Combine the initial part and the faded part
        return Compilation(source=initial_clip, target=faded_clip.set_start(self.block.time.start), mode="compose")


class EffectFactory(AbstractEffectFactory):
    def from_yml(self, effect_yml):
        configuration = effect_yml.get('configuration', {})
        time = effect_yml.get('time', {})

        if time.get('start', 0) > 0:
            Logger.warn(f"The <<time.start>> parameter for <<fadein>> effect is useless and will be ignored")

        return Effect(Time(time.get('start', 0), time.get('duration', 0)),
                      configuration.get('initial_color', [0, 0, 0]))
