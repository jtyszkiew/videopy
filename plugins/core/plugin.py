from plugins.core.compilers.compose import ComposeCompiler
from plugins.core.compilers.concacenate import ConcatenateCompiler
from plugins.core.compilers.ignore import IgnoreCompiler
from plugins.core.compilers.use_source import UseSourceCompiler
from plugins.core.compilers.use_target import UseTargetCompiler
from plugins.core.loaders.loaders import yaml_file_loader
from plugins.core.templates.load_effects_template import load_effects_template


def register_scenarios(scenarios):
    scenarios["images_dir_to_video"] = "plugins/core/scenarios/images_dir_to_video.yml"


def register_frames(frames):
    frames["plugins.core.frames.image"] = {
        "description": "This frame will display an image.",
        "configuration": {
            "file_path": {
                "description": "The path to the image.",
                "type": "string",
                "required": True
            }
        }
    }
    frames["plugins.core.frames.video"] = {
        "description": "This frame will display an video.",
        "configuration": {
            "file_path": {
                "description": "The path to the video.",
                "type": "string",
                "required": True
            },
            "mute": {
                "description": "Mute the source video (for example if you want to compose the sound differently).",
                "type": "bool",
                "default": False,
                "required": False
            },
            "subclip_start": {
                "description": "Setting the subclip will start the video from the given time.",
                "type": "float",
                "default": 0,
                "required": False,
            },
            "cut_to_frame_duration": {
                "description": "If video is longer than frame duration, cut it to frame duration.",
                "type": "bool",
                "default": True,
                "required": False
            }
        }
    }


def register_blocks(blocks):
    blocks["plugins.core.blocks.text"] = {
        "description": "This block will display text.",
        "configuration": {
            "content": {
                "description": "The text content.",
                "type": "string",
                "required": True
            },
            "font": {
                "description": "The font of the text.",
                "type": "string",
                "default": "Arial",
                "required": False
            },
            "size": {
                "description": "The size of the text.",
                "type": "int",
                "default": 50,
                "required": False
            },
            "color": {
                "description": "The color of the text.",
                "type": "string",
                "default": "black",
                "required": False
            },
            "margin": {
                "description": "The margin of the text.",
                "type": "float",
                "default": 0,
                "required": False
            },
            "padding": {
                "description": "The padding of the text.",
                "type": "float",
                "default": 10,
                "required": False
            }
        }
    }
    blocks["plugins.core.blocks.audio"] = {
        "description": "This is base block to manage audio on frame",
        "configuration": {
            "file_path": {
                "description": "The path to the audio file.",
                "type": "string",
                "required": True
            }
        }
    }


