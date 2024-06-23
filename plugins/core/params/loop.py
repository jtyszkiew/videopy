import copy

from videopy.param import AbstractParamHandler


class LoopParamHandler(AbstractParamHandler):

    def __init__(self):
        super().__init__("loop", ["frame", "block", "effect"])

    def handle(self, parent_obj, current_obj):
        loop_items = current_obj[self.name]

        if isinstance(parent_obj, list):
            index = parent_obj.index(current_obj)
            del parent_obj[index]

            for i, loop in enumerate(loop_items):
                new_obj = self.create_new_obj(current_obj, loop, i, total_elements=len(loop_items))
                parent_obj.insert(index + i, new_obj)

    def create_new_obj(self, current_obj, loop, index, total_elements):
        """
        Create a new object based on the current object and loop variables.
        """
        new_obj = copy.deepcopy(current_obj)
        new_obj["vars"] = self.update_vars(new_obj)

        del new_obj[self.name]

        new_obj["vars"]["loop_index"] = index
        new_obj["vars"]["loop_total_elements"] = total_elements

        self.add_loop_vars(new_obj, loop)

        return new_obj

    def update_vars(self, obj):
        """
        Ensure vars is initialized in the object.
        """
        return obj.get("vars", {}).copy()

    def add_loop_vars(self, obj, loop):
        """
        Add loop variables to the object's vars.
        """
        for key, value in loop.items():
            obj["vars"][key] = value
