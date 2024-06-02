from videopy.block import AbstractBlock, AbstractBlockFactory
from videopy.compilation import Compilation
from videopy.utils.time import Time


class Block(AbstractBlock):

    def __init__(self, time, configuration, frame):
        super().__init__(time, [0, 0], frame)

        self.__audio = None

        self.configuration = configuration
        self.current_time = 0

    def get_type(self):
        return "audio"

    def render(self, clip):
        return Compilation(clip, mode="ignore")

    def set_audio(self, audio):
        if self.__audio is not None:
            raise Exception("Audio is already set")

        self.__audio = audio

    def get_audio(self):
        return self.__audio


class BlockFactory(AbstractBlockFactory):
    def from_yml(self, block_yml, module_yml, frame):
        time = block_yml.get('time', {})

        return Block(Time(time.get('start', 0), time['duration']), block_yml['configuration'], frame)
