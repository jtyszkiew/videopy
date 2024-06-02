import numpy as np
import random
from moviepy.editor import VideoFileClip
from videopy.compilation import Compilation
from videopy.effect import AbstractFrameEffect, AbstractEffectFactory
from videopy.utils.time import Time
from PIL import Image


class Effect(AbstractFrameEffect):

    def __init__(self, time, configuration):
        super().__init__("bouncein", time)
        self.configuration = configuration
        self.randomize_shrink_factor = configuration.get('randomize_shrink_factor', False)
        if self.randomize_shrink_factor:
            self.random_shrink_factors = self._generate_random_shrink_factors(configuration['bounces'],
                                                                              configuration['shrink_factor'])
        else:
            self.random_shrink_factors = [configuration['shrink_factor']] * configuration['bounces']

    def render_on_frame(self, clip):
        return Compilation(
            self.__bouncein(clip, self.time.duration, self.configuration['bounces']),
            mode="use_source"
        )

    def _generate_random_shrink_factors(self, bounces, shrink_factor):
        """Generate random shrink factors for each bounce."""
        return [shrink_factor * random.uniform(0.6, 1.4) for _ in range(bounces)]

    def __bouncein(self, clip, duration, bounces):
        """Applies a bounce-in effect with shrinking on a single clip.

        Args:
            clip (VideoFileClip): The video clip.
            duration (float): Duration of the bounce-in effect.
            bounces (int): Number of bounces.

        Returns:
            VideoClip: The final video clip with the bounce-in and shrink effect.
        """

        def make_frame(get_frame, t):
            """Generates the frame at time t."""
            alpha = min(1, t / duration)
            shrink_offset = self.__shrink(t, duration, bounces)
            frame = get_frame(t)
            h, w, _ = frame.shape
            new_h = int(h * (1 - shrink_offset))
            new_w = int(w * (1 - shrink_offset))

            # Resize the frame to the new dimensions
            resized_frame = np.array(frame).astype(np.uint8)
            resized_frame = np.array(Image.fromarray(resized_frame).resize((new_w, new_h)))

            # Create a new frame with the same dimensions and insert the resized frame into the center
            new_frame = np.zeros_like(frame)
            top = (h - new_h) // 2
            left = (w - new_w) // 2
            new_frame[top:top + new_h, left:left + new_w] = resized_frame

            return (alpha * new_frame).astype(np.uint8)

        return clip.fl(make_frame)

    def __shrink(self, t, duration, bounces):
        """Creates a shrinking effect with optional random shrink factors.

        Args:
            t (float): Current time.
            duration (float): Duration of the effect.
            bounces (int): Number of bounces.

        Returns:
            float: Shrink factor at time t.
        """
        t_normalized = t / duration
        if t_normalized >= 1:
            return 0
        current_bounce = int(t_normalized * bounces)
        bounce_shrink_factor = self.random_shrink_factors[current_bounce]
        return bounce_shrink_factor * (1 - np.cos(np.pi * (t_normalized * bounces - current_bounce)))


class EffectFactory(AbstractEffectFactory):

    def from_yml(self, effect_yml):
        configuration = effect_yml.get('configuration', {})
        time = effect_yml.get('time', {})

        return Effect(Time(time.get('start', 0), time.get('duration', 0)), configuration)
