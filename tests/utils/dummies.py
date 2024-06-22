from videopy.block import AbstractBlock
from videopy.compilation import AbstractCompiler, Compilation
from videopy.effect import AbstractFrameEffect, AbstractBlockEffect
from videopy.frame import AbstractFrame
from moviepy.editor import TextClip

from videopy.hooks import Hooks
from videopy.module import Registry
from videopy.scenario import ScenarioFactory


def create_dummy_scenario(compiler=None):
    if compiler is None:
        compiler = DummyCompiler()

    registry = Registry()

    registry.add_compiler("dummy", compiler)

    scenario = {
        "output_path": "video_yml.output.mp4",
        "width": 1920,
        "height": 1080,
        "fps": 24,
        "debug": False
    }

    return ScenarioFactory.from_yml(registry, scenario, Hooks())


class DummyFrame(AbstractFrame):

    def __init__(self, time, scenario):
        super().__init__(time, scenario)

    def get_type(self):
        return "dummy"

    def render(self, relative_start_time):
        return TextClip("dummy").set_duration(5)


class DummyFrameEffect(AbstractFrameEffect):

    def __init__(self, type, time):
        super().__init__(type, time)

    def render_on_frame(self, clip):
        return TextClip("dummy").set_duration(5)


class DummyBlockEffect(AbstractBlockEffect):

    def render_on_block(self, clip):
        return Compilation(TextClip("dummy").set_duration(5), TextClip("dummy").set_duration(5), "dummy")


class DummyBlock(AbstractBlock):

    def get_type(self):
        return "dummy"


class DummyCompiler(AbstractCompiler):

    def compile(self, compilation):
        return compilation.target


class DummyCompilerReturningNone(AbstractCompiler):

    def compile(self, compilation):
        return None
