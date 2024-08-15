import unittest
from typer.testing import CliRunner
from video import app

runner = CliRunner()


class TestVideopy(unittest.TestCase):

    def test_scenarios_listing(self):
        result = runner.invoke(app, ["scenarios"])

        assert result.exit_code == 0
        assert "images_dir_to_video" in result.stdout

    def test_scenario_detail(self):
        result = runner.invoke(app, ["scenarios", "images_dir_to_video"])

        assert result.exit_code == 1

    def test_frames_listing(self):
        result = runner.invoke(app, ["frames"])

        assert result.exit_code == 0
        assert "plugins.core.frames.image" in result.stdout

    def test_frame_detail(self):
        result = runner.invoke(app, ["frames", "plugins.core.frames.image"])

        assert result.exit_code == 0
        assert "plugins.core.frames.image: This block will display image." in result.stdout

    def test_blocks_listing(self):
        result = runner.invoke(app, ["blocks"])

        assert result.exit_code == 0
        assert "plugins.core.blocks.text" in result.stdout

    def test_block_detail(self):
        result = runner.invoke(app, ["blocks", "plugins.core.blocks.text"])

        assert result.exit_code == 0
        assert "plugins.core.blocks.text: This block will display text." in result.stdout

    def test_effects_listing(self):
        result = runner.invoke(app, ["effects"])

        assert result.exit_code == 0
        assert "plugins.core.effects.blocks" in result.stdout

    def test_effect_detail(self):
        result = runner.invoke(app, ["effects", "plugins.core.effects.blocks.text.background"])

        assert result.exit_code == 0
        assert "plugins.core.effects.blocks.text.background: Write text on a block." in result.stdout
