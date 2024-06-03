from videopy.compilation import Compiler
from moviepy.editor import concatenate_videoclips


class ConcatenateCompiler(Compiler):

    def compile(self, compilation):
        """ This type of compiler will concatenate clips.

        :param compilation: Compilation object
        :return: CompositeVideoClip
        """
        return concatenate_videoclips([compilation.source, compilation.target])
