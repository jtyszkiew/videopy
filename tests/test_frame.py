import unittest
from unittest.mock import Mock, patch

from tests.utils.dummies import DummyFrameEffect, DummyFrame, create_dummy_scenario, DummyBlock, DummyBlockEffect, \
    DummyCompilerReturningNone
from videopy.clip.empty import EmptyClip
from videopy.compilation import Compilation
from videopy.exception import DurationNotMatchedError, NoneValueError, InvalidTypeError
from videopy.frame import AbstractFrameFactory, AbstractFrame
from videopy.utils.time import Time
from moviepy.editor import TextClip


class TestAbstractFrame(unittest.TestCase):

    def test_time_is_required(self):
        with self.assertRaises(ValueError):
            AbstractFrame(None, Mock())

    def test_add_block_time_check(self):
        frame = DummyFrame(Time(0, 5), create_dummy_scenario())

        block = Mock()
        block.time.duration = 5
        block.time.start = 0

        frame.add_block(block)  # Should not raise error

        with self.assertRaises(DurationNotMatchedError):
            block.time.duration = 15
            frame.add_block(block)  # Duration exceeds frame duration

        with self.assertRaises(DurationNotMatchedError):
            block.time.duration = 5
            block.time.start = 6
            frame.add_block(block)  # Start time + duration exceeds frame duration

    def test_add_effect_time_check(self):
        frame = DummyFrame(Time(0, 5), create_dummy_scenario())
        effect = Mock()
        effect.time.duration = 5
        effect.time.start = 0
        frame.add_effect(effect)  # Should not raise error

        with self.assertRaises(DurationNotMatchedError):
            effect.time.duration = 15
            frame.add_effect(effect)  # Duration exceeds frame duration

        with self.assertRaises(DurationNotMatchedError):
            effect.time.duration = 5
            effect.time.start = 6
            frame.add_effect(effect)  # Start time + duration exceeds frame duration

    def test_effects_do_render_is_called(self):
        scenario = create_dummy_scenario()
        frame = DummyFrame(Time(0, 5), scenario)
        effect = DummyFrameEffect('plugins.core.effects.blocks.text.dummy', Time(0, 5))
        effect_result = Compilation(TextClip("dummy").set_duration(5), TextClip("dummy").set_duration(5), "dummy")

        frame.add_effect(effect)

        with patch.object(DummyFrameEffect, "render_on_frame", return_value=effect_result) as mock_render:
            frame.do_render(0)
            mock_render.assert_called_once()

    @patch('moviepy.editor.CompositeVideoClip')
    def test_block_do_render_is_called(self, mock_composite):
        scenario = create_dummy_scenario()
        frame = DummyFrame(Time(0, 5), scenario)
        effect = DummyBlockEffect('plugins.core.effects.blocks.text.dummy', Time(0, 5))
        block = DummyBlock(Time(0, 5), [0, 0], frame)
        block_result = Compilation(EmptyClip(), EmptyClip(), "dummy")

        block.add_effect(effect)
        frame.add_block(block)

        with patch.object(DummyBlock, "do_render", return_value=block_result) as mock_render:
            frame.do_render(0)
            mock_render.assert_called_once()

    def test_do_render_raises_error_when_frame_render_returns_none(self):
        scenario = create_dummy_scenario()
        frame = DummyFrame(Time(0, 5), scenario)

        with patch.object(DummyFrame, "render", return_value=None) as mock_render:
            with self.assertRaises(NoneValueError):
                frame.do_render(0)
            mock_render.assert_called_once()

    def test_it_does_not_allow_effect_that_does_not_return_compilation(self):
        scenario = create_dummy_scenario()
        frame = DummyFrame(Time(0, 5), scenario)
        effect = DummyFrameEffect('plugins.core.effects.frames.text.dummy', Time(0, 5))

        frame.add_effect(effect)

        with patch.object(DummyFrameEffect, "render_on_frame", return_value=None) as mock_render:
            with self.assertRaises(InvalidTypeError):
                frame.do_render(0)
            mock_render.assert_called_once()

    def test_compilation_needs_to_return_clip(self):
        scenario = create_dummy_scenario(DummyCompilerReturningNone())
        frame = DummyFrame(Time(0, 5), scenario)
        effect = DummyFrameEffect('plugins.core.effects.frames.text.dummy', Time(0, 5))
        effect_result = Compilation(TextClip("dummy").set_duration(5), "dummy", mode="dummy")

        frame.add_effect(effect)

        with patch.object(DummyFrameEffect, "render_on_frame", return_value=effect_result) as mock_render:
            with self.assertRaises(NoneValueError):
                frame.do_render(0)
            mock_render.assert_called_once()

    def test_effect_needs_to_be_abstract_block_effect(self):
        scenario = create_dummy_scenario()
        frame = DummyFrame(Time(0, 5), scenario)
        block = DummyBlock(Time(0, 5), scenario, frame)
        effect = DummyFrameEffect('plugins.core.effects.frames.text.dummy', Time(0, 5))

        block.add_effect(effect)

        with self.assertRaises(InvalidTypeError):
            block.do_render()

    def test_effect_needs_to_be_abstract_frame_effect(self):
        scenario = create_dummy_scenario()
        frame = DummyFrame(Time(0, 5), scenario)
        effect = DummyBlockEffect('plugins.core.effects.blocks.text.dummy', Time(0, 5))

        frame.add_effect(effect)

        with self.assertRaises(InvalidTypeError):
            frame.do_render(0)

    def test_effect_duration_after_render_is_checked(self):
        scenario = create_dummy_scenario()
        frame = DummyFrame(Time(0, 5), scenario)
        effect = DummyFrameEffect('plugins.core.effects.frames.text.dummy', Time(0, 5))
        effect_result = Compilation(TextClip("dummy").set_duration(5), TextClip("dummy").set_duration(6), "dummy")

        frame.add_effect(effect)

        with patch.object(DummyFrameEffect, "render_on_frame", return_value=effect_result) as mock_render:
            with self.assertRaises(DurationNotMatchedError):
                frame.do_render(0)
                mock_render.assert_called_once()

    def test_block_result_is_not_none(self):
        scenario = create_dummy_scenario(DummyCompilerReturningNone())
        frame = DummyFrame(Time(0, 5), scenario)
        block = DummyBlock(Time(0, 5), scenario, frame)
        compilation = Compilation(TextClip("dummy").set_duration(5), TextClip("dummy").set_duration(5), "dummy")

        frame.add_block(block)

        with patch.object(DummyBlock, "do_render", return_value=compilation) as mock_render:
            with self.assertRaises(NoneValueError):
                frame.do_render(0)
                mock_render.assert_called_once()

    def test_block_do_render_result_is_compilation_check(self):
        scenario = create_dummy_scenario()
        frame = DummyFrame(Time(0, 5), scenario)
        block = DummyBlock(Time(0, 5), scenario, frame)

        frame.add_block(block)

        with patch.object(DummyBlock, "do_render", return_value=None) as mock_render:
            with self.assertRaises(InvalidTypeError):
                frame.do_render(0)
                mock_render.assert_called_once()

    def test_rendered_block_duration_is_checked(self):
        scenario = create_dummy_scenario()
        frame = DummyFrame(Time(0, 5), scenario)
        block = DummyBlock(Time(0, 5), scenario, frame)
        compilation = Compilation(TextClip("dummy").set_duration(5), TextClip("dummy").set_duration(6), "dummy")

        frame.add_block(block)

        with patch.object(DummyBlock, "do_render", return_value=compilation) as mock_render:
            with self.assertRaises(DurationNotMatchedError):
                frame.do_render(0)
                mock_render.assert_called_once()

    def test_factory_creates_frame(self):
        factory = AbstractFrameFactory()
        frame_yml = {'type': 'mock_type', 'time': {'start': 0, 'duration': 10}}
        scenario = Mock()

        with patch.object(AbstractFrameFactory, 'from_yml', return_value=Mock(spec=AbstractFrame)) as mock_from_yml:
            frame = factory.from_yml(frame_yml, scenario)
            mock_from_yml.assert_called_once_with(frame_yml, scenario)
            self.assertIsInstance(frame, AbstractFrame)
