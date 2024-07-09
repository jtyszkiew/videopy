from videopy.hooks import Hooks
from videopy.module import Registry, AbstractModuleDefinition
from videopy.scenario import ScenarioFactory
from videopy.utils.loader import Loader

HOOK_FRAME_EFFECT_BL = "videopy.scenario.frame.block.effects.before_load"


class Renderer:

    def __init__(self, scenario_yml, registry: Registry, hooks: Hooks):
        self.registry = registry
        self.scenario_yml = scenario_yml
        self.hooks = hooks

    def render(self):
        scenario = ScenarioFactory.from_yml(self.registry, self.scenario_yml, self.hooks)

        for frame_yml in self.scenario_yml['frames']:
            frame = self.__create_frame(frame_yml, scenario)

            # Set up effects
            for effect_yml in frame_yml.get('effects', []):
                frame.add_effect(self.__create_effect(effect_yml))

            # Set up blocks
            for block_yml in frame_yml.get('blocks', []):
                block = self.__create_block(block_yml, frame)

                frame.add_block(block)

                self.hooks.run_hook(HOOK_FRAME_EFFECT_BL, block_yml['effects'], self.registry.file_loaders)
                for effect_yml in block_yml.get('effects', []):
                    block.add_effect(self.__create_effect(effect_yml))

            scenario.add_frame(frame)
        scenario.render()

    def __create_frame(self, frame_yml, scenario):
        frame_type = frame_yml['type']
        factory = Loader.get_frame_factory(frame_type)

        return factory().from_yml(frame_yml, scenario)

    def __create_effect(self, effect_yml):
        effect_type = effect_yml['type']
        module = self.registry.effects[effect_type]
        module_configuration = self.__get_module_configuration(module)

        effect_yml['configuration'] = effect_yml['configuration'] if 'configuration' in effect_yml else {}

        Loader.load_defaults(effect_yml['configuration'], module_configuration)

        effect_factory = Loader.get_effect_factory(effect_type)

        return effect_factory().from_yml(effect_yml)

    def __create_block(self, block_yml, frame):
        block_type = block_yml['type']
        module = self.registry.blocks[block_type]
        module_configuration = self.__get_module_configuration(module)
        block_yml['configuration'] = block_yml['configuration'] if 'configuration' in block_yml else {}

        Loader.load_defaults(block_yml['configuration'], module_configuration)

        block_factory = Loader.get_block_factory(block_type)

        return block_factory().from_yml(block_yml, module, frame)

    def __get_module_configuration(self, module):
        if issubclass(type(module), AbstractModuleDefinition):
            return module.get_configuration()
        else:
            return module['configuration'] if 'configuration' in module else {}
