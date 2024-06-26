import unittest

from plugins.core.params.loop import LoopParamHandler
from plugins.core.params.math import MathParamHandler
from plugins.core.params.when import WhenParamHandler
from videopy.hooks import Hooks
from videopy.template import Template, HOOK_TEMPLATE_PARAM_PRE_HANDLER_REGISTER, \
    HOOK_TEMPLATE_PARAM_POST_HANDLER_REGISTER


class TestTemplate(unittest.TestCase):

    def test_values_traversing(self):
        template = Template({}, Hooks())
        keys = [
            # Dictionary
            {
                "source": {"key1": {"value1": "value", "value2": "value_{var1}"}},
                "target": {"key1": {"value1": "value", "value2": "value_var"}},
                "vars": {"var1": "var"}
            },
            # List
            {
                "source": {"key1": [{"value1": "value", "value2": "value_{var1}"}]},
                "target": {"key1": [{"value1": "value", "value2": "value_var"}]},
                "vars": {"var1": "var"}
            },
            # Multiple vars
            {
                "source": {"key1": [{"value1": "{var1}", "value2": "value_{var1}_{var2}"}]},
                "target": {"key1": [{"value1": "var", "value2": "value_var_var2"}]},
                "vars": {"var1": "var", "var2": "var2"}
            }
        ]

        for key in keys:
            template.traverse_values(key["source"], vars=key["vars"])
            self.assertEqual(key["target"], key["source"])

    def test_loop_template_handler_and_variable_inheritance(self):
        scenario = self.__scenario()
        hooks = Hooks()

        def register_loop_param_handler(params):
            params["loop"] = LoopParamHandler()

        hooks.register_hook(HOOK_TEMPLATE_PARAM_PRE_HANDLER_REGISTER, register_loop_param_handler)

        Template(scenario, hooks).process()

        # Number of elements
        self.assertEqual(len(scenario["frames"]), 2)
        self.assertEqual(len(scenario["frames"][0]["blocks"]), 2)
        self.assertEqual(len(scenario["frames"][0]["blocks"][0]["effects"]), 2)

        # Loop index and total elements
        self.assertEqual(scenario["frames"][0]["vars"]["loop_index"], 0)
        self.assertEqual(scenario["frames"][1]["vars"]["loop_index"], 1)
        self.assertEqual(scenario["frames"][0]["blocks"][0]["vars"]["loop_index"], 0)
        self.assertEqual(scenario["frames"][0]["blocks"][1]["vars"]["loop_index"], 1)
        self.assertEqual(scenario["frames"][0]["blocks"][0]["effects"][0]["vars"]["loop_index"], 0)
        self.assertEqual(scenario["frames"][0]["blocks"][0]["effects"][1]["vars"]["loop_index"], 1)
        self.assertEqual(scenario["frames"][0]["vars"]["loop_total_elements"], 2)
        self.assertEqual(scenario["frames"][0]["blocks"][0]["vars"]["loop_total_elements"], 2)
        self.assertEqual(scenario["frames"][0]["blocks"][0]["effects"][0]["vars"]["loop_total_elements"], 2)
        self.assertEqual(scenario["frames"][0]["blocks"][0]["effects"][1]["vars"]["loop_total_elements"], 2)

        # Variable propagation
        self.assertEqual(scenario["frames"][0]["vars"]["frameindex0key"], "frameindex0value")
        self.assertEqual(scenario["frames"][1]["vars"]["frameindex1key"], "frameindex1value")
        self.assertEqual(scenario["frames"][0]["blocks"][0]["vars"]["blockindex0key"], "blockindex0value")
        self.assertEqual(scenario["frames"][0]["blocks"][1]["vars"]["blockindex1key"], "blockindex1value")
        self.assertEqual(scenario["frames"][0]["blocks"][0]["effects"][0]["vars"]["effectindex0key"],
                         "effectindex0value")
        self.assertEqual(scenario["frames"][0]["blocks"][0]["effects"][1]["vars"]["effectindex1key"],
                         "effectindex1value")

        # Variable inheritance
        # Scenario -> Frame
        frame_0_vars = {
            "scenario": {"scenario1var": "scenario1value"},
            "frameindex0key": "frameindex0value",
            "loop_index": 0,
            "loop_total_elements": 2,
        }
        self.assertEqual(frame_0_vars, scenario["frames"][0]["vars"])

        # Frame -> Block
        frame_0_block_0_vars = {
            "frame": frame_0_vars,
            "blockindex0key": "blockindex0value",
            "loop_index": 0,
            "loop_total_elements": 2,
        }
        self.assertEqual(frame_0_block_0_vars, scenario["frames"][0]["blocks"][0]["vars"])

        # Block -> Effect
        frame_0_block_0_effect_0_vars = {
            "block": frame_0_block_0_vars,
            "effectindex0key": "effectindex0value",
            "loop_index": 0,
            "loop_total_elements": 2,
        }
        self.assertEqual(frame_0_block_0_effect_0_vars, scenario["frames"][0]["blocks"][0]["effects"][0]["vars"])

        # Frame -> Effect
        frame_0_effect_0_vars = {
            "frame": frame_0_vars,
            "effectindex0key": "effectindex0value",
            "loop_index": 0,
            "loop_total_elements": 2,
        }
        self.assertEqual(frame_0_effect_0_vars, scenario["frames"][0]["effects"][0]["vars"])

    def test_math_template_handler(self):
        scenario = self.__scenario()
        hooks = Hooks()

        scenario["frames"][0]["vars"] = {}
        scenario["frames"][0]["vars"]["computable"] = 4

        scenario["frames"][0]["math"] = [
            {"name": "mathvar1", "calculate": "2*2"},
            {"name": "mathvar2", "calculate": "computable * 2"},
        ]

        def register_math_param_handler(params):
            params["math"] = MathParamHandler()

        hooks.register_hook(HOOK_TEMPLATE_PARAM_PRE_HANDLER_REGISTER, register_math_param_handler)

        Template(scenario, hooks).process()

        self.assertEqual(scenario["frames"][0]["vars"]["math_mathvar1"], 4)
        self.assertEqual(scenario["frames"][0]["vars"]["math_mathvar2"], 8)

    def test_when_template_handler(self):
        scenario = self.__scenario()
        hooks = Hooks()

        scenario["frames"][0]["vars"] = {}
        scenario["frames"][0]["vars"]["computable"] = {"value": 4}

        scenario["frames"][0]["when"] = "computable.value > 8"

        def register_math_param_handler(params):
            params["when"] = WhenParamHandler()

        hooks.register_hook(HOOK_TEMPLATE_PARAM_POST_HANDLER_REGISTER, register_math_param_handler)

        Template(scenario, hooks).process()

        self.assertEqual(len(scenario["frames"]), 0)

    @staticmethod
    def __scenario():
        return {
            "output_path": "videopy.output.mp4",
            "width": 1920,
            "height": 1080,
            "fps": 24,
            "vars": {
                "scenario1var": "scenario1value"
            },
            "frames": [
                {
                    "type": "dummy",
                    "time": {"start": 0, "duration": 1},
                    "loop": [{"frameindex0key": "frameindex0value"}, {"frameindex1key": "frameindex1value"}],
                    "effects": [
                        {
                            "type": "dummy",
                            "time": {"start": 0, "duration": 1},
                            "loop": [{"effectindex0key": "effectindex0value"},
                                     {"effectindex1key": "effectindex1value"}]
                        }
                    ],
                    "blocks": [
                        {
                            "type": "dummy",
                            "time": {"start": 0, "duration": 1},
                            "loop": [{"blockindex0key": "blockindex0value"}, {"blockindex1key": "blockindex1value"}],
                            "effects": [
                                {
                                    "type": "dummy",
                                    "time": {"start": 0, "duration": 1},
                                    "loop": [{"effectindex0key": "effectindex0value"},
                                             {"effectindex1key": "effectindex1value"}]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
