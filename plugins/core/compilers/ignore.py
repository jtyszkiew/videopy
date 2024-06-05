from videopy.clip.empty import EmptyClip
from videopy.compilation import AbstractCompiler


class IgnoreCompiler(AbstractCompiler):

    def compile(self, compilation):
        return EmptyClip()