def register_effects(effects):
    # BLOCKS / TEXT / WRITE
    effects["plugins.core.effects.blocks.text.write"] = {
        "description": "Write text on a block. This is a base effect if you want to display text.",
        "renders_on": {
            "block": ["text"]
        },
    }

    # BLOCKS / TEXT / TYPEWRITE
    effects["plugins.core.effects.blocks.text.typewrite"] = {
        "description": "This effect will type the text one the block.",
        "renders_on": {
            "block": ["text"]
        },
        "configuration": {
            "duration_per_char": {
                "description": "The duration each character takes to appear. If not set it will be calculated "
                               "based on the duration of the effect. (duration / len(text))",
                "type": "float",
                "default": 0,
                "required": False
            }
        }
    }

    # BLOCKS / TEXT / BACKGROUND
    effects["plugins.core.effects.blocks.text.background"] = {
        "description": "Adds background to the frame.",
        "renders_on": {
            "block": ["text"]
        },
        "configuration": {
            "color": {
                "description": "The color of the background.",
                "type": "string",
                "default": "black",
                "required": False
            },
            "padding": {
                "description": "The padding of the background.",
                "type": "float",
                "default": 10,
                "required": False
            },
            "opacity": {
                "description": "The opacity of the background.",
                "type": "float",
                "default": 1,
                "required": False
            },
            "border_radius": {
                "description": "The border radius of the background.",
                "type": "float",
                "default": 10,
                "required": False
            }
        }
    }

    # BLOCKS / TEXT / FADEIN
    effects["plugins.core.effects.blocks.text.fadein"] = {
        "description": "Fade in the text block.",
        "renders_on": {
            "block": ["text"]
        },
        "configuration": {
            "duration": {
                "description": "The duration of the fade in. It's the time from the left side of block timeline.",
                "type": "float",
                "default": 1,
                "required": False
            }
        }
    }

    # BLOCKS / TEXT / FADEOUT
    effects["plugins.core.effects.blocks.text.fadeout"] = {
        "description": "Fade out the text block.",
        "renders_on": {
            "block": ["text"]
        },
        "configuration": {
            "duration": {
                "description": "The duration of the fade in. It's the time from the right side of block timeline.",
                "type": "float",
                "default": 1,
                "required": False
            }
        }
    }

    # BLOCKS / AUDIO / PLAY
    effects["plugins.core.effects.blocks.audio.play"] = {
        "description": "Play audio on block.",
        "renders_on": {
            "block": ["audio"]
        },
        "configuration": {
            "subclip_start": {
                "description": "Setting the subclip will start the audio from the given time.",
                "type": "float",
                "required": False,
            },
            "cut_to_block_duration": {
                "description": "If audio is longer than block duration, cut it to block duration.",
                "type": "bool",
                "default": True,
                "required": False
            }
        }
    }

    # FRAMES / FADEIN
    effects["plugins.core.effects.frames.fadein"] = {
        "description": "Fade in the frame.",
        "renders_on": {
            "frame": ["image"],
        },
        "configuration": {
            "duration": {
                "description": "The duration of the fade in. It's the time from the left side of frame timeline.",
                "type": "float",
                "default": 1,
                "required": False
            }
        }
    }

    # FRAMES / FADEOUT
    effects["plugins.core.effects.frames.fadeout"] = {
        "description": "Fade out the frame.",
        "renders_on": {
            "frame": ["image"],
        },
        "configuration": {
            "duration": {
                "description": "The duration of the fade in. It's the time from the right side of frame timeline.",
                "type": "float",
                "default": 1,
                "required": False
            }
        }
    }

    # FRAMES / AUDIO
    effects["plugins.core.effects.frames.audio"] = {
        "description": "Adds audio effect on frame.",
        "renders_on": {
            "frame": ["image"],
        },
        "configuration": {
            "file_path": {
                "description": "Path to the audio file.",
                "type": "str",
                "required": True
            },
            "subclip_start": {
                "description": "Setting the subclip will start the audio from the given time.",
                "type": "float",
                "required": False,
            }
        }
    }

    # FRAMES / RESIZE
    effects["plugins.core.effects.frames.resize"] = {
        "description": "Resize the frame with given mode.",
        "renders_on": {
            "frame": ["image"],
        },
        "configuration": {
            "mode": {
                "description": "Mode of the resize effect.",
                "type": "str",
                "required": False,
                "default": "default",
            },
        }
    }

    # FRAMES / BOUNCEIN
    effects["plugins.core.effects.frames.bouncein"] = {
        "description": "Bounce in the frame.",
        "renders_on": {
            "frame": ["image"],
        },
        "configuration": {
            "bounces": {
                "description": "How many times frame will bounce (change the sizes down and up).",
                "type": "float",
                "default": 4,
                "required": False
            },
            "shrink_factor": {
                "description": "Maximum shrink percentage. 0.2 means 20% of the original size.",
                "type": "float",
                "default": 0.02,
                "required": False
            },
            "randomize_shrink_factor": {
                "description": "Randomize the shrink factor for each bounce. "
                               "(the maximum shrink factor will be the shrink_factor value)",
                "type": "bool",
                "default": True,
                "required": False
            }
        }
    }


def register_file_loaders(file_loaders):
    file_loaders["yml"] = yaml_file_loader


def register_compilers(compilers):
    compilers["use_source"] = UseSourceCompiler()
    compilers["use_target"] = UseTargetCompiler()
    compilers["compose"] = ComposeCompiler()
    compilers["concatenate"] = ConcatenateCompiler()
    compilers["ignore"] = IgnoreCompiler()


def register(hooks):
    hooks.register_hook("videopy.modules.scenarios.register", register_scenarios)
    hooks.register_hook("videopy.modules.frames.register", register_frames)
    hooks.register_hook("videopy.modules.blocks.register", register_blocks)
    hooks.register_hook("videopy.modules.effects.register", register_effects)
    hooks.register_hook("videopy.modules.file_loaders.register", register_file_loaders)
    hooks.register_hook("videopy.modules.compilers.register", register_compilers)

    hooks.register_hook("videopy.scenario.frame.block.effects.before_load", load_effects_template)
