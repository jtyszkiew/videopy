from videopy.hooks import Hooks
from unittest.mock import MagicMock, patch
from unittest import TestCase


class TestHooks(TestCase):

    def setUp(self):
        self.hooks = Hooks()

    def test_register_hook(self):
        event = 'test_event'
        function = MagicMock()

        self.hooks.register_hook(event, function)

        self.assertIn(event, self.hooks._hooks)
        self.assertIn(function, self.hooks._hooks[event])

    def test_run_hook_with_registered_hooks(self):
        event = 'test_event'
        function1 = MagicMock()
        function2 = MagicMock()

        self.hooks.register_hook(event, function1)
        self.hooks.register_hook(event, function2)

        self.hooks.run_hook(event, 42, keyword_arg='value')

        function1.assert_called_once_with(42, keyword_arg='value')
        function2.assert_called_once_with(42, keyword_arg='value')

    @patch('videopy.utils.logger.Logger.debug')
    def test_run_hook_with_no_registered_hooks(self, mock_logger_debug):
        event = 'non_existent_event'

        self.hooks.run_hook(event)

        mock_logger_debug.assert_called_once_with(f"No hooks registered for event: <<{event}>>")
