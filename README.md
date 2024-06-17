# VideoPy

## What is VideoPy?

VideoPy is an application built on top of the MoviePy library, designed to streamline the process of creating videos
through the use of YAML files. By defining video scenarios in YAML, VideoPy allows users to automate common video
creation tasks, making it accessible even to those with minimal programming experience.

## How Does It Work?

With VideoPy, you can define aspects of your video in a simple, human-readable YAML file. Here’s an example:

```yaml
output_path: "outputs/example.mp4"
width: 640
height: 960
fps: 24
frames:
  - type: "plugins.core.frames.image"
    time:
      duration: 5
    configuration:
      file_path: "example/assets/image/1.jpg"
    blocks:
      - type: "plugins.core.blocks.text"
        position: [ center, bottom ]
        time:
          duration: 5
        configuration:
          content: "Image 1"
        effects:
          - type: "plugins.core.effects.blocks.text.typewrite"
            time:
              duration: 4
            configuration:
              duration_per_char: 0.1
          - type: "plugins.core.effects.blocks.text.background"
            time:
              duration: 5
            configuration:
              background_color: [ 255, 255, 255 ]
          - type: "plugins.core.effects.blocks.text.fadein"
            time:
              duration: 1
      - type: "plugins.core.blocks.audio"
        time:
          duration: 5
        configuration:
          file_path: "example/assets/audio/epic_sound.mp3"
        effects:
          - type: "plugins.core.effects.blocks.audio.play"
            time:
              duration: 5
    effects:
      - type: "plugins.core.effects.frames.resize"
        configuration:
          mode: "center_crop"
      - type: "plugins.core.effects.frames.fadein"
        time:
          duration: 1
```      

### In this scenario, the resulting video will:

- Have dimensions of **640x960** pixels and a frame rate of **24 fps**.
- Include a single **frame** displaying an image (`example/assets/image/1.jpg`).
- Display the block of type `text` containing the text: "Image 1" positioned at the bottom center and displayed with the "typewrite" **effect**.
- Play audio (`example/assets/audio/epic_sound.mp3`) for the duration of the **frame**.
- Apply a fade-in **effect** at the start.
- Resize the image to fit centrally.

## Why Use VideoPy?

### VideoPy simplifies and automates the video creation process by allowing you to:

- Define video scenarios in a straightforward YAML format.
- Automate repetitive video creation tasks, reducing the need for advanced video editing software.
- Create custom scripts in Python that generate YAML scenario files, offering flexibility for more advanced users.

# Installation

## Git

1. Clone the repository
2. Install the required dependencies using
```shell
pip install -r requirements.txt
```
3. Run the application using 
```shell
python videopy.py run --scenario-file example/scenario.yml
```

> More installation options coming in the future

# Modules

## What's a module?

Modules are the building blocks of VideoPy scenarios. They define the different components that make up a video, such as
frames, blocks, effects, and more. Each module has a specific purpose and can be combined to create video scenarios.

## Scenarios

### Creating scenario

1. Create fully using YAML files. (`example/scenario.yaml`)
2. Create using Python scripts that generate these YAML files (`plugins/core/scenarios/images_dir_to_video.py`).

### Using scenarios from plugins

To list available scenarios use:
```shell
python video.py scenarios
```

To get more information about a specific scenario use:
```shell
python video.py scenario __scenario_name__
```

## Frames

To list available frames use:
```shell
python video.py frames
```

To get more information about a specific frame use:
```shell
python video.py frame __frame_name__
```

## Blocks

To list available blocks use:
```shell
python video.py blocks
```

To get more information about a specific block use:
```shell
python video.py block __block_name__
```

## Effects

To list available effects use:
```shell
python video.py effects
```

To get more information about a specific effect use:
```shell
python video.py effect __effect_name__
```

> Each of the commands above will display a table containing information about given module.

# Examples:
# Frames
## plugins.core.frames.image
This frame will display an image.
### Showing Image as Frame
![plugins.core.frames.image - This frame will display an image. - Example 0](example/generated/plugins.core.frames.image_example_0.gif)
>This example shows how to display an image as a frame.


<details><summary>Example code</summary>

```yaml
{
  "width": 640,
  "height": 240,
  "fps": 24,
  "frames": [
    {
      "type": "plugins.core.frames.image",
      "time": {
        "duration": 5
      },
      "configuration": {
        "file_path": "example/assets/image/1.jpg"
      },
      "effects": [
        {
          "type": "plugins.core.effects.frames.resize",
          "configuration": {
            "mode": "center_crop"
          }
        }
      ]
    }
  ],
  "output_path": "example/generated/plugins.core.frames.image_example_0"
}
```

