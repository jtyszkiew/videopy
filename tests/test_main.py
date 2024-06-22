import unittest
from unittest.mock import patch

from videopy.main import run_scenario, HOOK_FRAMES_REGISTER, HOOK_SCENARIOS_REGISTER, HOOK_BLOCKS_REGISTER, \
    HOOK_EFFECTS_REGISTER, HOOK_FILE_LOADERS_REGISTER, HOOK_COMPILERS_REGISTER


class TestMain(unittest.TestCase):

    @patch('videopy.hooks.Hooks.run_hook')
    @patch('videopy.module.Registry')
    @patch('videopy.utils.loader.Loader.load_plugins')
    @patch('videopy.renderer.Renderer.render')
    def test_is_registering_hooks(self, mock_renderer_render, mock_registry, mock_load_plugins, mock_hooks_run):
        scenario = {
            'width': 1920,
            'height': 1080,
            'fps': 24,
            'output_path': 'videopy.mp4',
            'frames': []
        }

        run_scenario(
            input_content=scenario,
        )

        mock_hooks_run.assert_any_call(HOOK_SCENARIOS_REGISTER, {})
        mock_hooks_run.assert_any_call(HOOK_FRAMES_REGISTER, {})
        mock_hooks_run.assert_any_call(HOOK_BLOCKS_REGISTER, {})
        mock_hooks_run.assert_any_call(HOOK_EFFECTS_REGISTER, {})
        mock_hooks_run.assert_any_call(HOOK_FILE_LOADERS_REGISTER, {})
        mock_hooks_run.assert_any_call(HOOK_COMPILERS_REGISTER, {})

        mock_renderer_render.assert_called_once()

    @patch('videopy.module.Registry.add_frame')
    @patch('videopy.module.Registry.add_block')
    @patch('videopy.module.Registry.add_effect')
    @patch('videopy.module.Registry.add_file_loader')
    @patch('videopy.module.Registry.add_compiler')
    @patch('videopy.module.Registry.add_scenario')
    @patch('videopy.hooks.Hooks.run_hook')
    @patch('videopy.utils.loader.Loader.load_plugins')
    @patch('videopy.renderer.Renderer.render')
    def test_is_using_modules(
            self,
            mock_renderer_render,
            mock_load_plugins,
            mock_run_hook,
            mock_add_scenario,
            mock_add_compiler,
            mock_add_file_loader,
            mock_add_effect,
            mock_add_block,
            mock_add_frame
    ):
        scenario = {
            'width': 1920,
            'height': 1080,
            'fps': 24,
            'output_path': 'videopy.mp4',
            'frames': []
        }

        def run_hook_side_effect(hook_name, module, *args):
            if hook_name == HOOK_FRAMES_REGISTER:
                module['frame1'] = {'description': 'frame1'}
            elif hook_name == HOOK_BLOCKS_REGISTER:
                module['block1'] = {'description': 'block1'}
            elif hook_name == HOOK_EFFECTS_REGISTER:
                module['effect1'] = {'description': 'effect1'}
            elif hook_name == HOOK_FILE_LOADERS_REGISTER:
                module['file_loader1'] = {'description': 'file_loader1'}
            elif hook_name == HOOK_COMPILERS_REGISTER:
                module['compiler1'] = {'description': 'compiler1'}
            elif hook_name == HOOK_SCENARIOS_REGISTER:
                module['scenario1'] = {'description': 'scenario1'}

        mock_run_hook.side_effect = run_hook_side_effect

        run_scenario(
            input_content=scenario,
        )

        mock_add_frame.assert_called_once()
        mock_add_block.assert_called_once()
        mock_add_effect.assert_called_once()
        mock_add_compiler.assert_called_once()
        mock_add_file_loader.assert_called_once()
        mock_add_scenario.assert_called_once()
