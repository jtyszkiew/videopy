from moviepy.editor import ImageClip

from videopy.frame import AbstractFrame, AbstractFrameFactory
from videopy.utils.time import Time


class Frame(AbstractFrame):

    def __init__(self, time, configuration, scenario):
        super().__init__(time, scenario)

        self.configuration = configuration

    def get_type(self):
        return 'image'

    def render(self, relative_start_time):
        return ImageClip(self.configuration['file_path'], duration=self.time.duration)


class FrameFactory(AbstractFrameFactory):

    def from_yml(self, frame_yml, scenario):
        configuration = frame_yml['configuration']
        time_yml = frame_yml.get('time', {})

        return Frame(Time(time_yml.get('start', 0), time_yml.get('duration', 1)), configuration, scenario)
