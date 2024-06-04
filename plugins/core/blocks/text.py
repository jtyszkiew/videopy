from moviepy.editor import TextClip

from videopy.block import AbstractBlock, AbstractBlockFactory
from videopy.compilation import Compilation
from videopy.utils.time import Time
from videopy.utils.utils import get_position_with_padding, transform_position


class Block(AbstractBlock):

    def get_type(self):
        return "text"

    def __init__(self, time, position, configuration, frame):
        super().__init__(time, position, frame)

        self.configuration = configuration

    def __str__(self):
        return f"Block(time={self.time}, position={self.position}, configuration={self.configuration})"

    def get_text_size(self):
        clip = TextClip(
            txt=self.configuration['content'],
            font=self.configuration['font'],
            fontsize=self.configuration['size']
        )

        return clip.size

    def get_text_position(self):
        """This method will calculate the text position based on the block position and padding."""
        x, y = transform_position(
            position=self.position,
            frame=self.frame.scenario.size,
            block=self.get_text_size(),
            margin=self.configuration['margin']
        )

        return x, y

    def render(self, clip):
        return Compilation(clip, mode="use_source")


class BlockFactory(AbstractBlockFactory):

    def from_yml(self, block_yml, module_yml, frame):
        time = block_yml.get('time', {})

        return Block(Time(time.get('start', 0), time['duration']),
                     block_yml['position'], block_yml['configuration'], frame)
