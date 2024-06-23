import json

from videopy.hooks import Hooks
from videopy.module import Registry
from videopy.renderer import Renderer
from videopy.template import Template
from videopy.utils.file import get_file_extension
from videopy.utils.loader import Loader
from videopy.utils.logger import Logger

HOOK_SCENARIOS_REGISTER = "videopy.modules.scenarios.register"
HOOK_FRAMES_REGISTER = "videopy.modules.frames.register"
HOOK_BLOCKS_REGISTER = "videopy.modules.blocks.register"
HOOK_EFFECTS_REGISTER = "videopy.modules.effects.register"
HOOK_FILE_LOADERS_REGISTER = "videopy.modules.file_loaders.register"
HOOK_COMPILERS_REGISTER = "videopy.modules.compilers.register"


def run_scenario(
        input_name: str = None,
        input_file: str = None,
        input_content: dict = None,
        scenario_data=None,
        log_level: str = "info",
):
    Logger.set_level(log_level)

    if input_file is None and input_name is None and input_content is None:
        raise ValueError("You need to provide one of: input_file, input_name, input_content")

    hooks = Hooks()
    registry = Registry()
    scenario_yml = None

    Loader.load_plugins("plugins", hooks)

    frames = {}
    hooks.run_hook(HOOK_FRAMES_REGISTER, frames)
    for key, frame in frames.items():
        registry.add_frame(key, frame)

    blocks = {}
    hooks.run_hook(HOOK_BLOCKS_REGISTER, blocks)
    for key, block in blocks.items():
        registry.add_block(key, block)

    effects = {}
    hooks.run_hook(HOOK_EFFECTS_REGISTER, effects)
    for key, effect in effects.items():
        registry.add_effect(key, effect)

    file_loaders = {}
    hooks.run_hook(HOOK_FILE_LOADERS_REGISTER, file_loaders)
    for key, file_loader in file_loaders.items():
        registry.add_file_loader(key, file_loader)

    compilers = {}
    hooks.run_hook(HOOK_COMPILERS_REGISTER, compilers)
    for key, compiler in compilers.items():
        registry.add_compiler(key, compiler)

    scenarios = {}
    hooks.run_hook(HOOK_SCENARIOS_REGISTER, scenarios)
    for key, scenario in scenarios.items():
        registry.add_scenario(key, scenario)

    if input_name is not None:
        Logger.debug(f"Loading scenario by name: <<{input_name}>>")

        for key, value in registry.scenarios.items():
            if key == input_name:
                input_file = value['file_path']
                break

    if input_file is not None:
        Logger.debug(f"Loading scenario from file: <<{input_file}>>")
        if registry.file_loaders[get_file_extension(input_file)]:
            Logger.debug(f"File loader for extension <<{get_file_extension(input_file)}>> found")

            scenario_yml = registry.file_loaders[get_file_extension(input_file)](input_file)
        else:
            raise ValueError(f"File loader for extension [{get_file_extension(input_file)}] not found")
    elif input_content is not None:
        Logger.debug(f"Loading scenario from content")
        scenario_yml = input_content

    if scenario_yml is None:
        raise ValueError("Scenario not found")

    hooks.run_hook("videopy.scenario.before_render", registry, scenario_yml, scenario_data)

    if "script" in scenario_yml:
        script = Loader.load_script(scenario_yml["script"])(scenario_yml)

        Logger.info(f"Used the following data to run the scenario:")
        Logger.raw(json.dumps(json.dumps(scenario_data)))
        Logger.info("Use the data above with <<--scenario-data>> option to run the scenario with the same data again")

        script.do_run(hooks, scenario_data)

    Template(scenario_yml, hooks).process()
    Renderer(scenario_yml, registry, hooks).render()
