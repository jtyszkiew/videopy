import json

from typing_extensions import Annotated

import typer
from rich.table import Table
from rich.console import Console
from rich import print
from rich.markdown import Markdown

from moviepy.editor import TextClip

from videopy.hooks import Hooks
from videopy.main import run_scenario
from videopy.module_validators import validate_frame
from videopy.utils.file import get_file_extension
from videopy.utils.loader import Loader
from videopy.utils.logger import Logger, LoggerProvider

app = typer.Typer()
console = Console()


def log(self, message):
    print(message)


Logger.provider = type('RichLoggerProvider', (LoggerProvider,), {'print': log})()


@app.command()
def run(scenario_name: Annotated[str, typer.Argument(
    help="Scenario name to use, if you want to use your own need to provide with --scenario-file option.")] = None,
        scenario_file: Annotated[
            str, typer.Option(help="If you don't want to use auto discovered scenarios use this option")] = None,
        scenario_data: Annotated[str, typer.Option(help="Data to pass to scenario")] = None,
        scenario_content: Annotated[str, typer.Option(help="You can use this option insted of yaml file")] = None):
    run_scenario(scenario_name, scenario_file, scenario_content, "info",
                 json.loads(scenario_data) if scenario_data else None)


@app.command()
def scenario(scenario_name: Annotated[str, typer.Argument(
    help="Scenario name to use, if you want to use your own need to provide with --scenario-file option.")]):
    hooks = Hooks()
    scenarios, file_loaders = {}, {}

    Loader.load_plugins("plugins", hooks)
    hooks.run_hook("videopy.modules.scenarios.register", scenarios)
    hooks.run_hook("videopy.modules.file_loaders.register", file_loaders)

    for key, value in scenarios.items():
        if key == scenario_name:
            if file_loaders[get_file_extension(value['file_path'])]:
                scenario_yml = file_loaders[get_file_extension(value['file_path'])](value['file_path'])
            else:
                raise ValueError(f"File loader for extension [{get_file_extension(value['file_path'])}] not found")

            console = Console()
            console.print(Markdown(f"# Description"))
            console.print(Markdown(f"{scenario_yml['description']}"))
            console.print(Markdown(f"# Configuration"))

            form = scenario_yml.get('form', None)
            fields = form.get('fields', None) if form else None

            if form is not None and fields is not None:
                table = Table(
                    "Configuration",
                    "Description",
                    "Type",
                    "Required",
                    "Default Value",
                    show_lines=True,
                    title=f"{scenario_name}",
                    title_style="bold cyan"
                )

                for key, value in scenario_yml['form']['fields'].items():
                    default_value = str(value.get('default', 'None'))
                    table.add_row(
                        key,
                        value['description'],
                        value['type'], "Yes" if value['required'] else "No",
                        default_value
                    )

                console.print(table)


@app.command()
def scenarios():
    hooks = Hooks()
    scenarios, file_loaders = {}, {}

    Loader.load_plugins("plugins", hooks)
    hooks.run_hook("videopy.modules.scenarios.register", scenarios)
    hooks.run_hook("videopy.modules.file_loaders.register", file_loaders)

    table = Table("Name", "Description", show_lines=True)

    for key, value in scenarios.items():
        if file_loaders[get_file_extension(value['file_path'])]:
            scenario_yml = file_loaders[get_file_extension(value['file_path'])](value['file_path'])
        else:
            raise ValueError(f"File loader for extension [{get_file_extension(value)}] not found")

        table.add_row(key, scenario_yml['description'] if 'description' in scenario_yml else "No description")

    console.print(table)


@app.command()
def frames():
    hooks = Hooks()
    frames = {}

    Loader.load_plugins("plugins", hooks)
    hooks.run_hook("videopy.modules.frames.register", frames)

    table = Table("Name", "Description", show_lines=True)

    for key, value in frames.items():
        table.add_row(key, value['description'])

    console.print(table)


@app.command()
def frame(frame_name: Annotated[str, typer.Argument(help="Frame to show info about.")]):
    __display_configuration_table("frames", frame_name)


@app.command()
def blocks():
    hooks = Hooks()
    blocks = {}

    Loader.load_plugins("plugins", hooks)
    hooks.run_hook("videopy.modules.blocks.register", blocks)

    table = Table("Name", "Description", show_lines=True)

    for key, value in blocks.items():
        table.add_row(key, value['description'])

    console.print(table)


