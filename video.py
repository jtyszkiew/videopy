import json
import os

import yaml
from typing_extensions import Annotated

import typer
from rich.table import Table
from rich.console import Console
from rich import print

from moviepy.editor import TextClip

from videopy.hooks import Hooks
from videopy.main import run_scenario
from videopy.utils.file import get_file_extension
from videopy.utils.loader import Loader
from videopy.utils.logger import Logger, LoggerProvider

app = typer.Typer()
console = Console()

__EXAMPLES_OUTPUT_DIR = "outputs/examples"


def log(self, message):
    print(message)


Logger.provider = type('RichLoggerProvider', (LoggerProvider,), {'print': log})()

__H_SCENARIO_NAME = "Provide scenario name from registry (added through plugins)"
__H_SCENARIO_FILE = "Provide file path containing scenario in yaml format"
__H_SCENARIO_CONTENT = "Provide the scenario as json"
__H_SCENARIO_DATA = "Data to pass to scenario"
__H_FRAME_NAME = "Frame to show info about."
__H_BLOCK_NAME = "Block to show info about."
__H_EFFECT_NAME = "Effect to show info about."

current_dir = os.path.dirname(__file__)
absolute_path = os.path.abspath(current_dir)

@app.command()
def run(input_name: Annotated[str, typer.Option(help=__H_SCENARIO_NAME)] = None,
        input_file: Annotated[str, typer.Option(help=__H_SCENARIO_FILE)] = None,
        input_content: Annotated[str, typer.Option(help=__H_SCENARIO_CONTENT)] = None,
        data: Annotated[str, typer.Option(help=__H_SCENARIO_DATA)] = None,
        ctx: typer.Context = typer.Context
        ):
    if input_name is None and input_file is None and data is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()

    run_scenario(
        input_name=input_name,
        input_file=input_file,
        input_content=input_content,
        scenario_data=json.loads(data) if data else None,
        log_level="info",
    )


@app.command()
def scenarios(scenario_name: Annotated[str, typer.Argument(help=__H_SCENARIO_NAME)] = None):
    hooks = Hooks()
    scenarios, file_loaders = {}, {}

    Loader.load_plugins(f"{absolute_path}/plugins", hooks)
    hooks.run_hook("videopy.modules.scenarios.register", scenarios)
    hooks.run_hook("videopy.modules.file_loaders.register", file_loaders)

    console = Console()

    if scenario_name is None:
        table = Table("Name", "Description", show_lines=True)

        for key, value in scenarios.items():
            if file_loaders[get_file_extension(value['file_path'])]:
                scenario_yml = file_loaders[get_file_extension(value['file_path'])](f"{absolute_path}/{value['file_path']}")
            else:
                raise ValueError(f"File loader for extension [{get_file_extension(value)}] not found")

            table.add_row(key, scenario_yml['description'] if 'description' in scenario_yml else "No description")

        console.print(table)
    else:
        raise NotImplementedError("Not implemented yet")


@app.command()
def frames(frame_name: Annotated[str, typer.Argument(help=__H_FRAME_NAME)] = None):
    hooks = Hooks()
    frames = {}

    if frame_name is None:
        Loader.load_plugins(f"{absolute_path}/plugins", hooks)
        hooks.run_hook("videopy.modules.frames.register", frames)

        table = Table("Name", "Description", show_lines=True)

        for key, value in frames.items():
            table.add_row(key, value.get_description())

        console.print(table)
    else:
        __display_configuration_table("frames", frame_name)


@app.command()
def blocks(block_name: Annotated[str, typer.Argument(help=__H_BLOCK_NAME)] = None):
    hooks = Hooks()
    blocks = {}

    if block_name is None:
        Loader.load_plugins(f"{absolute_path}/plugins", hooks)
        hooks.run_hook("videopy.modules.blocks.register", blocks)

        table = Table("Name", "Description", show_lines=True)

        for key, value in blocks.items():
            table.add_row(key, value.get_description())

        console.print(table)
    else:
        __display_configuration_table("blocks", block_name)


@app.command()
def effects(effect_name: Annotated[str, typer.Argument(help=__H_EFFECT_NAME)] = None):
    hooks = Hooks()
    effects = {}

    if effect_name is None:
        Loader.load_plugins(f"{absolute_path}/plugins", hooks)
        hooks.run_hook("videopy.modules.effects.register", effects)

        table = Table("Name", "Description", "Renders On", show_lines=True)

        for key, value in effects.items():
            table.add_row(key, value.get_description(), ', '.join(value.get_renders_on()))

        console.print(table)
    else:
        __display_configuration_table("effects", effect_name)


