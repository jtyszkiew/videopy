from videopy.frame import AbstractFrame, AbstractFrameFactory
from videopy.utils.time import Time
from moviepy.editor import VideoFileClip


class Frame(AbstractFrame):

    def __init__(self, time, configuration, scenario):
        super().__init__(time, scenario)

        self.file_path = configuration["file_path"]
        self.mute = configuration.get("mute", False)
        self.subclip_start = configuration.get("subclip_start", 0)
        self.cut_to_frame_duration = configuration.get("cut_to_frame_duration", True)

    def get_type(self):
        return "video"

    def render(self, relative_start_time):
        clip = VideoFileClip(
            filename=self.file_path,
            audio=(not self.mute),
        )

        if self.subclip_start:
            clip = clip.subclip(self.subclip_start, self.subclip_start + self.time.duration)
        if self.time.duration < clip.duration and self.cut_to_frame_duration:
            clip = clip.set_duration(self.time.duration)

        return clip


class FrameFactory(AbstractFrameFactory):
    def from_yml(self, frame_yml, scenario):
        time_yml = frame_yml.get("time", {})

        return Frame(Time(time_yml.get("start", 0), time_yml.get("duration", 1)), frame_yml['configuration'], scenario)
