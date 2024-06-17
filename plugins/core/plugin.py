from plugins.core.compilers.compose import ComposeCompiler
from plugins.core.compilers.concacenate import ConcatenateCompiler
from plugins.core.compilers.ignore import IgnoreCompiler
from plugins.core.compilers.use_source import UseSourceCompiler
from plugins.core.compilers.use_target import UseTargetCompiler
from plugins.core.loaders.yaml import yaml_file_loader
from plugins.core.templates.load_effects_template import load_effects_template

__EFFECT_RESIZE_CENTER_CROP = {"type": f"plugins.core.effects.frames.resize", "configuration": {"mode": "center_crop"}}

__BASIC_SCENARIO = {"width": 640, "height": 240, "fps": 24}
__BASIC_DURATION = {"duration": 2}
__BASIC_IMAGE = "example/assets/image/1.jpg"

__PLUGIN_PREFIX = "plugins.core"


def register_scenarios(scenarios):
    scenarios["images_dir_to_video"] = {
        "file_path": "plugins/core/scenarios/images_dir_to_video/images_dir_to_video.yml",
    }


def register_frames(frames):
    frames[f"{__PLUGIN_PREFIX}.frames.image"] = {
        "description": "This frame will display an image.",
        "configuration": {
            "file_path": {
                "description": "The path to the image.",
                "type": "str",
                "required": True
            }
        },
        "examples": [
            {
                "name": "Showing Image as Frame",
                "description": "This example shows how to display an image as a frame.",
                "scenario": {
                    "width": 640,
                    "height": 240,
                    "fps": 24,
                    "frames": [
                        {
                            "type": f"{__PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": 0.1},
                            "configuration": {"file_path": __BASIC_IMAGE},
                            "effects": [__EFFECT_RESIZE_CENTER_CROP]
                        }
                    ]
                },
            }
        ]
    }

    frames[f"{__PLUGIN_PREFIX}.frames.video"] = {
        "description": "This frame will display an video.",
        "configuration": {
            "file_path": {
                "description": "The path to the video.",
                "type": "str",
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
    blocks[f"{__PLUGIN_PREFIX}.blocks.text"] = {
        "description": "This block will display text.",
        "configuration": {
            "content": {
                "description": "The text content.",
                "type": "str",
                "required": True
            },
            "font": {
                "description": "The font of the text.",
                "type": "str",
                "default": "Roboto-Bold",
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
                "type": "str",
                "default": "black",
                "required": False
            },
            "margin": {
                "description": "The margin of the text.",
                "type": "float",
                "default": 30,
                "required": False
            },
            "padding": {
                "description": "The padding of the text.",
                "type": "float",
                "default": 20,
                "required": False
            }
        },
        "examples": [
            {
                "name": "Showing Text as Block",
                "description": "This example shows how to display text as a block.",
                "tips": [
                    "Don't forget to use some display effect on text block to make it visible. (write, typewrite, etc.)"
                ],
                "scenario": {
                    "width": 640,
                    "height": 240,
                    "fps": 24,
                    "frames": [
                        {
                            "type": f"{__PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": 0.1},
                            "configuration": {"file_path": __BASIC_IMAGE},
                            "effects": [__EFFECT_RESIZE_CENTER_CROP],
                            "blocks": [
                                {
                                    "type": f"{__PLUGIN_PREFIX}.blocks.text",
                                    "time": {"duration": 0.1},
                                    "position": ["center", "center"],
                                    "configuration": {
                                        "content": "Hello, World!",
                                        "color": "white",
                                    },
                                    "effects": [
                                        {"type": f"{__PLUGIN_PREFIX}.effects.blocks.text.write",
                                         "time": {"duration": 0.1}},
                                    ]
                                }
                            ]
                        },
                    ]
                },
            }
        ]
    }
    blocks[f"{__PLUGIN_PREFIX}.blocks.audio"] = {
        "description": "This is base block to manage audio on frame",
        "configuration": {
            "file_path": {
                "description": "The path to the audio file.",
                "type": "str",
                "required": True
            }
        }
    }


def register_effects(effects):
    # BLOCKS / TEXT / WRITE
    effects[f"{__PLUGIN_PREFIX}.effects.blocks.text.write"] = {
        "description": "Write text on a block. This is a base effect if you want to display text.",
        "renders_on": {
            "block": ["text"]
        },
        "examples": [
            {
                "name": "Write Effect On Text Block",
                "description": "This example shows how to add write effect on text block.",
                "scenario": {
                    "width": 640,
                    "height": 240,
                    "fps": 24,
                    "frames": [
                        {
                            "type": f"{__PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": 0.1},
                            "configuration": {"file_path": __BASIC_IMAGE},
                            "effects": [__EFFECT_RESIZE_CENTER_CROP],
                            "blocks": [
                                {
                                    "type": f"{__PLUGIN_PREFIX}.blocks.text",
                                    "time": {"duration": 0.1},
                                    "position": ["center", "center"],
                                    "configuration": {
                                        "content": "Hello, World!",
                                        "color": "white",
                                    },
                                    "effects": [
                                        {"type": f"{__PLUGIN_PREFIX}.effects.blocks.text.write",
                                         "time": {"duration": 0.1}},
                                    ]
                                }
                            ]
                        }
                    ]
                },
            }
        ]
    }

    # BLOCKS / TEXT / TYPEWRITE
    effects[f"{__PLUGIN_PREFIX}.effects.blocks.text.typewrite"] = {
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
        },
        "examples": [
            {
                "name": "Typewrite Effect On Text Block",
                "description": "This example shows how to add typewrite effect on text block.",
                "scenario": {
                    "width": 640,
                    "height": 240,
                    "fps": 24,
                    "frames": [
                        {
                            "type": f"{__PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": 1},
                            "configuration": {"file_path": __BASIC_IMAGE},
                            "effects": [__EFFECT_RESIZE_CENTER_CROP],
                            "blocks": [
                                {
                                    "type": f"{__PLUGIN_PREFIX}.blocks.text",
                                    "time": {"duration": 1},
                                    "position": ["center", "center"],
                                    "configuration": {
                                        "content": "Hello, World!",
                                        "color": "white",
                                    },
                                    "effects": [
                                        {"type": f"{__PLUGIN_PREFIX}.effects.blocks.text.typewrite",
                                         "time": {"duration": 1}},
                                    ]
                                }
                            ]
                        }
                    ]
                },
            }
        ]
    }

    # BLOCKS / TEXT / BACKGROUND
    effects[f"{__PLUGIN_PREFIX}.effects.blocks.text.background"] = {
        "description": "Adds background to the frame.",
        "renders_on": {
            "block": ["text"]
        },
        "configuration": {
            "color": {
                "description": "The color of the background.",
                "type": "str",
                "default": "black",
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
        },
        "examples": [
            {
                "name": "Background Effect On Text Block",
                "description": "This example shows how to add background effect on text block.",
                "scenario": {
                    "width": 640,
                    "height": 240,
                    "fps": 24,
                    "frames": [
                        {
                            "type": f"{__PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": 0.1},
                            "configuration": {"file_path": __BASIC_IMAGE},
                            "effects": [__EFFECT_RESIZE_CENTER_CROP],
                            "blocks": [
                                {
                                    "type": f"{__PLUGIN_PREFIX}.blocks.text",
                                    "time": {"duration": 0.1},
                                    "position": ["center", "center"],
                                    "configuration": {
                                        "content": "Hello, World!",
                                        "color": "white",
                                    },
                                    "effects": [
                                        {"type": f"{__PLUGIN_PREFIX}.effects.blocks.text.write",
                                         "time": {"duration": 0.1}},
                                        {"type": f"{__PLUGIN_PREFIX}.effects.blocks.text.background",
                                         "time": {"duration": 0.1},
                                         "configuration": {"background_color": [0, 0, 0], "border_radius": 10},
                                         }
                                    ]
                                }
                            ]
                        }
                    ]
                },
            }
        ]
    }

    # BLOCKS / TEXT / FADEIN
    effects[f"{__PLUGIN_PREFIX}.effects.blocks.text.fadein"] = {
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
        },
        "examples": [
            {
                "name": "Fade In Effect On Text Block",
                "description": "This example shows how to add fade in effect on text block.",
                "scenario": {
                    "width": 640,
                    "height": 240,
                    "fps": 24,
                    "frames": [
                        {
                            "type": f"{__PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": 1},
                            "configuration": {"file_path": __BASIC_IMAGE},
                            "effects": [__EFFECT_RESIZE_CENTER_CROP],
                            "blocks": [
                                {
                                    "type": f"{__PLUGIN_PREFIX}.blocks.text",
                                    "time": {"duration": 1},
                                    "position": ["center", "center"],
                                    "configuration": {
                                        "content": "Hello, World!",
                                        "color": "white",
                                    },
                                    "effects": [
                                        {"type": f"{__PLUGIN_PREFIX}.effects.blocks.text.write",
                                         "time": {"duration": 1}},
                                        {"type": f"{__PLUGIN_PREFIX}.effects.blocks.text.background",
                                         "time": {"duration": 1},
                                         "configuration": {"background_color": [0, 0, 0], "border_radius": 10},
                                         },
                                        {"type": f"{__PLUGIN_PREFIX}.effects.blocks.text.fadein",
                                         "time": {"duration": 1}}
                                    ]
                                }
                            ]
                        }
                    ]
                },
            },
        ]
    }

    # BLOCKS / TEXT / FADEOUT
    effects[f"{__PLUGIN_PREFIX}.effects.blocks.text.fadeout"] = {
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
        },
        "examples": [
            {
                "name": "Fade Out Effect On Text Block",
                "description": "This example shows how to add fade out effect on text block.",
                "scenario": {
                    "width": 640,
                    "height": 240,
                    "fps": 24,
                    "frames": [
                        {
                            "type": f"{__PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": 1},
                            "configuration": {"file_path": __BASIC_IMAGE},
                            "effects": [__EFFECT_RESIZE_CENTER_CROP],
                            "blocks": [
                                {
                                    "type": f"{__PLUGIN_PREFIX}.blocks.text",
                                    "time": {"duration": 1},
                                    "position": ["center", "center"],
                                    "configuration": {
                                        "content": "Hello, World!",
                                        "color": "white",
                                    },
                                    "effects": [
                                        {"type": f"{__PLUGIN_PREFIX}.effects.blocks.text.write",
                                         "time": {"duration": 1}},
                                        {"type": f"{__PLUGIN_PREFIX}.effects.blocks.text.background",
                                         "time": {"duration": 1},
                                         "configuration": {"background_color": [0, 0, 0], "border_radius": 10},
                                         },
                                        {"type": f"{__PLUGIN_PREFIX}.effects.blocks.text.fadeout",
                                         "time": {"duration": 1}}
                                    ]
                                }
                            ]
                        }
                    ]
                },
            },
        ]
    }

    # BLOCKS / TEXT / SLIDEIN
    effects[f"{__PLUGIN_PREFIX}.effects.blocks.text.slidein"] = {
        "description": "Slide in the text block from given direction into target position.",
        "renders_on": {
            "block": ["text"]
        },
        "configuration": {
            "duration": {
                "description": "The duration of the slide in. It's the time from the left side of block timeline.",
                "type": "float",
                "default": 1,
                "required": False
            },
            "slide_from": {
                "description": "The direction of the slide in.",
                "type": "str",
                "default": "left",
                "required": False
            },
        },
        "examples": [
            {
                "name": "Text Block Slide In Effect",
                "description": "This example shows how to add slide in effect on text block.",
                "scenario": {
                    "width": 640,
                    "height": 240,
                    "fps": 24,
                    "frames": [
                        {
                            "type": f"{__PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": 1},
                            "configuration": {"file_path": __BASIC_IMAGE},
                            "effects": [__EFFECT_RESIZE_CENTER_CROP],
                            "blocks": [
                                {
                                    "type": f"{__PLUGIN_PREFIX}.blocks.text",
                                    "time": {"duration": 1},
                                    "position": ["center", "center"],
                                    "configuration": {
                                        "content": "Hello, World!",
                                        "color": "white",
                                    },
                                    "effects": [
                                        {"type": f"{__PLUGIN_PREFIX}.effects.blocks.text.write",
                                         "time": {"duration": 1}},
                                        {"type": f"{__PLUGIN_PREFIX}.effects.blocks.text.background",
                                         "time": {"duration": 1},
                                         "configuration": {"background_color": [0, 0, 0], "border_radius": 10},
                                         },
                                        {"type": f"{__PLUGIN_PREFIX}.effects.blocks.text.slidein",
                                         "configuration": {"slide_from": "top"}, "time": {"duration": 0.5}}
                                    ]
                                }
                            ]
                        }
                    ]
                },
            }
        ]
    }

    # BLOCKS / TEXT / SLIDEIN
    effects[f"{__PLUGIN_PREFIX}.effects.blocks.text.slideout"] = {
        "description": "Slide out the text block to given direction (until it's not visible).",
        "renders_on": {
            "block": ["text"]
        },
        "configuration": {
            "duration": {
                "description": "The duration of the slide out. It's the time from the right side of block timeline.",
                "type": "float",
                "default": 1,
                "required": False
            },
            "slide_to": {
                "description": "The direction of the slide out.",
                "type": "str",
                "default": "left",
                "required": False
            },
        },
        "examples": [
            {
                "name": "Text Block Slide Out Effect",
                "description": "This example shows how to add slide out effect on text block.",
                "scenario": {
                    "width": 640,
                    "height": 240,
                    "fps": 24,
                    "frames": [
                        {
                            "type": f"{__PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": 1},
                            "configuration": {"file_path": __BASIC_IMAGE},
                            "effects": [__EFFECT_RESIZE_CENTER_CROP],
                            "blocks": [
                                {
                                    "type": f"{__PLUGIN_PREFIX}.blocks.text",
                                    "time": {"duration": 1},
                                    "position": ["center", "center"],
                                    "configuration": {
                                        "content": "Hello, World!",
                                        "color": "white",
                                    },
                                    "effects": [
                                        {"type": f"{__PLUGIN_PREFIX}.effects.blocks.text.write",
                                         "time": {"duration": 1}},
                                        {"type": f"{__PLUGIN_PREFIX}.effects.blocks.text.background",
                                         "time": {"duration": 1},
                                         "configuration": {"background_color": [0, 0, 0], "border_radius": 10},
                                         },
                                        {"type": f"{__PLUGIN_PREFIX}.effects.blocks.text.slideout",
                                         "configuration": {"slide_to": "bottom"}, "time": {"duration": 0.5}}
                                    ]
                                }
                            ]
                        }
                    ]
                },
            }
        ]
    }

    # BLOCKS / AUDIO / PLAY
    effects[f"{__PLUGIN_PREFIX}.effects.blocks.audio.play"] = {
        "description": "Play audio on block.",
        "renders_on": {
            "block": ["audio"]
        },
        "configuration": {
            "subclip_start": {
                "description": "Setting the subclip will start the audio from the given time.",
                "type": "float",
                "default": 0,
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
    effects[f"{__PLUGIN_PREFIX}.effects.frames.fadein"] = {
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
        },
        "examples": [
            {
                "name": "Fade In effect on frame",
                "description": "This example shows how to add fade in effect on frame.",
                "scenario": {
                    "width": 640,
                    "height": 240,
                    "fps": 24,
                    "frames": [
                        {
                            "type": f"{__PLUGIN_PREFIX}.frames.image",
                            "time": __BASIC_DURATION,
                            "configuration": {"file_path": __BASIC_IMAGE},
                            "effects": [
                                __EFFECT_RESIZE_CENTER_CROP,
                                {"type": f"{__PLUGIN_PREFIX}.effects.frames.fadein", "time": {"duration": 1}}
                            ]
                        }
                    ]
                },
            }
        ]
    }

    # FRAMES / FADEOUT
    effects[f"{__PLUGIN_PREFIX}.effects.frames.fadeout"] = {
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
        },
        "examples": [
            {
                "name": "Fade Out effect on frame",
                "description": "This example shows how to add fade out effect on frame.",
                "scenario": {
                    "width": 640,
                    "height": 240,
                    "fps": 24,
                    "frames": [
                        {
                            "type": f"{__PLUGIN_PREFIX}.frames.image",
                            "time": __BASIC_DURATION,
                            "configuration": {"file_path": __BASIC_IMAGE},
                            "effects": [
                                __EFFECT_RESIZE_CENTER_CROP,
                                {"type": f"{__PLUGIN_PREFIX}.effects.frames.fadeout", "time": {"duration": 1}}
                            ]
                        }
                    ]
                },
            }
        ]
    }

    # FRAMES / AUDIO
    effects[f"{__PLUGIN_PREFIX}.effects.frames.audio"] = {
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
                "default": 0,
                "required": False,
            }
        }
    }

    # FRAMES / RESIZE
    effects[f"{__PLUGIN_PREFIX}.effects.frames.resize"] = {
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
        },
        "examples": [
            {
                "name": "Resize Effect - Fit",
                "description": "This example shows how to add 'fit' resize effect on frame.",
                "scenario": {
                    "width": 640,
                    "height": 240,
                    "fps": 24,
                    "frames": [
                        {
                            "type": f"{__PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": 0.1},
                            "configuration": {"file_path": __BASIC_IMAGE},
                            "effects": [
                                {"type": f"{__PLUGIN_PREFIX}.effects.frames.resize", "configuration": {"mode": "fit"}},
                            ]
                        }
                    ]
                },
            },
            {
                "name": "Resize Effect - Center crop",
                "description": "This example shows how to add 'center_crop' resize effect on frame.",
                "scenario": {
                    "width": 640,
                    "height": 240,
                    "fps": 24,
                    "frames": [
                        {
                            "type": f"{__PLUGIN_PREFIX}.frames.image",
                            "time": {"duration": 0.1},
                            "configuration": {"file_path": __BASIC_IMAGE},
                            "effects": [__EFFECT_RESIZE_CENTER_CROP]
                        }
                    ]
                },
            }
        ]
    }

    # FRAMES / BOUNCEIN
    effects[f"{__PLUGIN_PREFIX}.effects.frames.bouncein"] = {
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


def register_fields(fields):
    fields[f"{__PLUGIN_PREFIX}.fields.directory"] = {
        "description": "The path to the directory.",
    }

    fields[f"{__PLUGIN_PREFIX}.fields.output_path"] = {
        "description": "The path to the output file.",
    }

    fields[f"{__PLUGIN_PREFIX}.fields.resolution"] = {
        "description": "Video resolution selector.",
        "configuration": {
            "resolutions": {
                "required": False,
                "default": [
                    "1920x1080", "1280x720", "720x480", "640x480", "320x240",
                    "1080x1920", "720x1280", "480x720", "480x640", "240x320"
                ],
                "type": "list",
                "description": "List of resolutions to choose from."
            }
        }
    }

    fields[f"{__PLUGIN_PREFIX}.fields.fps"] = {
        "description": "Video FPS selector.",
        "configuration": {
            "fps": {
                "required": False,
                "default": {
                    "24 (Movie)": 24,
                    "25 (PAL / SECAM)": 25,
                    "30 (NTSC)": 30,
                    "50 (HDTV PAL)": 50,
                    "60 (HDTV NTSC)": 60,
                    "120 (HFR)": 120
                },
                "type": "list",
                "description": "List of fps to choose from."
            }
        }
    }

    fields[f"{__PLUGIN_PREFIX}.fields.text"] = {
        "description": "Simple text input",
    }

    fields[f"{__PLUGIN_PREFIX}.fields.timer"] = {
        "description": "Time input with hours, minutes and seconds."
    }

    fields[f"{__PLUGIN_PREFIX}.fields.media_selector"] = {
        "description": "Media selector",
        "configuration": {
            "extensions": {
                "required": False,
                "type": "str",
                "description": "Only provided extensions will be allowed to provide as the field value.",
                "default": ""
            },
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
    hooks.register_hook("videopy.modules.forms.fields.register", register_fields)

    hooks.register_hook("videopy.scenario.frame.block.effects.before_load", load_effects_template)