</details>

# Frame Effects
## plugins.core.effects.frames.fadein
Fade in the frame.
### Fade In effect on frame
![plugins.core.effects.frames.fadein - Fade in the frame. - Example 0](example/generated/plugins.core.effects.frames.fadein_example_0.gif)
>This example shows how to add fade in effect on frame.


<details><summary>Example code</summary>

```yaml
{
  "width": 640,
  "height": 240,
  "fps": 24,
  "frames": [
    {
      "type": "plugins.core.frames.image",
      "time": {
        "duration": 5
      },
      "configuration": {
        "file_path": "example/assets/image/1.jpg"
      },
      "effects": [
        {
          "type": "plugins.core.effects.frames.resize",
          "configuration": {
            "mode": "center_crop"
          }
        },
        {
          "type": "plugins.core.effects.frames.fadein",
          "time": {
            "duration": 4
          },
          "configuration": {
            "duration": 1
          }
        }
      ]
    }
  ],
  "output_path": "example/generated/plugins.core.effects.frames.fadein_example_0"
}
```

</details>

## plugins.core.effects.frames.fadeout
Fade out the frame.
### Fade Out effect on frame
![plugins.core.effects.frames.fadeout - Fade out the frame. - Example 0](example/generated/plugins.core.effects.frames.fadeout_example_0.gif)
>This example shows how to add fade out effect on frame.


<details><summary>Example code</summary>

```yaml
{
  "width": 640,
  "height": 240,
  "fps": 24,
  "frames": [
    {
      "type": "plugins.core.frames.image",
      "time": {
        "duration": 5
      },
      "configuration": {
        "file_path": "example/assets/image/1.jpg"
      },
      "effects": [
        {
          "type": "plugins.core.effects.frames.resize",
          "configuration": {
            "mode": "center_crop"
          }
        },
        {
          "type": "plugins.core.effects.frames.fadeout",
          "time": {
            "duration": 4
          },
          "configuration": {
            "duration": 1
          }
        }
      ]
    }
  ],
  "output_path": "example/generated/plugins.core.effects.frames.fadeout_example_0"
}
```

</details>

## plugins.core.effects.frames.resize
Resize the frame with given mode.
### Resize Effect - Fit
![plugins.core.effects.frames.resize - Resize the frame with given mode. - Example 0](example/generated/plugins.core.effects.frames.resize_example_0.gif)
>This example shows how to add 'fit' resize effect on frame.


<details><summary>Example code</summary>

```yaml
{
  "width": 640,
  "height": 240,
  "fps": 24,
  "frames": [
    {
      "type": "plugins.core.frames.image",
      "time": {
        "duration": 5
      },
      "configuration": {
        "file_path": "example/assets/image/1.jpg"
      },
      "effects": [
        {
          "type": "plugins.core.effects.frames.resize",
          "configuration": {
            "mode": "fit"
          }
        }
      ]
    }
  ],
  "output_path": "example/generated/plugins.core.effects.frames.resize_example_0"
}
```

</details>

### Resize Effect - Center crop
![plugins.core.effects.frames.resize - Resize the frame with given mode. - Example 1](example/generated/plugins.core.effects.frames.resize_example_1.gif)
>This example shows how to add 'center_crop' resize effect on frame.


<details><summary>Example code</summary>

```yaml
{
  "width": 640,
  "height": 240,
  "fps": 24,
  "frames": [
    {
      "type": "plugins.core.frames.image",
      "time": {
        "duration": 5
      },
      "configuration": {
        "file_path": "example/assets/image/1.jpg"
      },
      "effects": [
        {
          "type": "plugins.core.effects.frames.resize",
          "configuration": {
            "mode": "center_crop"
          }
        }
      ]
    }
  ],
  "output_path": "example/generated/plugins.core.effects.frames.resize_example_1"
}
```

</details>

# Blocks
## plugins.core.blocks.text
This block will display text.
### Showing Text as Block
![plugins.core.blocks.text - This block will display text. - Example 0](example/generated/plugins.core.blocks.text_example_0.gif)
>This example shows how to display text as a block.

> Don't forget to use some display effect on text block to make it visible. (write, typewrite, etc.)


<details><summary>Example code</summary>

