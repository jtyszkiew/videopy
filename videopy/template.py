import numexpr as ne
import re

from videopy.param import AbstractParamHandler

HOOK_FRAME_VARS_REGISTER = "videopy.template.frame.variables.register"
HOOK_FRAME_EFFECT_VARS_REGISTER = "videopy.template.frame.effect.vars.register"
HOOK_BLOCK_VARS_REGISTER = "videopy.template.block.vars.register"
HOOK_BLOCK_EFFECT_VARS_REGISTER = "videopy.template.block.effect.vars.register"


class Template:

    def __init__(self, scenario_yml, hooks):
        self.param_handlers = {}

        self.scenario_yml = scenario_yml
        self.hooks = hooks

    def traverse_values(self, obj, path="", exclude=None, vars=None):
        """
        Recursively traverse all fields of a Python object and update their values
        based on the provided vars.

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
                if key in exclude:
                    continue
                obj[key] = self.traverse_values(value, f"{path}.{key}" if path else key, exclude, vars)
        elif isinstance(obj, list):
            for index, value in enumerate(obj):
                obj[index] = self.traverse_values(value, f"{path}[{index}]", exclude, vars)
        elif hasattr(obj, "__dict__"):
            for key, value in obj.__dict__.items():
                if key in exclude:
                    continue
                setattr(obj, key, self.traverse_values(value, f"{path}.{key}" if path else key, exclude, vars))
        elif isinstance(obj, str):
            return self.resolve_placeholders(obj, vars)
        return obj

    def traverse_keys(self, obj, path="", exclude=None, vars=None):
        """
        Recursively traverse all fields of a Python object and handle special keys like 'loop'.

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

                for handler_key, handler in self.param_handlers.items():
                    if handler.name == key:
                        parent_path = self.get_parent_path(path)
                        parent_obj = None if path == "" else self.get_nested_obj(self.scenario_yml, parent_path)
                        current_obj = self.scenario_yml if path == "" else self.get_nested_obj(self.scenario_yml, path)

                        handler.handle(parent_obj, current_obj)
                else:
                    self.traverse_keys(value, f"{path}.{key}" if path else key, exclude, vars)
        elif isinstance(obj, list):
            for index, value in enumerate(obj):
                self.traverse_keys(value, f"{path}[{index}]", exclude, vars)
        elif hasattr(obj, "__dict__"):
            for key, value in obj.__dict__.items():
                if key in exclude:
                    continue
                self.traverse_keys(value, f"{path}.{key}" if path else key, exclude, vars)

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
                if re.match(r'^[a-zA-Z_]\w*(?:\.\w+)*$', expr):
                    result = self.resolve_variable(expr, vars)
                else:
                    result = ne.evaluate(expr, local_dict=vars).item()
            except KeyError as e:
                print(f"Missing key in vars for placeholder: {e}")
                result = f"{{{{ {expr} }}}}"
            except Exception as e:
                print(f"Error evaluating expression '{expr}': {e}")
                result = f"{{{{ {expr} }}}}"
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
            print(f"Missing key in vars for variable: {e}")
            return f"{{{{ {expr} }}}}"
        return value

    def resolve_all_vars(self, vars):
        """
        Resolve all variable references in the vars dictionary.

        :param vars: Dictionary containing variable values.
        :return: The vars dictionary with all placeholders resolved.
        """
        resolved_vars = {}
        for key, value in vars.items():
            if isinstance(value, str):
                resolved_vars[key] = self.resolve_placeholders(value, {**resolved_vars, **vars})
            elif isinstance(value, dict):
                resolved_vars[key] = self.resolve_all_vars(value)
            else:
                resolved_vars[key] = value
        return resolved_vars

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

    def process(self):
        self.hooks.run_hook("videopy.template.handlers.register", self.param_handlers)

        for key, handler in self.param_handlers.items():
            if not isinstance(handler, AbstractParamHandler):
                raise ValueError(f"Handler {handler} is not an instance of ParamHandler")

        self.traverse_keys(self.scenario_yml, exclude=[])

        scenario_context = {}
        scenario_context.update(self.scenario_yml.get("vars", {}))

        self.traverse_values(self.scenario_yml, exclude=["frames"], vars=scenario_context)

        previous_frame_start = 0
        previous_frame_duration = 0
        previous_frame_end = 0
        for frame in self.scenario_yml["frames"]:
            frame_time = frame["time"]
            frame_vars = frame.get("vars", {})

            frame_vars["previous_frame_start"] = previous_frame_start
            frame_vars["previous_frame_duration"] = previous_frame_duration
            frame_vars["previous_frame_end"] = previous_frame_end

            self.hooks.run_hook(HOOK_FRAME_VARS_REGISTER, frame_vars, frame, self.scenario_yml)
            self.traverse_values(frame, exclude=["blocks"], vars=frame_vars)

            previous_frame_effect_start = 0
            previous_frame_effect_duration = 0
            previous_frame_effect_end = 0
            for frame_effect in frame["effects"]:
                frame_effect_time = frame_effect.get("time", None)
                frame_effect_vars = frame_effect.get("vars", {})

                frame_effect_vars["previous_effect_start"] = previous_frame_effect_start
                frame_effect_vars["previous_effect_duration"] = previous_frame_effect_duration
                frame_effect_vars["previous_effect_end"] = previous_frame_effect_end

                frame_effect_vars["frame_start"] = frame_time.get("start", 0)
                frame_effect_vars["frame_duration"] = frame_time["duration"]
                frame_effect_vars["frame_end"] = frame_time.get("start", 0) + frame_time["duration"]

                self.hooks.run_hook(HOOK_FRAME_EFFECT_VARS_REGISTER, frame_vars, frame_effect, self.scenario_yml)
                self.traverse_values(frame_effect, vars=frame_effect_vars)

                if frame_effect_time is not None:
                    previous_frame_effect_start = frame_effect_time.get("start", 0)
                    previous_frame_effect_duration = frame_effect_time["duration"]
                    previous_frame_effect_end = frame_effect_time.get("start", 0) + frame_effect_time["duration"]

            previous_block_start = 0
            previous_block_duration = 0
            previous_block_end = 0
            for block in frame["blocks"]:
                block_time = block["time"]
                block_vars = block.get("vars", {})

                block_vars["previous_block_start"] = previous_block_start
                block_vars["previous_block_duration"] = previous_block_duration
                block_vars["previous_block_end"] = previous_block_end

                block_vars["frame_start"] = frame_time.get("start", 0)
                block_vars["frame_duration"] = frame_time["duration"]
                block_vars["frame_end"] = frame_time.get("start", 0) + frame_time["duration"]

                self.hooks.run_hook(HOOK_BLOCK_VARS_REGISTER, block_vars, block, self.scenario_yml)
                self.traverse_values(block, vars=block_vars)

                previous_block_start = block_time.get("start", 0)
                previous_block_duration = block_time["duration"]
                previous_block_end = block_time.get("start", 0) + block_time["duration"]

                previous_effect_start = 0
                previous_effect_duration = 0
                previous_effect_end = 0
                for effect in block["effects"]:
                    effect_time = effect["time"]
                    effect_vars = effect.get("vars", {})

                    effect_vars["previous_effect_start"] = previous_effect_start
                    effect_vars["previous_effect_duration"] = previous_effect_duration
                    effect_vars["previous_effect_end"] = previous_effect_end

                    effect_vars["block_start"] = block_time.get("start", 0)
                    effect_vars["block_duration"] = block_time["duration"]
                    effect_vars["block_end"] = block_time.get("start", 0) + block_time["duration"]

                    effect_vars["frame_start"] = frame_time.get("start", 0)
                    effect_vars["frame_duration"] = frame_time["duration"]
                    effect_vars["frame_end"] = frame_time.get("start", 0) + frame_time["duration"]

                    self.hooks.run_hook(HOOK_BLOCK_EFFECT_VARS_REGISTER, effect_vars, effect, self.scenario_yml)
                    self.traverse_values(effect, vars=effect_vars)

                    previous_effect_start = effect_time.get("start")
                    previous_effect_duration = effect_time["duration"]
                    previous_effect_end = effect_time.get("start", 0) + effect_time["duration"]

            previous_frame_start = frame_time.get("start", 0)
            previous_frame_duration = frame_time["duration"]
            previous_frame_end = frame_time.get("start", 0) + frame_time["duration"]
