from videopy.hooks import Hooks
from videopy.utils.file import get_file_extension, get_file_name_without_extension
from videopy.utils.loader import Loader
from videopy.utils.logger import Logger
from videopy.scenario import ScenarioFactory


def run_scenario(scenario_name: str = None, scenario_file: str = None, log_level: str = "info"):
    Logger.set_level(log_level)

    if scenario_file is None and scenario_name is None:
        raise ValueError("You need to provide either --scenario-file or --scenario-name")

    hooks = Hooks()
    scenarios, blocks, effects, frames, file_loaders, compilers = {}, {}, {}, {}, {}, {}

    Loader.load_plugins("plugins", hooks)

    if scenario_file is None:
        Logger.debug(f"Scenario file not provided, trying to auto discover scenario by name: <<{scenario_name}>>")

        hooks.run_hook("videopy.modules.scenarios.register", scenarios)

        for key, value in scenarios.items():
            if key == scenario_name:
                scenario_file = value
                break

    hooks.run_hook("videopy.modules.frames.register", frames)
    hooks.run_hook("videopy.modules.blocks.register", blocks)
    hooks.run_hook("videopy.modules.effects.register", effects)
    hooks.run_hook("videopy.modules.file_loaders.register", file_loaders)
    hooks.run_hook("videopy.modules.compilers.register", compilers)

    modules = {
        "blocks": blocks,
        "effects": effects,
        "frames": frames
    }

    if file_loaders[get_file_extension(scenario_file)]:
        scenario_yml = file_loaders[get_file_extension(scenario_file)](scenario_file)
    else:
        raise ValueError(f"File loader for extension [{get_file_extension(scenario_file)}] not found")

    scenario_name = get_file_name_without_extension(scenario_file)

    if "script" in scenario_yml:
        Loader.load_script(scenario_yml["script"])(scenario_yml).do_run(hooks)

    scenario = ScenarioFactory.from_yml(modules, scenario_yml, scenario_name, hooks, compilers)

    for frame_yml in scenario_yml['frames']:
        frame = __create_frame(modules, frame_yml, scenario)

        # Set up effects
        for effect_yml in frame_yml.get('effects', []):
            frame.add_effect(__create_effect(modules, effect_yml))

        # Set up blocks
        for block_yml in frame_yml.get('blocks', []):
            block = __create_block(modules, block_yml, frame)

            frame.add_block(block)

            hooks.run_hook("videopy.scenario.frame.block.effects.before_load", block_yml['effects'])
            for effect_yml in block_yml.get('effects', []):
                block.add_effect(__create_effect(modules, effect_yml))

        scenario.add_frame(frame)
    scenario.render()


def __create_effect(modules, effect_yml):
    effect_type = effect_yml['type']
    effect_yml['configuration'] = effect_yml['configuration'] if 'configuration' in effect_yml else {}
    modules['effects'][effect_type]['configuration'] = modules['effects'][effect_type][
        'configuration'] if 'configuration' in modules['effects'][effect_type] else {}

    Loader.load_defaults(effect_yml['configuration'], modules['effects'][effect_type]['configuration'])

    effect_factory = Loader.get_effect_factory(effect_type)

    return effect_factory().from_yml(effect_yml)


def __create_block(modules, block_yml, frame):
    block_type = block_yml['type']
    block_yml['configuration'] = block_yml['configuration'] if 'configuration' in block_yml else {}

    Loader.load_defaults(block_yml['configuration'], modules['blocks'][block_type]['configuration'])

    block_factory = Loader.get_block_factory(block_type)

    return block_factory().from_yml(block_yml, modules['blocks'][block_type], frame)


def __create_frame(modules, frame_yml, scenario):
    frame_type = frame_yml['type']
    factory = Loader.get_frame_factory(frame_type)

    return factory().from_yml(frame_yml, scenario)
