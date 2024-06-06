import importlib
import os
import sys

from videopy.block import AbstractBlockFactory
from videopy.effect import AbstractEffectFactory
from videopy.form import AbstractFieldFactory
from videopy.frame import AbstractFrameFactory
from videopy.script import AbstractScript
from videopy.utils.logger import Logger

FRAME_FACTORY_CLASS_NAME = "FrameFactory"
BLOCK_FACTORY_CLASS_NAME = "BlockFactory"
EFFECT_FACTORY_CLASS_NAME = "EffectFactory"
FIELD_FACTORY_CLASS_NAME = "FieldFactory"


class Loader:

    @staticmethod
    def get_frame_factory(package):
        package = importlib.import_module(package)
        factory = getattr(package, FRAME_FACTORY_CLASS_NAME)

        if not issubclass(factory, AbstractFrameFactory):
            raise ValueError(f"Factory {factory} is not an instance of FrameFactory")

        Logger.trace(f"Registered frame factory: <<{factory}>>")

        return factory

    @staticmethod
    def get_block_factory(package):
        package = importlib.import_module(package)
        factory = getattr(package, BLOCK_FACTORY_CLASS_NAME)

        if not issubclass(factory, AbstractBlockFactory):
            raise ValueError(f"Factory {factory} is not an instance of BlockFactory")

        Logger.trace(f"Registered block factory: <<{factory}>>")

        return factory

    @staticmethod
    def get_effect_factory(package):
        package = importlib.import_module(package)
        factory = getattr(package, EFFECT_FACTORY_CLASS_NAME)

        if not issubclass(factory, AbstractEffectFactory):
            raise ValueError(f"Factory {factory} is not an instance of EffectFactory")

        Logger.trace(f"Registered effect factory: <<{factory}>>")

        return factory

    def get_field_factory(package):
        package = importlib.import_module(package)
        factory = getattr(package, FIELD_FACTORY_CLASS_NAME)

        if not issubclass(factory, AbstractFieldFactory):
            raise ValueError(f"Factory {factory} is not an instance of FieldFactory")

        Logger.trace(f"Registered field factory: <<{factory}>>")

        return factory

    @staticmethod
    def load_plugins(plugin_dir, hooks):
        for plugin_name in os.listdir(plugin_dir):
            plugin_path = os.path.join(plugin_dir, plugin_name, 'plugin.py')
            if os.path.isfile(plugin_path):
                spec = importlib.util.spec_from_file_location(f"{plugin_name}_plugin", plugin_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[f"{plugin_name}_plugin"] = module
                spec.loader.exec_module(module)
                if hasattr(module, 'register'):
                    module.register(hooks)

                    Logger.debug(f"Registered plugin: <<{plugin_name}>>")
                else:
                    Logger.debug(f"No register function found in plugin: <<{plugin_name}>>")

    @staticmethod
    def load_script(package):
        package = importlib.import_module(package)
        factory = getattr(package, "Script")

        if not issubclass(factory, AbstractScript):
            raise ValueError(f"Script {package} is not an instance of EffectFactory")

        Logger.trace(f"Registered script: <<{factory}>>")

        return factory

    @staticmethod
    def load_defaults(scenario, module):
        for key, value in module.items():
            is_required = value.get('required', False)
            default = value.get('default', None)

            if is_required and key not in scenario:
                raise ValueError(f"Key {key} is required in configuration")

            if key not in scenario:
                scenario[key] = default
