from moviepy.editor import concatenate_videoclips, concatenate_audioclips

from videopy.utils.file import get_file_extension
from videopy.utils.logger import Logger


class Scenario:
    def __init__(self, registry, scenario_yml, hooks, output_path="videopy.mp4", width=1920, height=1080, fps=24):
        self.frames = []
        self.audio = []
        self.total_time = 0

        self.hooks = hooks
        self.output_path = output_path
        self.size = (width, height)
        self.fps = fps
        self.registry = registry
        self.scenario_yml = scenario_yml

    def add_frame(self, frame):
        self.total_time += frame.time.start + frame.time.duration

        self.frames.append(frame)

    def add_audio(self, audio):
        self.audio.append(audio)

    def render(self):
        Logger.debug(f"Rendering scenario with <<{len(self.frames)}>> frames "
                     f"with a total time of <<{self.total_time}>> seconds")

        clips = []
        start_time = 0

        for frame in self.frames:
            Logger.debug(f"Rendering frame of type <<{frame.get_type()}>>")
            clip = frame.do_render(start_time)

            clips.append(clip)
            start_time += frame.time.duration

            if clip.duration != frame.time.duration:
                raise ValueError(f"Frame duration [{frame.time.duration}] does not match "
                                 f"the clip duration [{clip.duration}]")

        final_video = concatenate_videoclips(clips, method="compose")

        Logger.debug(f"Scenario rendered with a total time of <<{final_video.duration}>> seconds")

        if self.audio:
            Logger.debug(f"Concatenating <<{len(self.audio)}>> audio clips")

            audio = concatenate_audioclips(self.audio)
            final_video = final_video.set_audio(audio)

        format = get_file_extension(self.output_path)

        if format == "gif":
            final_video.write_gif(self.output_path, fps=self.fps)
        else:
            final_video.write_videofile(self.output_path, fps=self.fps)


class ScenarioFactory:

    @staticmethod
    def from_yml(modules_yml, scenario_yml, hooks):
        return Scenario(
            registry=modules_yml,
            scenario_yml=scenario_yml,
            hooks=hooks,
            output_path=scenario_yml['output_path'],
            width=scenario_yml['width'],
            height=scenario_yml['height'],
            fps=scenario_yml['fps']
        )
