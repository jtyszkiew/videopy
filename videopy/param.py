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
    def handle(self, parent_obj, current_obj):
        pass
