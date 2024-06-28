from videopy.compilation import AbstractCompiler

types = ['str', 'float', 'bool', 'int', 'select', 'color', 'file', 'image', 'video', 'audio', 'datetime', 'date',
         'time', 'tuple']


class Registry:

    def __init__(self):
        self.scenarios = {}
        self.frames = {}
        self.blocks = {}
        self.effects = {}
        self.file_loaders = {}
        self.compilers = {}

    def add_scenario(self, scenario_type, module):
        Validator.validate_scenario(module)

        self.scenarios[scenario_type] = module

    def add_frame(self, frame_type, module):
        Validator.validate_frame(module)

        self.frames[frame_type] = module

    def add_block(self, block_type, module):
        Validator.validate_block(module)

        self.blocks[block_type] = module

    def add_effect(self, effect_type, module):
        Validator.validate_effect(module)

        self.effects[effect_type] = module

    def add_file_loader(self, file_loader_type, module):
        Validator.validate_file_loader(file_loader_type, module)

        self.file_loaders[file_loader_type] = module

    def add_compiler(self, compiler_type, module):
        Validator.validate_compiler(module)

        self.compilers[compiler_type] = module


class Validator:

    @staticmethod
    def validate_configuration(configuration):
        for key, value in configuration.items():
            if 'description' not in value or value['description'] is None or value['description'] == "":
                raise ValueError(f"Description is required in module configuration")

            if 'type' not in value or value['type'] is None:
                raise ValueError(f"Type is required in module configuration")

            if value['type'] not in types:
                raise ValueError(f"Type is not valid in module configuration")

            if 'required' not in value or value['required'] is None:
                raise ValueError(f"Required is required in module configuration")

            if value['required'] not in [True, False]:
                raise ValueError(f"Required is not valid in module configuration")

            if value['required'] is False and 'default' not in value:
                raise ValueError(f"Default is required in module configuration")

    @staticmethod
    def validate_scenario(scenario):
        pass

    @staticmethod
    def validate_frame(frame):
        if 'description' not in frame:
            raise ValueError("Frame description is required")
        if 'configuration' in frame:
            Validator.validate_configuration(frame['configuration'])

    @staticmethod
    def validate_block(block):
        if 'description' not in block:
            raise ValueError("Block description is required")
        if 'configuration' in block:
            Validator.validate_configuration(block['configuration'])

    @staticmethod
    def validate_effect(effect):
        if 'description' not in effect:
            raise ValueError("Effect description is required")
        if 'configuration' in effect:
            Validator.validate_configuration(effect['configuration'])

    @staticmethod
    def validate_file_loader(key, value):
        if not callable(value):
            raise ValueError(f"File loader {key} is not callable")

    @staticmethod
    def validate_compiler(compiler):
        if not issubclass(type(compiler), AbstractCompiler):
            raise ValueError(f"Compiler {compiler} is not a subclass of AbstractCompiler")
