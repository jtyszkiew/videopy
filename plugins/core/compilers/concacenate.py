from videopy.compilation import AbstractCompiler
from moviepy.editor import concatenate_videoclips


class ConcatenateCompiler(AbstractCompiler):

    def compile(self, compilation):
        """ This type of compiler will concatenate clips.

        :param compilation: Compilation object
        :return: CompositeVideoClip
        """
        return concatenate_videoclips([compilation.source, compilation.target])
