from videopy.utils.logger import Logger


class Hooks:
    def __init__(self):
        self._hooks = {}

    def register_hook(self, event, function):
        if event not in self._hooks:
            self._hooks[event] = []
        self._hooks[event].append(function)

    def run_hook(self, event, *args, **kwargs):
        if event in self._hooks:
            for function in self._hooks[event]:
                function(*args, **kwargs)
        else:
            Logger.debug(f"No hooks registered for event: <<{event}>>")
