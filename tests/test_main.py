import unittest
from unittest.mock import MagicMock, patch

from videopy.main import register_modules


class TestMain(unittest.TestCase):

    @patch('videopy.main.validate_frame')
    @patch('videopy.main.validate_block')
    @patch('videopy.main.validate_effect')
    @patch('videopy.main.validate_file_loader')
    @patch('videopy.main.validate_compiler')
    @patch('videopy.main.validate_scenario')
    def test_register_modules(self, mock_validate_scenario, mock_validate_compiler, mock_validate_file_loader,
                              mock_validate_effect, mock_validate_block, mock_validate_frame):
        hooks = MagicMock()

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

        register_modules(hooks)

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
        mock_validate_file_loader.assert_any_call(file_loaders)

        # Check that validate_compiler was called for each compiler
        for compiler in compilers.values():
            mock_validate_compiler.assert_any_call(compiler)

        # Check that validate_scenario was called for each scenario
        for scenario in scenarios.values():
            mock_validate_scenario.assert_any_call(scenario)
