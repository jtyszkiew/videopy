from abc import abstractmethod


class Compilation:

    def __init__(self, source, target=None, mode="compose", configuration=None):
        self.source = source
        self.target = target
        self.configuration = configuration if configuration is not None else {}
        self.mode = mode

    def __str__(self):
        return f"Compilation(source={self.source}, target={self.target}, mode={self.mode}, configuration={self.configuration})"


class AbstractCompiler:

    @abstractmethod
    def compile(self, compilation):
        pass