@app.command()
def block(block_name: Annotated[str, typer.Argument(help="Effect to show info about.")]):
    __display_configuration_table("blocks", block_name)


@app.command()
def effects():
    hooks = Hooks()
    effects = {}

    Loader.load_plugins("plugins", hooks)
    hooks.run_hook("videopy.modules.effects.register", effects)

    table = Table("Name", "Description", "Renders On", show_lines=True)

    for key, value in effects.items():
        table.add_row(key, value['description'], ', '.join(value['renders_on']))

    console.print(table)


@app.command()
def effect(effect_name: Annotated[str, typer.Argument(help="Effect to show info about.")]):
    __display_configuration_table("effects", effect_name)


@app.command()
def helpers(helper_name: Annotated[str, typer.Argument(help="Helper to show info about.")]):
    if helper_name == "fonts":
        print(TextClip("fonts").list('font'))

    if helper_name == "examples":
        print("Starting to generate examples")
        hooks = Hooks()
        Loader.load_plugins("plugins", hooks)
        md_file = ""

        blocks, effects, frames, file_loaders, compilers, fields = {}, {}, {}, {}, {}, {}

        hooks.run_hook("videopy.modules.frames.register", frames)
        hooks.run_hook("videopy.modules.blocks.register", blocks)
        hooks.run_hook("videopy.modules.effects.register", effects)
        hooks.run_hook("videopy.modules.file_loaders.register", file_loaders)
        hooks.run_hook("videopy.modules.compilers.register", compilers)
        hooks.run_hook("videopy.modules.forms.fields.register", fields)

        md_file += "# Frames \n"
        for key, frame in frames.items():
            md_file = __print_example_container(md_file, key, frame)

        md_file += "# Frame Effects \n"
        for key, effect in effects.items():
            if 'frame' in effect['renders_on']:
                md_file = __print_example_container(md_file, key, effect)

        md_file += "# Blocks \n"
        for key, block in blocks.items():
            md_file = __print_example_container(md_file, key, block)

        md_file += "# Blocks Effects \n"
        for key, effect in effects.items():
            if 'block' in effect['renders_on']:
                md_file = __print_example_container(md_file, key, effect)

        with open("example.md", "w") as f:
            f.write(md_file)


def __display_configuration_table(module: str, concrete_module_name: str):
    Logger.enabled = False
    hooks = Hooks()
    modules = {}

    Loader.load_plugins("plugins", hooks)
    hooks.run_hook(f"videopy.modules.{module}.register", modules)

    table = Table(
        "Configuration",
        "Description",
        "Type",
        "Required",
        "Default Value",
        show_lines=True,
        title=f"{concrete_module_name}: {modules[concrete_module_name]['description']}",
        title_style="bold cyan"
    )

    for key, value in modules[concrete_module_name]['configuration'].items():
        default_value = str(value.get('default', 'None'))
        table.add_row(
            key,
            value['description'],
            value['type'], "Yes" if value['required'] else "No",
            default_value
        )

    console.print(table)

def __print_example_container(md_file, key, module):
    if module.get('examples', None):
        md_file = __print_example_header(md_file, key, module)

        for index, example in enumerate(module['examples']):
            module['examples'][index]['scenario']['output_path'] = f"example/generated/{key}_example_{index}"
            run_scenario(scenario_content=module['examples'][index]['scenario'], format="gif")

            md_file = __print_example(md_file, key, module, example, index, example.get('tips', []))

    return md_file

def __print_example_header(md_file, key, frame):
    md_file += f"## {key}\n"
    md_file += f"{frame['description']}\n"

    return md_file


def __print_example(md_file, key, frame, example, index, tips=None):
    if tips is None:
        tips = []

    md_file += f"### {example['name']}\n"
    md_file += f"![{key} - {frame['description']} - Example {index}](example/generated/{key}_example_{index}.gif)\n"
    md_file += f">{example['description']}\n\n"
    for tip in tips:
        md_file += f"> {tip}\n\n"
    md_file += "\n"
    md_file += f"<details><summary>Example code</summary>\n\n```yaml\n{json.dumps(example['scenario'], indent=2)}\n```\n\n</details>\n\n"

    return md_file


if __name__ == "__main__":
    app()