```yaml
{
  "width": 640,
  "height": 240,
  "fps": 24,
  "frames": [
    {
      "type": "plugins.core.frames.image",
      "time": {
        "duration": 5
      },
      "configuration": {
        "file_path": "example/assets/image/1.jpg"
      },
      "effects": [
        {
          "type": "plugins.core.effects.frames.resize",
          "configuration": {
            "mode": "center_crop"
          }
        }
      ],
      "blocks": [
        {
          "type": "plugins.core.blocks.text",
          "time": {
            "duration": 5
          },
          "position": [
            "center",
            "center"
          ],
          "configuration": {
            "content": "Hello, World!",
            "color": "white",
            "font": "Roboto-Bold",
            "size": 50,
            "margin": 30,
            "padding": 20
          },
          "effects": [
            {
              "type": "plugins.core.effects.blocks.text.write",
              "time": {
                "duration": 5
              },
              "configuration": {}
            }
          ]
        }
      ]
    }
  ],
  "output_path": "example/generated/plugins.core.blocks.text_example_0"
}
```

</details>

# Blocks Effects
## plugins.core.effects.blocks.text.write
Write text on a block. This is a base effect if you want to display text.
### Write Effect On Text Block
![plugins.core.effects.blocks.text.write - Write text on a block. This is a base effect if you want to display text. - Example 0](example/generated/plugins.core.effects.blocks.text.write_example_0.gif)
>This example shows how to add write effect on text block.


<details><summary>Example code</summary>

```yaml
{
  "width": 640,
  "height": 240,
  "fps": 24,
  "frames": [
    {
      "type": "plugins.core.frames.image",
      "time": {
        "duration": 5
      },
      "configuration": {
        "file_path": "example/assets/image/1.jpg"
      },
      "effects": [
        {
          "type": "plugins.core.effects.frames.resize",
          "configuration": {
            "mode": "center_crop"
          }
        }
      ],
      "blocks": [
        {
          "type": "plugins.core.blocks.text",
          "time": {
            "duration": 5
          },
          "position": [
            "center",
            "center"
          ],
          "configuration": {
            "content": "Hello, World!",
            "color": "white",
            "font": "Roboto-Bold",
            "size": 50,
            "margin": 30,
            "padding": 20
          },
          "effects": [
            {
              "type": "plugins.core.effects.blocks.text.write",
              "time": {
                "duration": 5
              },
              "configuration": {}
            }
          ]
        }
      ]
    }
  ],
  "output_path": "example/generated/plugins.core.effects.blocks.text.write_example_0"
}
```

</details>

## plugins.core.effects.blocks.text.typewrite
This effect will type the text one the block.
### Typewrite Effect On Text Block
![plugins.core.effects.blocks.text.typewrite - This effect will type the text one the block. - Example 0](example/generated/plugins.core.effects.blocks.text.typewrite_example_0.gif)
>This example shows how to add typewrite effect on text block.


<details><summary>Example code</summary>

```yaml
{
  "width": 640,
  "height": 240,
  "fps": 24,
  "frames": [
    {
      "type": "plugins.core.frames.image",
      "time": {
        "duration": 5
      },
      "configuration": {
        "file_path": "example/assets/image/1.jpg"
      },
      "effects": [
        {
          "type": "plugins.core.effects.frames.resize",
          "configuration": {
            "mode": "center_crop"
          }
        }
      ],
      "blocks": [
        {
          "type": "plugins.core.blocks.text",
          "time": {
            "duration": 5
          },
          "position": [
            "center",
            "center"
          ],
          "configuration": {
            "content": "Hello, World!",
            "color": "white",
            "font": "Roboto-Bold",
            "size": 50,
            "margin": 30,
            "padding": 20
          },
          "effects": [
            {
              "type": "plugins.core.effects.blocks.text.typewrite",
              "time": {
                "duration": 5
              },
              "configuration": {
                "duration_per_char": 0
              }
            }
          ]
        }
      ]
    }
  ],
  "output_path": "example/generated/plugins.core.effects.blocks.text.typewrite_example_0"
}
```

</details>

## plugins.core.effects.blocks.text.background
Adds background to the frame.
### Background Effect On Text Block
![plugins.core.effects.blocks.text.background - Adds background to the frame. - Example 0](example/generated/plugins.core.effects.blocks.text.background_example_0.gif)
>This example shows how to add background effect on text block.


<details><summary>Example code</summary>

