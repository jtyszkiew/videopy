from moviepy.editor import ImageClip
from PIL import Image, ImageDraw
import numpy as np

def rounded_background(width, height, color, radius):
    # Create an image with rounded corners
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(((0, 0), (width, height)), radius, fill=color)

    # Convert to numpy array and then to ColorClip
    np_image = np.array(image)
    return ImageClip(np_image, ismask=False)
