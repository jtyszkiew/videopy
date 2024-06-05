import unittest

from tests.utils.dummies import DummyCompiler
from videopy.module_validators import validate_scenario, validate_frame, validate_configuration, validate_block, \
    validate_effect, validate_file_loader, validate_compiler


class TestScenario(unittest.TestCase):

    def test_valid_configuration(self):
        valid_configuration = {
            "module1": {
                "description": "This is a module",
                "type": "str",
                "required": True
            },
            "module2": {
                "description": "This is another module",
                "type": "int",
                "required": False,
                "default": 0
            }
        }

        validate_configuration(valid_configuration)

    def test_missing_description(self):
        invalid_configuration = {
            "module1": {
                "type": "str",
                "required": True
            }
        }

        with self.assertRaisesRegex(ValueError, "Description is required in module configuration"):
            validate_configuration(invalid_configuration)

    def test_empty_description(self):
        invalid_configuration = {
            "module1": {
                "description": "",
                "type": "str",
                "required": True
            }
        }

        with self.assertRaisesRegex(ValueError, "Description is required in module configuration"):
            validate_configuration(invalid_configuration)

    def test_missing_type(self):
        invalid_configuration = {
            "module1": {
                "description": "This is a module",
                "required": True
            }
        }

        with self.assertRaisesRegex(ValueError, "Type is required in module configuration"):
            validate_configuration(invalid_configuration)

    def test_invalid_type(self):
        invalid_configuration = {
            "module1": {
                "description": "This is a module",
                "type": "invalid_type",
                "required": True
            }
        }

        with self.assertRaisesRegex(ValueError, "Type is not valid in module configuration"):
            validate_configuration(invalid_configuration)

    def test_missing_required(self):
        invalid_configuration = {
            "module1": {
                "description": "This is a module",
                "type": "str"
            }
        }

        with self.assertRaisesRegex(ValueError, "Required is required in module configuration"):
            validate_configuration(invalid_configuration)

    def test_invalid_required(self):
        invalid_configuration = {
            "some_field": {
                "description": "This is a module",
                "type": "str",
                "required": "invalid"
            }
        }

        with self.assertRaisesRegex(ValueError, "Required is not valid in module configuration"):
            validate_configuration(invalid_configuration)

    def test_missing_default_for_non_required(self):
        invalid_configuration = {
            "module1": {
                "description": "This is a module",
                "type": "str",
                "required": False
            }
        }

        with self.assertRaisesRegex(ValueError, "Default is required in module configuration"):
            validate_configuration(invalid_configuration)

    def test_validate_scenario(self):
        scenario = {}

        with self.assertRaisesRegex(ValueError, "Scenario description is required"):
            validate_scenario(scenario)

    def test_validate_frame(self):
        with self.assertRaisesRegex(ValueError, "Frame description is required"):
            validate_frame({})

        with self.assertRaisesRegex(ValueError, "Description is required in module configuration"):
            validate_frame({"description": "test", "configuration": {"test": {}}})

    def test_validate_block(self):
        with self.assertRaisesRegex(ValueError, "Block description is required"):
            validate_block({})

        with self.assertRaisesRegex(ValueError, "Description is required in module configuration"):
            validate_block({"description": "test", "configuration": {"test": {}}})

    def test_validate_effect(self):
        with self.assertRaisesRegex(ValueError, "Effect description is required"):
            validate_effect({})

        with self.assertRaisesRegex(ValueError, "Description is required in module configuration"):
            validate_effect({"description": "test", "configuration": {"test": {}}})

    def test_validate_file_loader(self):
        with self.assertRaisesRegex(ValueError, "File loader test is not callable"):
            validate_file_loader({"test": "not_callable"})

        validate_file_loader({"test": lambda: None})

    def test_validate_compiler(self):
        with self.assertRaisesRegex(ValueError, "Compiler <class 'str'> is not a subclass of AbstractCompiler"):
            validate_compiler(str)

        validate_compiler(DummyCompiler())