```yaml
{
  "width": 640,
  "height": 240,
  "fps": 24,
  "frames": [
    {
      "type": "plugins.core.frames.image",
      "time": {
        "duration": 5
      },
      "configuration": {
        "file_path": "example/assets/image/1.jpg"
      },
      "effects": [
        {
          "type": "plugins.core.effects.frames.resize",
          "configuration": {
            "mode": "center_crop"
          }
        }
      ],
      "blocks": [
        {
          "type": "plugins.core.blocks.text",
          "time": {
            "duration": 5
          },
          "position": [
            "center",
            "center"
          ],
          "configuration": {
            "content": "Hello, World!",
            "color": "white",
            "font": "Roboto-Bold",
            "size": 50,
            "margin": 30,
            "padding": 20
          },
          "effects": [
            {
              "type": "plugins.core.effects.blocks.text.write",
              "time": {
                "duration": 5
              },
              "configuration": {}
            },
            {
              "type": "plugins.core.effects.blocks.text.background",
              "time": {
                "duration": 5
              },
              "configuration": {
                "background_color": [
                  0,
                  0,
                  0
                ],
                "border_radius": 10,
                "color": "black",
                "opacity": 1
              }
            }
          ]
        }
      ]
    }
  ],
  "output_path": "example/generated/plugins.core.effects.blocks.text.background_example_0"
}
```

</details>

## plugins.core.effects.blocks.text.fadein
Fade in the text block.
### Fade In Effect On Text Block
![plugins.core.effects.blocks.text.fadein - Fade in the text block. - Example 0](example/generated/plugins.core.effects.blocks.text.fadein_example_0.gif)
>This example shows how to add fade in effect on text block.


<details><summary>Example code</summary>

```yaml
{
  "width": 640,
  "height": 240,
  "fps": 24,
  "frames": [
    {
      "type": "plugins.core.frames.image",
      "time": {
        "duration": 5
      },
      "configuration": {
        "file_path": "example/assets/image/1.jpg"
      },
      "effects": [
        {
          "type": "plugins.core.effects.frames.resize",
          "configuration": {
            "mode": "center_crop"
          }
        }
      ],
      "blocks": [
        {
          "type": "plugins.core.blocks.text",
          "time": {
            "duration": 5
          },
          "position": [
            "center",
            "center"
          ],
          "configuration": {
            "content": "Hello, World!",
            "color": "white",
            "font": "Roboto-Bold",
            "size": 50,
            "margin": 30,
            "padding": 20
          },
          "effects": [
            {
              "type": "plugins.core.effects.blocks.text.write",
              "time": {
                "duration": 5
              },
              "configuration": {}
            },
            {
              "type": "plugins.core.effects.blocks.text.background",
              "time": {
                "duration": 5
              },
              "configuration": {
                "background_color": [
                  0,
                  0,
                  0
                ],
                "border_radius": 10,
                "color": "black",
                "opacity": 1
              }
            },
            {
              "type": "plugins.core.effects.blocks.text.fadein",
              "time": {
                "duration": 2
              },
              "configuration": {
                "duration": 1
              }
            }
          ]
        }
      ]
    }
  ],
  "output_path": "example/generated/plugins.core.effects.blocks.text.fadein_example_0"
}
```

</details>

## plugins.core.effects.blocks.text.fadeout
Fade out the text block.
### Fade Out Effect On Text Block
![plugins.core.effects.blocks.text.fadeout - Fade out the text block. - Example 0](example/generated/plugins.core.effects.blocks.text.fadeout_example_0.gif)
>This example shows how to add fade out effect on text block.


<details><summary>Example code</summary>

```yaml
{
  "width": 640,
  "height": 240,
  "fps": 24,
  "frames": [
    {
      "type": "plugins.core.frames.image",
      "time": {
        "duration": 5
      },
      "configuration": {
        "file_path": "example/assets/image/1.jpg"
      },
      "effects": [
        {
          "type": "plugins.core.effects.frames.resize",
          "configuration": {
            "mode": "center_crop"
          }
        }
      ],
      "blocks": [
        {
          "type": "plugins.core.blocks.text",
          "time": {
            "duration": 5
          },
          "position": [
            "center",
            "center"
          ],
          "configuration": {
            "content": "Hello, World!",
            "color": "white",
            "font": "Roboto-Bold",
            "size": 50,
            "margin": 30,
            "padding": 20
          },
          "effects": [
            {
              "type": "plugins.core.effects.blocks.text.write",
              "time": {
                "duration": 5
              },
              "configuration": {}
            },
            {
              "type": "plugins.core.effects.blocks.text.background",
              "time": {
                "duration": 5
              },
              "configuration": {
                "background_color": [
                  0,
                  0,
                  0
                ],
                "border_radius": 10,
                "color": "black",
                "opacity": 1
              }
            },
            {
              "type": "plugins.core.effects.blocks.text.fadeout",
              "time": {
                "duration": 2
              },
              "configuration": {
                "duration": 1
              }
            }
          ]
        }
      ]
    }
  ],
  "output_path": "example/generated/plugins.core.effects.blocks.text.fadeout_example_0"
}
```

