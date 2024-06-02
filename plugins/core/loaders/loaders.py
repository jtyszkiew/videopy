import yaml


def yaml_file_loader(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)
