from videopy.block import AbstractBlock, AbstractBlockFactory
from videopy.compilation import Compilation
from videopy.utils.time import Time


class Block(AbstractBlock):

    def get_type(self):
        return "text"

    def __init__(self, time, position, configuration, frame):
        super().__init__(time, position, frame)

        self.configuration = configuration
        self.size = None

    def __str__(self):
        return f"Block(time={self.time}, position={self.position}, configuration={self.configuration})"

    def render(self, clip):
        return Compilation(clip, mode="use_source")


class BlockFactory(AbstractBlockFactory):

    def from_yml(self, block_yml, module_yml, frame):
        time = block_yml.get('time', {})

        return Block(Time(time.get('start', 0), time['duration']),
                     block_yml['position'], block_yml['configuration'], frame)
