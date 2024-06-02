import unittest
from unittest.mock import patch
from io import StringIO

from videopy.utils.logger import Logger, LoggerProvider


class DummyLoggerProvider(LoggerProvider):
    def print(self, message):
        print(message)


class TestLogger(unittest.TestCase):

    def setUp(self):
        Logger.provider = DummyLoggerProvider()

    @patch('sys.stdout', new_callable=StringIO)
    def test_info_logging(self, mock_stdout):
        Logger.set_level("info")
        Logger.enabled = True
        Logger.info("This is an <<info>> message")
        self.assertIn("[bold blue]Info:[/bold blue] This is an [bold cyan]info[/bold cyan] message",
                      mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_warn_logging(self, mock_stdout):
        Logger.set_level("warn")
        Logger.enabled = True
        Logger.warn("This is a <<warn>> message")
        self.assertIn("[bold orange]Warn:[/bold orange] This is a [bold cyan]warn[/bold cyan] message",
                      mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_error_logging(self, mock_stdout):
        Logger.set_level("info")
        Logger.enabled = True
        Logger.error("This is an <<error>> message")
        self.assertIn("[bold red]Error:[/bold red] This is an [bold cyan]error[/bold cyan] message",
                      mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_debug_logging(self, mock_stdout):
        Logger.set_level("debug")
        Logger.enabled = True
        Logger.debug("This is a <<debug>> message")
        self.assertIn("[bold green]Debug:[/bold green] This is a [bold cyan]debug[/bold cyan] message",
                      mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_trace_logging(self, mock_stdout):
        Logger.set_level("trace")
        Logger.enabled = True
        Logger.trace("This is a <<trace>> message")
        self.assertIn("[bold magenta]Trace:[/bold magenta] This is a [bold cyan]trace[/bold cyan] message",
                      mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_logging_disabled(self, mock_stdout):
        Logger.set_level("info")
        Logger.enabled = False
        Logger.info("This is an <<info>> message")
        self.assertEqual(mock_stdout.getvalue(), "")
