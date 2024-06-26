import unittest
from unittest.mock import Mock, patch

from tests.utils.dummies import DummyFrame, create_dummy_scenario, DummyFrameEffect, DummyBlockEffect, DummyBlock, \
    DummyCompilerReturningNone
from videopy.block import AbstractBlockFactory, AbstractBlock
from videopy.clip.empty import EmptyClip
from videopy.compilation import Compilation
from videopy.exception import NoneValueError, InvalidTypeError, DurationNotMatchedError
from videopy.utils.time import Time

from moviepy.editor import TextClip


class TestBlock(unittest.TestCase):

    def test_time_is_required(self):
        with self.assertRaises(ValueError):
            DummyBlock(Time(0, 0), Mock(), Mock())

    def test_position_is_required(self):
        with self.assertRaises(ValueError):
            DummyBlock(Time(0, 5), None, Mock())

    def test_block_call_without_effects(self):
        scenario = create_dummy_scenario()
        frame = DummyFrame(Time(0, 5), scenario)
        block = DummyBlock(Time(0, 5), scenario, frame)

        with self.assertRaises(ValueError):
            block.do_render()

    def test_add_effect_time_check(self):
        block = DummyBlock(Time(0, 5), Mock(), Mock())
        effect = Mock()
        effect.time.duration = 5
        effect.time.start = 0

        block.add_effect(effect)

        with self.assertRaises(DurationNotMatchedError):
            effect.time.duration = 15
            block.add_effect(effect)  # Duration exceeds frame duration

        with self.assertRaises(DurationNotMatchedError):
            effect.time.duration = 5
            effect.time.start = 6
            block.add_effect(effect)  # Start time + duration exceeds frame duration

    def test_effects_do_render_is_called(self):
        scenario = create_dummy_scenario()
        frame = DummyFrame(Time(0, 5), scenario)
        block = DummyBlock(Time(0, 5), scenario, frame)
        effect = DummyBlockEffect('plugins.core.effects.blocks.text.dummy', Time(0, 5))
        effect_result = Compilation(EmptyClip(), EmptyClip(), "dummy")

        block.add_effect(effect)

        with patch.object(DummyBlockEffect, "render_on_block", return_value=effect_result) as mock_render:
            block.do_render()
            mock_render.assert_called_once()

    def test_block_render_is_called(self):
        scenario = create_dummy_scenario()
        frame = DummyFrame(Time(0, 5), scenario)
        block = DummyBlock(Time(0, 5), scenario, frame)
        effect = DummyBlockEffect('plugins.core.effects.blocks.text.dummy', Time(0, 5))

        block.add_effect(effect)

        with patch.object(DummyBlock, "render", return_value=None) as mock_render:
            block.do_render()
            mock_render.assert_called_once()

    def test_it_does_not_allow_effect_that_does_not_return_compilation(self):
        scenario = create_dummy_scenario()
        frame = DummyFrame(Time(0, 5), scenario)
        block = DummyBlock(Time(0, 5), scenario, frame)
        effect = DummyBlockEffect('plugins.core.effects.blocks.text.dummy', Time(0, 5))

        block.add_effect(effect)

        with patch.object(DummyBlockEffect, "render_on_block", return_value=None) as mock_render:
            with self.assertRaises(InvalidTypeError):
                block.do_render()
            mock_render.assert_called_once()

    def test_compilation_needs_to_return_clip(self):
        scenario = create_dummy_scenario(DummyCompilerReturningNone())
        frame = DummyFrame(Time(0, 5), scenario)
        block = DummyBlock(Time(0, 5), scenario, frame)
        effect = DummyBlockEffect('plugins.core.effects.blocks.text.dummy', Time(0, 5))
        effect_result = Compilation(EmptyClip(), "dummy", mode="dummy")

        block.add_effect(effect)

        with patch.object(DummyBlockEffect, "render_on_block", return_value=effect_result) as mock_render:
            with self.assertRaises(NoneValueError):
                block.do_render()
            mock_render.assert_called_once()

    def test_effect_needs_to_be_abstract_block_effect(self):
        scenario = create_dummy_scenario()
        frame = DummyFrame(Time(0, 5), scenario)
        block = DummyBlock(Time(0, 5), scenario, frame)
        effect = DummyFrameEffect('plugins.core.effects.frames.text.dummy', Time(0, 5))

        block.add_effect(effect)

        with self.assertRaises(InvalidTypeError):
            block.do_render()

    @patch("moviepy.editor.TextClip")
    def test_rendered_effect_duration_check(self, mock_text_clip):
        mock_text_clip = mock_text_clip.return_value
        mock_text_clip.duration = 8

        scenario = create_dummy_scenario()
        frame = DummyFrame(Time(0, 5), scenario)
        block = DummyBlock(Time(0, 5), scenario, frame)
        effect = DummyBlockEffect('plugins.core.effects.blocks.text.dummy', Time(0, 5))

        effect_result = Compilation(source=mock_text_clip, target=mock_text_clip, mode="dummy")

        block.add_effect(effect)

        with patch.object(DummyBlockEffect, "render_on_block", return_value=effect_result) as mock_render:
            with self.assertRaises(DurationNotMatchedError):
                block.do_render()
            mock_render.assert_called_once()

    def test_block_factory_creates_block(self):
        factory = AbstractBlockFactory()
        block_yml = {'type': 'mock_type', 'time': {'start': 0, 'duration': 10}}

        with patch.object(AbstractBlockFactory, 'from_yml', return_value=Mock(spec=AbstractBlock)) as mock_from_yml:
            block = factory.from_yml(block_yml, {}, {})
            mock_from_yml.assert_called_once_with(block_yml, {}, {})
            self.assertIsInstance(block, AbstractBlock)
