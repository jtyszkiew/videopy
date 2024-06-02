import unittest
from unittest.mock import Mock, patch

from tests.utils.dummies import DummyFrame, create_dummy_scenario, DummyFrameEffect, DummyBlockEffect, DummyBlock, \
    DummyCompilerReturningNone
from videopy.block import AbstractBlockFactory, AbstractBlock
from videopy.compilation import Compilation
from videopy.exception import NoneValueError, InvalidTypeError, DurationNotMatchedError
from videopy.utils.time import Time

from moviepy.editor import TextClip


class TestEffect(unittest.TestCase):

    def test_effect_type_is_required(self):
        with self.assertRaises(ValueError):
            DummyFrameEffect(None, Time(0, 5))

    def test_effect_time_is_required(self):
        with self.assertRaises(ValueError):
            DummyFrameEffect('dummy', None)

    def test_abstract_frame_effect_is_calling_render_on_frame(self):
        effect = DummyFrameEffect('dummy', Time(0, 5))
        clip = TextClip("dummy").set_duration(5)

        with patch.object(DummyFrameEffect, "render_on_frame", return_value=clip) as mock_render:
            effect.render_on_frame(clip)
            mock_render.assert_called_once()

    def test_abstract_block_effect_is_calling_render_on_block(self):
        effect = DummyBlockEffect('dummy', Time(0, 5))
        clip = TextClip("dummy").set_duration(5)

        with patch.object(DummyBlockEffect, "render_on_block", return_value=clip) as mock_render:
            effect.render_on_block(clip)
            mock_render.assert_called_once()
