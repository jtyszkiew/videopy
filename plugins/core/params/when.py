import simpleeval

from videopy.param import AbstractParamHandler


class WhenParamHandler(AbstractParamHandler):

    def __init__(self):
        super().__init__("when", ["frame", "block", "effect"])

    def handle(self, parent_context, container_context, param_context):
        condition = param_context

        if condition is not None:
            result = simpleeval.simple_eval(param_context, names=container_context.get("vars", {}))

            if result is False:
                index = parent_context.index(container_context)
                del parent_context[index]
