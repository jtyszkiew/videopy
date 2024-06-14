import math
import os

from videopy.script import AbstractScript

image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp']


class Script(AbstractScript):

    def __init__(self, scenario_yml):
        super().__init__(scenario_yml)

    def run(self, hooks, data):
        images, directory = self.__find_images_and_texts(data['directory'])
        resolution = data['resolution']
        fps = data['fps']
        output_path = f"{data['output_path']}.mp4"
        frame_duration = data['frame_duration']
        audio = data.get('audio', None)
        title = data.get('title', None)

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

            if audio:
                blocks.append({
                    "type": "plugins.core.blocks.audio",
                    "configuration": {
                        "file_path": audio
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
                                "background_color": [255, 255, 255]
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
                                "background_color": [255, 255, 255]
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

    def __get_images(self, directory):
        images = self.__find_images(directory)
        if not images:
            raise ValueError(f"No images with extension {image_extensions} found in directory {directory}")

        self.say_info(f"Found <<{len(images)}>> images in directory <<{directory}>>")

        return images, directory

    def __get_resolution(self, resolution):
        return resolution.split('x')

    def __get_output_path(self, resolution, fps):
        output_path = self.ask("Enter the output path of the video",
                               f"outputs/output_{resolution}_{fps}.mp4")
        return output_path

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
