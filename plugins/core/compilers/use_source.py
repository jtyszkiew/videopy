from videopy.compilation import Compiler


class UseSourceCompiler(Compiler):

    def compile(self, compilation):
        """ This type of compiler will simply use the source as the result.

        :param compilation: Compilation object
        :return: target clip
        """
        return compilation.source
