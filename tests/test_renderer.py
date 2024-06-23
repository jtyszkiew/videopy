import unittest
from unittest.mock import MagicMock, patch

from videopy.hooks import Hooks
from videopy.module import Registry
from videopy.renderer import Renderer, HOOK_FRAME_EFFECT_BL


class TestRenderer(unittest.TestCase):

    def setUp(self):
        self.registry = MagicMock(spec=Registry)
        self.hooks = MagicMock(spec=Hooks)

        self.registry.blocks = {'block_type': {}}
        self.registry.effects = {'effect_type': {}}
        self.registry.frames = {'frame_type': {}}
        self.registry.file_loaders = {'file_loader_type': {}}

        self.scenario_yml = {
            'frames': [
                {
                    'type': 'frame_type',
                    'effects': [{'type': 'effect_type'}],
                    'blocks': [
                        {
                            'type': 'block_type',
                            'effects': [{'type': 'effect_type'}]
                        }
                    ]
                }
            ]
        }
        self.renderer = Renderer(self.scenario_yml, self.registry, self.hooks)

    @patch('videopy.scenario.ScenarioFactory.from_yml')
    @patch('videopy.utils.loader.Loader.get_frame_factory')
    @patch('videopy.utils.loader.Loader.get_effect_factory')
    @patch('videopy.utils.loader.Loader.get_block_factory')
    @patch('videopy.utils.loader.Loader.load_defaults')
    def test_render(self, mock_load_defaults, mock_get_block_factory, mock_get_effect_factory, mock_get_frame_factory,
                    mock_from_yml):
        # Mocks
        mock_scenario = MagicMock()
        mock_from_yml.return_value = mock_scenario

        mock_frame_factory = MagicMock()
        mock_get_frame_factory.return_value = mock_frame_factory
        mock_frame = MagicMock()
        mock_frame_factory().from_yml.return_value = mock_frame

        mock_effect_factory = MagicMock()
        mock_get_effect_factory.return_value = mock_effect_factory
        mock_effect = MagicMock()
        mock_effect_factory().from_yml.return_value = mock_effect

        mock_block_factory = MagicMock()
        mock_get_block_factory.return_value = mock_block_factory
        mock_block = MagicMock()
        mock_block_factory().from_yml.return_value = mock_block

        # Run the method
        self.renderer.render()

        # Assertions
        mock_from_yml.assert_called_once_with(self.registry, self.scenario_yml, self.hooks)
        mock_get_frame_factory.assert_called_once_with('frame_type')
        mock_frame_factory().from_yml.assert_called_once_with(self.scenario_yml['frames'][0], mock_scenario)
        mock_get_effect_factory.assert_called_with('effect_type')
        self.assertEquals(mock_effect_factory().from_yml.call_count, 2)
        mock_effect_factory().from_yml.assert_called_with(self.scenario_yml['frames'][0]['effects'][0])
        mock_get_block_factory.assert_called_once_with('block_type')
        mock_block_factory().from_yml.assert_called_once_with(self.scenario_yml['frames'][0]['blocks'][0],
                                                              self.registry.blocks['block_type'], mock_frame)
        self.hooks.run_hook.assert_called_once_with(HOOK_FRAME_EFFECT_BL,
                                                    self.scenario_yml['frames'][0]['blocks'][0]['effects'],
                                                    self.registry.file_loaders)
        mock_effect_factory().from_yml.assert_called_with(self.scenario_yml['frames'][0]['blocks'][0]['effects'][0])
