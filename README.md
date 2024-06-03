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