@app.command()
def helpers(helper_name: Annotated[str, typer.Argument(help="Helper to show info about.")]):
    if helper_name == "fonts":
        print(TextClip("fonts").list('font'))

    if helper_name == "examples":
        print("Starting to generate examples")

        if not os.path.exists(__EXAMPLES_OUTPUT_DIR):
            os.makedirs(__EXAMPLES_OUTPUT_DIR)

        hooks = Hooks()
        Loader.load_plugins(f"{absolute_path}/plugins", hooks)
        md_file = ""

        blocks, effects, frames, file_loaders, compilers, fields = {}, {}, {}, {}, {}, {}

        hooks.run_hook("videopy.modules.frames.register", frames)
        hooks.run_hook("videopy.modules.blocks.register", blocks)
        hooks.run_hook("videopy.modules.effects.register", effects)
        hooks.run_hook("videopy.modules.file_loaders.register", file_loaders)
        hooks.run_hook("videopy.modules.compilers.register", compilers)
        hooks.run_hook("videopy.modules.forms.fields.register", fields)

        md_file += "# Table of contents\n"
        md_file += "- [Frames](#frames)\n"
        for key, frame in frames.items():
            replaced_key = key.replace(".", "")
            md_file += f"  - [{key}](#{replaced_key})\n"

        md_file += "- [Frame Effects](#frame-effects)\n"
        for key, effect in effects.items():
            if 'frame' in effect.get_renders_on():
                replaced_key = key.replace(".", "")
                md_file += f"  - [{key}](#{replaced_key})\n"

        md_file += "- [Blocks](#blocks)\n"
        for key, block in blocks.items():
            replaced_key = key.replace(".", "")
            md_file += f"  - [{key}](#{replaced_key})\n"

        md_file += "- [Block Effects](#block-effects)\n"
        for key, effect in effects.items():
            if 'block' in effect.get_renders_on():
                replaced_key = key.replace(".", "")
                md_file += f"  - [{key}](#{replaced_key})\n"

        md_file += "# Frames \n"
        for key, frame in frames.items():
            md_file = __print_example_container(md_file, key, frame)

        md_file += "# Frame Effects \n"
        for key, effect in effects.items():
            if 'frame' in effect.get_renders_on():
                md_file = __print_example_container(md_file, key, effect)

        md_file += "# Blocks \n"
        for key, block in blocks.items():
            md_file = __print_example_container(md_file, key, block)

        md_file += "# Blocks Effects \n"
        for key, effect in effects.items():
            if 'block' in effect.get_renders_on():
                md_file = __print_example_container(md_file, key, effect)

        with open("example.md", "w") as f:
            f.write(md_file)


def __display_configuration_table(module: str, concrete_module_name: str):
    Logger.enabled = False
    hooks = Hooks()
    modules = {}

    Loader.load_plugins(f"{absolute_path}/plugins", hooks)
    hooks.run_hook(f"videopy.modules.{module}.register", modules)

    if modules[concrete_module_name].get_configuration():
        table = Table(
            "Configuration",
            "Description",
            "Type",
            "Required",
            "Default Value",
            show_lines=True,
            title=f"{concrete_module_name}: {modules[concrete_module_name].get_description()}",
            title_style="bold cyan"
        )

        for key, value in modules[concrete_module_name].get_configuration().items():
            default_value = str(value.get('default', 'None'))
            table.add_row(
                key,
                value['description'],
                value['type'],
                "Yes" if value['required'] else "No",
                default_value
            )

        console.print(table)
    else:
        console.print(f"No configuration found for {concrete_module_name}")


def __print_example_container(md_file, key, module):
    md_file = __print_example_header(md_file, key, module)
    examples = module.get_examples()
    configuration = module.get_configuration()

    if examples:
        for index, example in enumerate(examples):
            examples[index]['scenario']['output_path'] = f"{__EXAMPLES_OUTPUT_DIR}/{key}_example_{index}.gif"
            run_scenario(input_content=examples[index]['scenario'])

            md_file = __print_example(md_file, key, module, example, index, example.get('tips', []))

    if configuration:
        table = "| Configuration | Description | Type | Required | Default Value |\n| --- | --- | --- | --- | --- |\n"

        for key, value in configuration.items():
            default_value = str(value.get('default', 'None'))
            table += f"| {key} | {value['description']} | {value['type']} | {'Yes' if value['required'] else 'No'} | {default_value} |\n"

        md_file += f"<details><summary>Configuration</summary>\n\n{table}\n\n</details>\n\n"

    md_file += "\n---\n"

    return md_file


def __print_example_header(md_file, key, frame):
    description = frame.get_description()

    md_file += f"## {key}\n"
    md_file += f"{description}\n"

    return md_file


def __print_example(md_file, key, frame, example, index, tips=None):
    if tips is None:
        tips = []

    description = frame.get_description()

    md_file += f"### Example: {example['name']}\n"
    md_file += f"![{key} - {description} - Example {index}]({__EXAMPLES_OUTPUT_DIR}/{key}_example_{index}.gif)\n"
    md_file += f">{example['description']}\n\n"
    for tip in tips:
        md_file += f"> {tip}\n\n"
    md_file += "\n"
    md_file += f"<details><summary>Example code</summary>\n\n```yaml\n{yaml.dump(example['scenario'], sort_keys=False)}\n```\n\n</details>\n\n"

    return md_file


if __name__ == "__main__":
    app()
