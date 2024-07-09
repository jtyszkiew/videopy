from plugins.core.blocks.audio import AudioBlockModuleDefinition
from plugins.core.blocks.image import ImageBlockModuleDefinition
from plugins.core.blocks.text import TextBlockModuleDefinition
from plugins.core.compilers.compose import ComposeCompiler
from plugins.core.compilers.concacenate import ConcatenateCompiler
from plugins.core.compilers.ignore import IgnoreCompiler
from plugins.core.compilers.use_source import UseSourceCompiler
from plugins.core.compilers.use_target import UseTargetCompiler
from plugins.core.effects.blocks.audio.play import AudioPlayEffectModuleDefinition
from plugins.core.effects.blocks.image.display import ImageDisplayEffectModuleDefinition
from plugins.core.effects.blocks.text.background import TextBackgroundEffectModuleDefinition
from plugins.core.effects.blocks.text.fadein import TextFadeInEffectModuleDefinition
from plugins.core.effects.blocks.text.fadeout import TextFadeOutEffectModuleDefinition
from plugins.core.effects.blocks.text.slidein import TextSlideInEffectModuleDefinition
from plugins.core.effects.blocks.text.slideout import TextSlideOutEffectModuleDefinition
from plugins.core.effects.blocks.text.typewrite import TextTypewriteEffectModuleDefinition
from plugins.core.effects.blocks.text.write import TextWriteEffectModuleDefinition
from plugins.core.effects.frames.audio import FrameAudioEffectModuleDefinition
from plugins.core.effects.frames.fadein import FrameFadeInEffectModuleDefinition
from plugins.core.effects.frames.fadeout import FrameFadeOutEffectModuleDefinition
from plugins.core.effects.frames.resize import FrameResizeEffectModuleDefinition
from plugins.core.frames.image import ImageFrameModuleDefinition
from plugins.core.frames.video import VideoFrameModuleDefinition
from plugins.core.loaders.yaml import yaml_file_loader
from plugins.core.params.loop import LoopParamHandler
from plugins.core.params.math import MathParamHandler
from plugins.core.params.when import WhenParamHandler
from plugins.core.templates.load_effects_template import load_effects_template
from videopy.template import HOOK_TEMPLATE_PARAM_PRE_HANDLER_REGISTER, HOOK_TEMPLATE_PARAM_POST_HANDLER_REGISTER

__PLUGIN_PREFIX = "plugins.core"
__PLUGIN_PREFIX_INDEX = __PLUGIN_PREFIX.replace(".", "")


def register_scenarios(scenarios):
    scenarios["images_dir_to_video"] = {
        "file_path": "plugins/core/scenarios/images_dir_to_video/images_dir_to_video.yml",
    }


def register_frames(frames):
    frames[f"{__PLUGIN_PREFIX}.frames.image"] = ImageFrameModuleDefinition()
    frames[f"{__PLUGIN_PREFIX}.frames.video"] = VideoFrameModuleDefinition()


def register_blocks(blocks):
    blocks[f"{__PLUGIN_PREFIX}.blocks.text"] = TextBlockModuleDefinition()
    blocks[f"{__PLUGIN_PREFIX}.blocks.image"] = ImageBlockModuleDefinition()
    blocks[f"{__PLUGIN_PREFIX}.blocks.audio"] = AudioBlockModuleDefinition()


def register_effects(effects):
    # BLOCK EFFECTS
    effects[f"{__PLUGIN_PREFIX}.effects.blocks.text.write"] = TextWriteEffectModuleDefinition()
    effects[f"{__PLUGIN_PREFIX}.effects.blocks.text.typewrite"] = TextTypewriteEffectModuleDefinition()
    effects[f"{__PLUGIN_PREFIX}.effects.blocks.text.background"] = TextBackgroundEffectModuleDefinition()
    effects[f"{__PLUGIN_PREFIX}.effects.blocks.text.fadein"] = TextFadeInEffectModuleDefinition()
    effects[f"{__PLUGIN_PREFIX}.effects.blocks.text.fadeout"] = TextFadeOutEffectModuleDefinition()
    effects[f"{__PLUGIN_PREFIX}.effects.blocks.text.slidein"] = TextSlideInEffectModuleDefinition()
    effects[f"{__PLUGIN_PREFIX}.effects.blocks.text.slideout"] = TextSlideOutEffectModuleDefinition()
    effects[f"{__PLUGIN_PREFIX}.effects.blocks.audio.play"] = AudioPlayEffectModuleDefinition()
    effects[f"{__PLUGIN_PREFIX}.effects.blocks.image.display"] = ImageDisplayEffectModuleDefinition()

    # FRAME EFFECTS
    effects[f"{__PLUGIN_PREFIX}.effects.frames.fadein"] = FrameFadeInEffectModuleDefinition()
    effects[f"{__PLUGIN_PREFIX}.effects.frames.fadeout"] = FrameFadeOutEffectModuleDefinition()
    effects[f"{__PLUGIN_PREFIX}.effects.frames.audio"] = FrameAudioEffectModuleDefinition()
    effects[f"{__PLUGIN_PREFIX}.effects.frames.resize"] = FrameResizeEffectModuleDefinition()


def register_file_loaders(file_loaders):
    file_loaders["yml"] = yaml_file_loader


def register_compilers(compilers):
    compilers["use_source"] = UseSourceCompiler()
    compilers["use_target"] = UseTargetCompiler()
    compilers["compose"] = ComposeCompiler()
    compilers["concatenate"] = ConcatenateCompiler()
    compilers["ignore"] = IgnoreCompiler()


def register_param_pre_handlers(param_pre_handlers):
    param_pre_handlers["loop"] = LoopParamHandler()
    param_pre_handlers["math"] = MathParamHandler()


def register_param_post_handlers(param_post_handlers):
    param_post_handlers["when"] = WhenParamHandler()


def register(hooks):
    hooks.register_hook("videopy.modules.scenarios.register", register_scenarios)
    hooks.register_hook("videopy.modules.frames.register", register_frames)
    hooks.register_hook("videopy.modules.blocks.register", register_blocks)
    hooks.register_hook("videopy.modules.effects.register", register_effects)
    hooks.register_hook("videopy.modules.file_loaders.register", register_file_loaders)
    hooks.register_hook("videopy.modules.compilers.register", register_compilers)
    hooks.register_hook(HOOK_TEMPLATE_PARAM_PRE_HANDLER_REGISTER, register_param_pre_handlers)
    hooks.register_hook(HOOK_TEMPLATE_PARAM_POST_HANDLER_REGISTER, register_param_post_handlers)

    hooks.register_hook("videopy.scenario.frame.block.effects.before_load", load_effects_template)