</details>

## plugins.core.effects.blocks.text.slidein
Slide in the text block from given direction into target position.
### Text Block Slide In Effect
![plugins.core.effects.blocks.text.slidein - Slide in the text block from given direction into target position. - Example 0](example/generated/plugins.core.effects.blocks.text.slidein_example_0.gif)
>This example shows how to add slide in effect on text block.


<details><summary>Example code</summary>

```yaml
{
  "width": 640,
  "height": 240,
  "fps": 24,
  "frames": [
    {
      "type": "plugins.core.frames.image",
      "time": {
        "duration": 5
      },
      "configuration": {
        "file_path": "example/assets/image/1.jpg"
      },
      "effects": [
        {
          "type": "plugins.core.effects.frames.resize",
          "configuration": {
            "mode": "center_crop"
          }
        }
      ],
      "blocks": [
        {
          "type": "plugins.core.blocks.text",
          "time": {
            "duration": 5
          },
          "position": [
            "center",
            "center"
          ],
          "configuration": {
            "content": "Hello, World!",
            "color": "white",
            "font": "Roboto-Bold",
            "size": 50,
            "margin": 30,
            "padding": 20
          },
          "effects": [
            {
              "type": "plugins.core.effects.blocks.text.write",
              "time": {
                "duration": 5
              },
              "configuration": {}
            },
            {
              "type": "plugins.core.effects.blocks.text.background",
              "time": {
                "duration": 5
              },
              "configuration": {
                "background_color": [
                  0,
                  0,
                  0
                ],
                "border_radius": 10,
                "color": "black",
                "opacity": 1
              }
            },
            {
              "type": "plugins.core.effects.blocks.text.slidein",
              "configuration": {
                "slide_from": "top",
                "duration": 1
              },
              "time": {
                "duration": 2
              }
            }
          ]
        }
      ]
    }
  ],
  "output_path": "example/generated/plugins.core.effects.blocks.text.slidein_example_0"
}
```

</details>

## plugins.core.effects.blocks.text.slideout
Slide out the text block to given direction (until it's not visible).
### Text Block Slide Out Effect
![plugins.core.effects.blocks.text.slideout - Slide out the text block to given direction (until it's not visible). - Example 0](example/generated/plugins.core.effects.blocks.text.slideout_example_0.gif)
>This example shows how to add slide out effect on text block.


<details><summary>Example code</summary>

```yaml
{
  "width": 640,
  "height": 240,
  "fps": 24,
  "frames": [
    {
      "type": "plugins.core.frames.image",
      "time": {
        "duration": 5
      },
      "configuration": {
        "file_path": "example/assets/image/1.jpg"
      },
      "effects": [
        {
          "type": "plugins.core.effects.frames.resize",
          "configuration": {
            "mode": "center_crop"
          }
        }
      ],
      "blocks": [
        {
          "type": "plugins.core.blocks.text",
          "time": {
            "duration": 5
          },
          "position": [
            "center",
            "center"
          ],
          "configuration": {
            "content": "Hello, World!",
            "color": "white",
            "font": "Roboto-Bold",
            "size": 50,
            "margin": 30,
            "padding": 20
          },
          "effects": [
            {
              "type": "plugins.core.effects.blocks.text.write",
              "time": {
                "duration": 5
              },
              "configuration": {}
            },
            {
              "type": "plugins.core.effects.blocks.text.background",
              "time": {
                "duration": 5
              },
              "configuration": {
                "background_color": [
                  0,
                  0,
                  0
                ],
                "border_radius": 10,
                "color": "black",
                "opacity": 1
              }
            },
            {
              "type": "plugins.core.effects.blocks.text.slideout",
              "configuration": {
                "slide_to": "bottom",
                "duration": 1
              },
              "time": {
                "duration": 2
              }
            }
          ]
        }
      ]
    }
  ],
  "output_path": "example/generated/plugins.core.effects.blocks.text.slideout_example_0"
}
```

</details>

