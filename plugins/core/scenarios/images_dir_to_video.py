import os

from videopy.script import AbstractScript

image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp']
presets = [
    '1920x1080',
    '1280x720',
    '720x480',
    '640x480',
    '320x240',
    '1080x1920',
    '720x1280',
    '480x720',
    '480x640',
    '240x320'
]


class Script(AbstractScript):

    def __get_images(self):
        directory = self.ask("Enter the directory of the images", "images")

        images = self.__find_images(directory)
        if not images:
            raise ValueError(f"No images with extension {image_extensions} found in directory {directory}")

        self.sayInfo(f"Found <<{len(images)}>> images in directory <<{directory}>>")

        return images, directory

    def __get_resolution(self):
        resolution = self.ask(
            "Enter the resolution of the video (or type 'p' for presets, or type the preset number)",
            "1920x1080"
        )

        if resolution == 'p':
            self.sayInfo("Presets:")

            for index, preset in enumerate(presets):
                self.sayInfo(f"{index + 1}. {preset}")

            resolution = self.ask("Enter the preset number", presets[0])

            resolution = presets[int(resolution) - 1]
        elif 'x' not in resolution:
            try:
                resolution = presets[int(resolution) - 1]
            except IndexError:
                raise ValueError("Invalid preset number")

        return resolution.split('x')

    def __get_output_path(self, resolution, fps):
        output_path = self.ask("Enter the output path of the video",
                               f"outputs/output_{resolution}_{fps}.mp4")
        return output_path

    def run(self, hooks):
        images, directory = self.__get_images()
        resolution = self.__get_resolution()
        fps = self.ask("Enter the FPS of the video", 24)
        output_path = self.__get_output_path("x".join(resolution), fps)
        seconds_per_image = self.ask("How long each image should be displayed (in seconds)", 2)
        audio = self.ask("Audio path", "")

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

        for index, image in enumerate(images):
            blocks = []

            if audio:
                blocks.append({
                    "type": "plugins.core.blocks.audio",
                    "configuration": {
                        "file_path": audio
                    },
                    "time": {
                        "duration": seconds_per_image
                    },
                    "effects": [
                        {
                            "type": "plugins.core.effects.blocks.audio.play",
                            "configuration": {
                                "subclip_start": index * seconds_per_image,
                                "cut_to_block_duration": True
                            },
                            "time": {
                                "duration": seconds_per_image
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
                    "duration": seconds_per_image
                },
                "effects": frame_effects,
                "blocks": blocks + [
                    {
                        "type": "plugins.core.blocks.text",
                        "time": {
                            "duration": seconds_per_image
                        },
                        "position": ['center', 'bottom'],
                        "configuration": {
                            "content": f"Image {index + 1}/{len(images)}",
                        },
                        "effects": [
                            {
                                "type": "plugins.core.effects.blocks.text.typewrite",
                                "time": {
                                    "duration": seconds_per_image
                                },
                                "configuration": {
                                    "duration_per_char": 0.1
                                }
                            },
                            {
                                "type": "plugins.core.effects.blocks.text.background",
                                "time": {
                                    "duration": seconds_per_image
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
                    }
                ]
            })

    @staticmethod
    def __find_images(directory):
        images = []
        for file in os.listdir(directory):
            if file.split('.')[-1] in image_extensions:
                images.append(file)

        return images
