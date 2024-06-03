from videopy.clip.empty import EmptyClip
from videopy.compilation import Compiler


class IgnoreCompiler(Compiler):

    def compile(self, compilation):
        return EmptyClip()
