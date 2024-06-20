import math
import os

from videopy.script import AbstractScript

image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp']


class Script(AbstractScript):

    def __init__(self, scenario_yml):
        super().__init__(scenario_yml)

    def run(self, hooks, data):
        self.__validate_data(data)

        images, directory = self.__find_images_and_texts(data['directory']['directory'])
        resolution = data['display']['resolution']
        fps = data['display']['fps']
        output_path = f"{data['output']['directory']}/{data['output']['file_name']}.{data['output']['extension']}"
        frame_duration = data['frame_duration']['combined_time_in_seconds']
        audio = data.get('audio', None)
        title = data['title']['text'] if data.get('title', None) else None
        font = data['font']

        self.set_width(int(resolution[0]))
        self.set_height(int(resolution[1]))
        self.set_fps(int(fps))
        self.set_output_path(output_path)

        frame_effects = [
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
                }
            }
        ]

        for index, (image, text) in enumerate(images.items()):
            blocks = []

            if audio is not None:
                blocks.append({
                    "type": "plugins.core.blocks.audio",
                    "configuration": {
                        "file_path": audio['path']
                    },
                    "time": {
                        "duration": frame_duration
                    },
                    "effects": [
                        {
                            "type": "plugins.core.effects.blocks.audio.play",
                            "configuration": {
                                "subclip_start": index * frame_duration,
                                "cut_to_block_duration": True
                            },
                            "time": {
                                "duration": frame_duration
                            }
                        }
                    ]
                })

            text_content = text if text is not None else f"Image {index + 1}/{len(images)}"

            if title is not None and index is 0:
                blocks.append({
                    "type": "plugins.core.blocks.text",
                    "time": {
                        "duration": math.floor(frame_duration * 50 / 100)
                    },
                    "position": ['center', resolution[1] * 10 / 100],
                    "configuration": {
                        "content": title,
                        "size": font.get('size', 50),
                        "font": font.get('font', 'Arial'),
                        "color": font.get('color', [255, 255, 255])
                    },
                    "effects": [
                        {
                            "type": "plugins.core.effects.blocks.text.write",
                            "time": {
                                "duration": math.floor(frame_duration * 50 / 100)
                            }
                        },
                        {
                            "type": "plugins.core.effects.blocks.text.background",
                            "time": {
                                "duration": math.floor(frame_duration * 50 / 100)
                            },
                            "configuration": {
                                "color": [255, 255, 255]
                            }
                        },
                        {
                            "type": "plugins.core.effects.blocks.text.fadein",
                            "time": {
                                "duration": 1
                            }
                        }
                    ]
                })

            if text is not None:
                blocks.append({
                    "type": "plugins.core.blocks.text",
                    "time": {
                        "duration": frame_duration
                    },
                    "position": ['center', resolution[1] - (resolution[1] * 20 / 100)],
                    "configuration": {
                        "content": text_content,
                        "size": font.get('size', 50),
                        "font": font.get('font', 'Arial'),
                        "color": font.get('color', [255, 255, 255])
                    },
                    "effects": [
                        {
                            "type": "plugins.core.effects.blocks.text.write",
                            "time": {
                                "duration": frame_duration
                            }
                        },
                        {
                            "type": "plugins.core.effects.blocks.text.background",
                            "time": {
                                "duration": frame_duration
                            },
                            "configuration": {
                                "color": [255, 255, 255]
                            }
                        },
                        {
                            "type": "plugins.core.effects.blocks.text.fadein",
                            "time": {
                                "duration": 1
                            }
                        }
                    ]
                })

            self.scenario_yml['frames'].append({
                "type": "plugins.core.frames.image",
                "configuration": {
                    "file_path": os.path.join(directory, image),
                },
                "time": {
                    "start": 0,
                    "duration": frame_duration
                },
                "effects": frame_effects,
                "blocks": blocks
            })

    def __validate_data(self, data):
        if not data.get('directory', None):
            raise ValueError("Directory is required")
        elif data['directory'].get('directory', None) is None:
            raise ValueError("Fields should pass data as subfields -> directory: {directory: '/path'}")

        if not data.get('display', None):
            raise ValueError("Display is required")
        elif data['display'].get('resolution', None) is None:
            raise ValueError("Fields should pass data as subfields -> display: {resolution: [1920, 1080], fps: 30}")

        if not data.get('output', None):
            raise ValueError("Output is required")
        elif data['output'].get('directory', None) is None:
            raise ValueError("Fields should pass data as subfields "
                             "-> output: {directory: '/path', file_name: 'name', extension: 'mp4'}")

        if not data.get('frame_duration', None):
            raise ValueError("Frame duration is required")
        elif data['frame_duration'].get('combined_time_in_seconds', None) is None:
            raise ValueError("Fields should pass data as subfields -> frame_duration: {combined_time_in_seconds: 5}")

        if not data.get('font', None):
            raise ValueError("Font is required")
        elif data['font'].get('font', None) is None:
            raise ValueError(
                "Fields should pass data as subfields -> font: {font: 'Arial', size: 50, color: [255, 255, 255]}")

    def __get_images(self, directory):
        images = self.__find_images(directory)
        if not images:
            raise ValueError(f"No images with extension {image_extensions} found in directory {directory}")

        self.say_info(f"Found <<{len(images)}>> images in directory <<{directory}>>")

        return images, directory

    def __find_images(self, directory):
        images = []
        for file in os.listdir(directory):
            if file.split('.')[-1] in image_extensions:
                images.append(file)

        return images

    def __find_images_and_texts(self, directory):
        images_and_texts = {}
        images = self.__find_images(directory)

        for image in images:
            base_name = os.path.splitext(image)[0]
            txt_file_path = os.path.join(directory, f"{base_name}.txt")

            if os.path.exists(txt_file_path):
                with open(txt_file_path, 'r') as file:
                    images_and_texts[image] = file.read().strip()
            else:
                images_and_texts[image] = None

        return images_and_texts, directory
