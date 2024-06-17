# [Frames] 
## Type: plugins.core.frames.image
This frame will display an image.
### Example: Showing Image as Frame
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
        "duration": 0.1
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

# [Frame Effects] 
## Type: plugins.core.effects.frames.fadein
Fade in the frame.
### Example: Fade In effect on frame
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
        "duration": 2
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
            "duration": 1
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

## Type: plugins.core.effects.frames.fadeout
Fade out the frame.
### Example: Fade Out effect on frame
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
        "duration": 2
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
            "duration": 1
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

## Type: plugins.core.effects.frames.resize
Resize the frame with given mode.
### Example: Resize Effect - Fit
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
        "duration": 0.1
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

### Example: Resize Effect - Center crop
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
        "duration": 0.1
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

# [Blocks] 
## Type: plugins.core.blocks.text
This block will display text.
### Example: Showing Text as Block
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
        "duration": 0.1
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
            "duration": 0.1
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
                "duration": 0.1
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

# [Blocks Effects] 
## Type: plugins.core.effects.blocks.text.write
Write text on a block. This is a base effect if you want to display text.
### Example: Write Effect On Text Block
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
        "duration": 0.1
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
            "duration": 0.1
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
                "duration": 0.1
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

## Type: plugins.core.effects.blocks.text.typewrite
This effect will type the text one the block.
### Example: Typewrite Effect On Text Block
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
        "duration": 1
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
            "duration": 1
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
                "duration": 1
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

## Type: plugins.core.effects.blocks.text.background
Adds background to the frame.
### Example: Background Effect On Text Block
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
        "duration": 0.1
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
            "duration": 0.1
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
                "duration": 0.1
              },
              "configuration": {}
            },
            {
              "type": "plugins.core.effects.blocks.text.background",
              "time": {
                "duration": 0.1
              },
              "configuration": {
                "color": [
                  0,
                  0,
                  0
                ],
                "border_radius": 10,
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

## Type: plugins.core.effects.blocks.text.fadein
Fade in the text block.
### Example: Fade In Effect On Text Block
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
        "duration": 1
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
            "duration": 1
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
                "duration": 1
              },
              "configuration": {}
            },
            {
              "type": "plugins.core.effects.blocks.text.background",
              "time": {
                "duration": 1
              },
              "configuration": {
                "color": [
                  0,
                  0,
                  0
                ],
                "border_radius": 10,
                "opacity": 1
              }
            },
            {
              "type": "plugins.core.effects.blocks.text.fadein",
              "time": {
                "duration": 1
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

## Type: plugins.core.effects.blocks.text.fadeout
Fade out the text block.
### Example: Fade Out Effect On Text Block
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
        "duration": 1
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
            "duration": 1
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
                "duration": 1
              },
              "configuration": {}
            },
            {
              "type": "plugins.core.effects.blocks.text.background",
              "time": {
                "duration": 1
              },
              "configuration": {
                "color": [
                  0,
                  0,
                  0
                ],
                "border_radius": 10,
                "opacity": 1
              }
            },
            {
              "type": "plugins.core.effects.blocks.text.fadeout",
              "time": {
                "duration": 1
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

## Type: plugins.core.effects.blocks.text.slidein
Slide in the text block from given direction into target position.
### Example: Text Block Slide In Effect
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
        "duration": 1
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
            "duration": 1
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
                "duration": 1
              },
              "configuration": {}
            },
            {
              "type": "plugins.core.effects.blocks.text.background",
              "time": {
                "duration": 1
              },
              "configuration": {
                "color": [
                  0,
                  0,
                  0
                ],
                "border_radius": 10,
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
                "duration": 0.5
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

## Type: plugins.core.effects.blocks.text.slideout
Slide out the text block to given direction (until it's not visible).
### Example: Text Block Slide Out Effect
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
        "duration": 1
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
            "duration": 1
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
                "duration": 1
              },
              "configuration": {}
            },
            {
              "type": "plugins.core.effects.blocks.text.background",
              "time": {
                "duration": 1
              },
              "configuration": {
                "color": [
                  0,
                  0,
                  0
                ],
                "border_radius": 10,
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
                "duration": 0.5
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

