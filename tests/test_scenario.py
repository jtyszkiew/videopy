import unittest
from unittest.mock import patch

from tests.utils.dummies import DummyFrame
from videopy.hooks import Hooks
from videopy.scenario import ScenarioFactory

from videopy.utils.time import Time


class TestScenario(unittest.TestCase):

    def test_scenario_factory_should_create_scenario_with_given_data(self):
        scenario = {
            "output_path": "video_yml.output.mp4",
            "width": 1920,
            "height": 1080,
            "fps": 24,
            "debug": False
        }

        scenario = ScenarioFactory.from_yml([], scenario, Hooks())

        assert scenario.output_path == "video_yml.output.mp4"
        assert scenario.size == (1920, 1080)
        assert scenario.fps == 24
        assert len(scenario.frames) == 0
        assert len(scenario.audio) == 0
        assert scenario.total_time == 0

    @patch('moviepy.video.VideoClip.VideoClip.write_videofile')
    @patch("moviepy.editor.TextClip")
    def test_scenario_should_call_frame_render_method(self, mock_text_clip, mock_write_videofile, ):
        mock_text_clip = mock_text_clip.return_value
        mock_text_clip.duration = 1

        scenario = {
            "output_path": "videopy.output.mp4",
            "width": 1920,
            "height": 1080,
            "fps": 24,
            "debug": False
        }

        scenario = ScenarioFactory.from_yml([], scenario, Hooks())
        frame = DummyFrame(Time(0, 1), scenario)

        with patch.object(DummyFrame, "render", return_value=mock_text_clip) as mock_render:
            scenario.add_frame(frame)
            scenario.render()

            mock_render.assert_called_once_with(0)

        mock_write_videofile.assert_called_once_with("videopy.output.mp4", fps=24)
