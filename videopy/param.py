from abc import abstractmethod

handle_types = ['scenario', 'frame', 'block', 'effect']


class AbstractParamHandler:

    def __init__(self, name, handles):
        if not name:
            raise ValueError("Param name is required")
        for handle in handles:
            if handle not in handle_types:
                raise ValueError(f"Handle type {handle} is not valid")

        self.name = name
        self.handles = handles

    @abstractmethod
    def handle(self, parent_context, container_context, param_context):
        """ Handle the param data.

        :param parent_context: The parent context of the param data.
        :param container_context: The parent context of the param data.
        :param param_context: The param data.
        """
        pass
