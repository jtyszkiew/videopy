from videopy.compilation import AbstractCompiler

types = ['str', 'float', 'bool', 'int', 'select', 'color', 'file', 'image', 'video', 'audio', 'datetime', 'date',
         'time']


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


def validate_scenario(scenario):
    pass


def validate_frame(frame):
    if 'description' not in frame:
        raise ValueError("Frame description is required")
    if 'configuration' in frame:
        validate_configuration(frame['configuration'])


def validate_block(block):
    if 'description' not in block:
        raise ValueError("Block description is required")
    if 'configuration' in block:
        validate_configuration(block['configuration'])


def validate_effect(effect):
    if 'description' not in effect:
        raise ValueError("Effect description is required")
    if 'configuration' in effect:
        validate_configuration(effect['configuration'])


def validate_file_loader(file_loader):
    for key, value in file_loader.items():
        if not callable(value):
            raise ValueError(f"File loader {key} is not callable")


def validate_compiler(compiler):
    if not issubclass(type(compiler), AbstractCompiler):
        raise ValueError(f"Compiler {compiler} is not a subclass of AbstractCompiler")
