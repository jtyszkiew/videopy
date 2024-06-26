import simpleeval

from videopy.param import AbstractParamHandler


class MathParamHandler(AbstractParamHandler):
    __RESULT_KEY = "math"
    __CALCULATE_KEY = "calculate"
    __VARS_KEY = "vars"

    def __init__(self):
        super().__init__("math", ["frame", "block", "effect", "scenario"])

    def handle(self, parent_context, container_context, param_context):
        if isinstance(param_context, list):
            for obj in param_context:
                self.handle(container_context, container_context, obj)
        else:
            container_context["vars"] = container_context.get("vars", {})
            result_name = f"math_{param_context['name']}"

            container_context["vars"][result_name] = simpleeval.simple_eval(param_context["calculate"],
                                                                            names=container_context.get("vars", {}))
