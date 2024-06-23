import unittest

from videopy.hooks import Hooks
from videopy.template import Template


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
            },
            # Math
            {
                "source": {"key1": [{"value1": "{var1*2}", "value2": "value_{var1*2}", "value3": "{var1+4}", "value4": "{var1-2}"}]},
                "target": {"key1": [{"value1": "4", "value2": "value_4", "value3": "6", "value4": "0"}]},
                "vars": {"var1": 2}
            },
        ]

        for key in keys:
            template.traverse_values(key["source"], vars=key["vars"])
            self.assertEqual(key["target"], key["source"])
