from videopy.compilation import AbstractCompiler


class UseTargetCompiler(AbstractCompiler):

    def compile(self, compilation):
        """ This type of compiler will replace the source clip with the target clip.

        :param compilation: Compilation object
        :return: target clip
        """
        return compilation.target
