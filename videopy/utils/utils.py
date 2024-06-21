from moviepy.editor import TextClip


def transform_position(position, frame, block, margin=0):
    frame_width, frame_height = frame
    block_width, block_height = block
    pos_x, pos_y = position

    if pos_x == "center":
        pos_x = (frame_width - block_width) / 2
    elif pos_x == "left":
        pos_x = margin
    elif pos_x == "right":
        pos_x = frame_width - block_width - margin

    if pos_y == "center":
        pos_y = (frame_height - block_height) / 2
    elif pos_y == "top":
        pos_y = margin
    elif pos_y == "bottom":
        pos_y = frame_height - block_height - margin

    return pos_x, pos_y


def load_fonts():
    return TextClip("fonts").list('font')
