import yaml

from videopy.utils.logger import Logger


def before_load_effects(effects):
    index = 0
    while index < len(effects):
        effect = effects[index]
        if effect['type'] == "plugins.template":
            name = effect['configuration'].get('name', None)
            file_path = effect['configuration'].get('file_path', None)

            if name is None:
                raise ValueError("[B]: Template name is required")
            if file_path is not None:
                Logger.debug(f"Loading template from file <<{file_path}>>")
                with open(file_path, 'r') as f1:
                    template_yml = yaml.safe_load(f1)
                    if 'templates' in template_yml and 'effects' in template_yml['templates']:
                        if name in template_yml['templates']['effects']:
                            template_effects = template_yml['templates']['effects'][name]
                            if isinstance(template_effects, list):
                                effects.pop(index)  # Remove the plugins.template entry
                                for template_effect in reversed(template_effects):  # Insert in reverse order
                                    effects.insert(index, template_effect)
                                index += len(
                                    template_effects)  # Move the index forward by the number of inserted effects
                            else:
                                raise ValueError(f"Template \"{name}\" effects should be a list")
                        else:
                            raise ValueError(f"Template \"{name}\" not found in file \"{file_path}\"")
                    else:
                        raise ValueError(f"Invalid template structure in file \"{file_path}\"")
            else:
                raise ValueError("Template file_path is required")
        else:
            index += 1


def register(hooks):
    hooks.register_hook("videopy.scenario.frame.block.effects.before_load", before_load_effects)
