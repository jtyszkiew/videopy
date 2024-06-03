from types import NoneType

from videopy.compilation import Compilation, Compiler
from moviepy.editor import CompositeVideoClip


class ComposeCompiler(Compiler):

    def compile(self, compilation: Compilation):
        """ This type of compiler will compose/stack clips on top of each other.
        If the source is a list, it will concatenate the clips in the list.
        If the target is not None, it will stack the source and target clips on top of each other.

        :param compilation: Compilation object
        :return: CompositeVideoClip
        """
        size = compilation.configuration.get('size', None)

        if not isinstance(compilation.source, list) and not isinstance(compilation.target, NoneType):
            return CompositeVideoClip(
                clips=[compilation.source, compilation.target],
                size=size
            )
        elif isinstance(compilation.source, list) and isinstance(compilation.target, NoneType):
            return CompositeVideoClip(
                clips=compilation.source,
                size=size
            )
        else:
            raise ValueError("Invalid compilation source and target")

