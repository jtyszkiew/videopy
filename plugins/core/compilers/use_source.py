from videopy.compilation import AbstractCompiler


class UseSourceCompiler(AbstractCompiler):

    def compile(self, compilation):
        """ This type of compiler will simply use the source as the result.

        :param compilation: Compilation object
        :return: target clip
        """
        return compilation.source
