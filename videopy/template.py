import re

from videopy.param import AbstractParamHandler

HOOK_FRAME_VARS_REGISTER = "videopy.template.frame.variables.register"
HOOK_FRAME_EFFECT_VARS_REGISTER = "videopy.template.frame.effect.vars.register"
HOOK_BLOCK_VARS_REGISTER = "videopy.template.block.vars.register"
HOOK_BLOCK_EFFECT_VARS_REGISTER = "videopy.template.block.effect.vars.register"

HOOK_TEMPLATE_PARAM_PRE_HANDLER_REGISTER = "videopy.template.params.pre_handlers.register"
HOOK_TEMPLATE_PARAM_POST_HANDLER_REGISTER = "videopy.template.params.post_handlers.register"


class Template:

    def __init__(self, scenario_yml, hooks):
        self.scenario_yml = scenario_yml
        self.hooks = hooks

    def traverse_values(self, obj, path="", exclude=None, vars=None):
        """
        Recursively traverse all fields of a Python object and update their values
        based on the provided vars.

        :param handlers:
        :param obj: The object to traverse.
        :param path: The current path of traversal.
        :param exclude: List of keys to exclude from traversal.
        :param vars: Dictionary of variables to use for replacing placeholders.
        """
        if vars is None:
            vars = {}
        if exclude is None:
            exclude = []

        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "vars":
                    vars.update(value)
                if key in exclude:
                    continue
                obj[key] = self.traverse_values(value, f"{path}.{key}" if path else key, exclude, vars=vars)
        elif isinstance(obj, list):
            for index, value in enumerate(obj):
                if isinstance(value, dict) and "vars" in value:
                    vars.update(value["vars"])

                obj[index] = self.traverse_values(value, f"{path}[{index}]", exclude, vars=vars)
        elif hasattr(obj, "__dict__"):
            for key, value in obj.__dict__.items():
                if key in exclude:
                    continue
                setattr(obj, key, self.traverse_values(value, f"{path}.{key}" if path else key, exclude, vars=vars))
        elif isinstance(obj, str):
            return self.resolve_placeholders(obj, vars=vars)
        return obj

    def traverse_keys(self, obj, handlers, path="", exclude=None, vars=None):
        """
        Recursively traverse all fields of a Python object and handle special keys like 'loop'.

        :param handlers:
        :param obj: The object to traverse.
        :param path: The current path of traversal.
        :param exclude: List of keys to exclude from traversal.
        :param vars: Dictionary of variables to use for processing keys.
        """
        if vars is None:
            vars = {}
        if exclude is None:
            exclude = []

        if isinstance(obj, dict):
            items = list(obj.items())
            for key, value in items:
                if key in exclude:
                    continue

                for handler_key, handler in handlers.items():
                    if handler.name == key:
                        parent_path = self.get_parent_path(path)
                        parent_obj = None if path == "" else self.get_nested_obj(self.scenario_yml, parent_path)
                        current_obj = self.scenario_yml if path == "" else self.get_nested_obj(self.scenario_yml, path)

                        handler.handle(parent_obj, current_obj, value)
                else:
                    self.traverse_keys(value, handlers, f"{path}.{key}" if path else key, exclude, vars)
        elif isinstance(obj, list):
            for index, value in enumerate(obj):
                self.traverse_keys(value, handlers, f"{path}[{index}]", exclude, vars)
        elif hasattr(obj, "__dict__"):
            for key, value in obj.__dict__.items():
                if key in exclude:
                    continue
                self.traverse_keys(value, handlers, f"{path}.{key}" if path else key, exclude, vars)

    def get_nested_obj(self, obj, path):
        """
        Get the nested object based on the path.

        :param obj: The root object.
        :param path: The path to the nested object.
        :return: The nested object.
        """
        keys = re.split(r'\.|\[|\]', path)
        keys = [key for key in keys if key]  # Remove empty strings
        for key in keys:
            if key.isdigit():
                key = int(key)
            obj = obj[key]
        return obj

    def resolve_placeholders(self, value, vars):
        """
        Replace placeholders in the value using vars and evaluate expressions if needed.

        :param value: The string value containing placeholders.
        :param vars: Dictionary containing variable values.
        :return: The processed string value with placeholders replaced.
        """

        def eval_placeholder(match):
            expr = match.group(1).strip()
            try:
                result = self.resolve_variable(expr, vars)
            except KeyError as e:
                print(f"Missing key in vars for placeholder: {e}")
                result = f"{expr}"
            except Exception as e:
                print(f"Error evaluating expression '{expr}': {e}")
                result = f"{expr}"
            return str(result)

        pattern = re.compile(r'{(.*?)}')
        value = pattern.sub(eval_placeholder, value)
        return value

    def resolve_variable(self, expr, vars):
        """
        Resolve a nested variable from the vars dictionary.

        :param expr: The expression containing the variable.
        :param vars: Dictionary containing variable values.
        :return: The resolved variable value.
        """
        keys = expr.split('.')
        value = vars
        try:
            for key in keys:
                value = value[key]
        except KeyError as e:
            print(expr, vars)
            print(f"Missing key in vars for variable: {e}")
            return f"{{{{ {expr} }}}}"
        return value

    def get_parent_path(self, path):
        """
        Get the parent path of a given path.

        :param path: The path to get the parent path for.
        :return: The parent path.
        """
        if '[' in path and ']' in path:
            path = re.sub(r'\[\d+\]$', '', path)
        elif '.' in path:
            path = path.rsplit('.', 1)[0]
        else:
            path = ''
        return path

    def inherit_vars(self):
        scenario_vars = self.scenario_yml.get("vars", {})

        for frame in self.scenario_yml.get("frames", []):
            if "vars" not in frame:
                frame["vars"] = {}

            frame["vars"]["scenario"] = scenario_vars

            for frame_effect in frame.get("effects", []):
                if "vars" not in frame_effect:
                    frame_effect["vars"] = {}

                frame_effect["vars"]["frame"] = frame["vars"]

            for block in frame.get("blocks", []):
                if "vars" not in block:
                    block["vars"] = {}

                block["vars"]["frame"] = frame["vars"]

                for effect in block.get("effects", []):
                    if "vars" not in effect:
                        effect["vars"] = {}

                    effect["vars"]["block"] = block["vars"]

    def process(self):
        pre_handlers = {}
        post_handlers = {}

        # Pre/Post handlers are simply groups of handlers ran each after the other
        self.hooks.run_hook(HOOK_TEMPLATE_PARAM_PRE_HANDLER_REGISTER, pre_handlers)
        self.hooks.run_hook(HOOK_TEMPLATE_PARAM_POST_HANDLER_REGISTER, post_handlers)

        for key, handler in pre_handlers.items():
            if not isinstance(handler, AbstractParamHandler):
                raise ValueError(f"Handler {handler} is not an instance of ParamHandler")

        for key, handler in post_handlers.items():
            if not isinstance(handler, AbstractParamHandler):
                raise ValueError(f"Handler {handler} is not an instance of ParamHandler")

        scenario_context = {}
        scenario_context.update(self.scenario_yml.get("vars", {}))

        self.traverse_keys(self.scenario_yml, pre_handlers, vars=scenario_context)
        self.inherit_vars()
        self.traverse_values(self.scenario_yml, vars=scenario_context)
        self.traverse_keys(self.scenario_yml, post_handlers, vars=scenario_context)
        self.traverse_values(self.scenario_yml, vars=scenario_context)
