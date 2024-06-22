import unittest
from unittest.mock import patch, MagicMock

from tests.utils.dummies import DummyCompiler
from videopy.module import Validator, Registry


class TestRegistry(unittest.TestCase):

    @patch('videopy.module.Validator.validate_frame')
    @patch('videopy.module.Validator.validate_block')
    @patch('videopy.module.Validator.validate_effect')
    @patch('videopy.module.Validator.validate_file_loader')
    @patch('videopy.module.Validator.validate_compiler')
    @patch('videopy.module.Validator.validate_scenario')
    def test_register_modules(self, mock_validate_scenario, mock_validate_compiler, mock_validate_file_loader,
                              mock_validate_effect, mock_validate_block, mock_validate_frame):
        hooks = MagicMock()
        registry = Registry()

        frames = {'frame1': 'frame1_data'}
        blocks = {'block1': 'block1_data'}
        effects = {'effect1': 'effect1_data'}
        file_loaders = {'file_loader1': 'file_loader1_data'}
        compilers = {'compiler1': 'compiler1_data'}
        scenarios = {'scenario1': 'scenario1_data'}
        fields = {'field1': 'field1_data'}

        hooks.run_hook.side_effect = lambda hook_name, module_dict: module_dict.update(
            {'videopy.modules.frames.register': frames,
             'videopy.modules.blocks.register': blocks,
             'videopy.modules.effects.register': effects,
             'videopy.modules.file_loaders.register': file_loaders,
             'videopy.modules.compilers.register': compilers,
             'videopy.modules.scenarios.register': scenarios,
             'videopy.modules.forms.fields.register': fields}[hook_name]
        )

        registry.add_frame('frame1', frames['frame1'])
        registry.add_block('block1', blocks['block1'])
        registry.add_effect('effect1', effects['effect1'])
        registry.add_file_loader('file_loader1', file_loaders['file_loader1'])
        registry.add_compiler('compiler1', compilers['compiler1'])
        registry.add_scenario('scenario1', scenarios['scenario1'])

        # Check that validate_frame was called for each frame
        for frame in frames.values():
            mock_validate_frame.assert_any_call(frame)

        # Check that validate_block was called for each block
        for block in blocks.values():
            mock_validate_block.assert_any_call(block)

        # Check that validate_effect was called for each effect
        for effect in effects.values():
            mock_validate_effect.assert_any_call(effect)

        # Check that validate_file_loader was called
        for key, file_loader in file_loaders.items():
            mock_validate_file_loader.assert_any_call(key, file_loader)

        # Check that validate_compiler was called for each compiler
        for compiler in compilers.values():
            mock_validate_compiler.assert_any_call(compiler)

        # Check that validate_scenario was called for each scenario
        for scenario in scenarios.values():
            mock_validate_scenario.assert_any_call(scenario)


class TestValidator(unittest.TestCase):

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

        Validator.validate_configuration(valid_configuration)

    def test_missing_description(self):
        invalid_configuration = {
            "module1": {
                "type": "str",
                "required": True
            }
        }

        with self.assertRaisesRegex(ValueError, "Description is required in module configuration"):
            Validator.validate_configuration(invalid_configuration)

    def test_empty_description(self):
        invalid_configuration = {
            "module1": {
                "description": "",
                "type": "str",
                "required": True
            }
        }

        with self.assertRaisesRegex(ValueError, "Description is required in module configuration"):
            Validator.validate_configuration(invalid_configuration)

    def test_missing_type(self):
        invalid_configuration = {
            "module1": {
                "description": "This is a module",
                "required": True
            }
        }

        with self.assertRaisesRegex(ValueError, "Type is required in module configuration"):
            Validator.validate_configuration(invalid_configuration)

    def test_invalid_type(self):
        invalid_configuration = {
            "module1": {
                "description": "This is a module",
                "type": "invalid_type",
                "required": True
            }
        }

        with self.assertRaisesRegex(ValueError, "Type is not valid in module configuration"):
            Validator.validate_configuration(invalid_configuration)

    def test_missing_required(self):
        invalid_configuration = {
            "module1": {
                "description": "This is a module",
                "type": "str"
            }
        }

        with self.assertRaisesRegex(ValueError, "Required is required in module configuration"):
            Validator.validate_configuration(invalid_configuration)

    def test_invalid_required(self):
        invalid_configuration = {
            "some_field": {
                "description": "This is a module",
                "type": "str",
                "required": "invalid"
            }
        }

        with self.assertRaisesRegex(ValueError, "Required is not valid in module configuration"):
            Validator.validate_configuration(invalid_configuration)

    def test_missing_default_for_non_required(self):
        invalid_configuration = {
            "module1": {
                "description": "This is a module",
                "type": "str",
                "required": False
            }
        }

        with self.assertRaisesRegex(ValueError, "Default is required in module configuration"):
            Validator.validate_configuration(invalid_configuration)

    def test_validate_frame(self):
        with self.assertRaisesRegex(ValueError, "Frame description is required"):
            Validator.validate_frame({})

        with self.assertRaisesRegex(ValueError, "Description is required in module configuration"):
            Validator.validate_frame({"description": "test", "configuration": {"test": {}}})

    def test_validate_block(self):
        with self.assertRaisesRegex(ValueError, "Block description is required"):
            Validator.validate_block({})

        with self.assertRaisesRegex(ValueError, "Description is required in module configuration"):
            Validator.validate_block({"description": "test", "configuration": {"test": {}}})

    def test_validate_effect(self):
        with self.assertRaisesRegex(ValueError, "Effect description is required"):
            Validator.validate_effect({})

        with self.assertRaisesRegex(ValueError, "Description is required in module configuration"):
            Validator.validate_effect({"description": "test", "configuration": {"test": {}}})

    def test_validate_file_loader(self):
        with self.assertRaisesRegex(ValueError, "File loader test is not callable"):
            Validator.validate_file_loader("test", "not callable")

        Validator.validate_file_loader("test", lambda: None)

    def test_validate_compiler(self):
        with self.assertRaisesRegex(ValueError, "Compiler <class 'str'> is not a subclass of AbstractCompiler"):
            Validator.validate_compiler(str)

        Validator.validate_compiler(DummyCompiler())
