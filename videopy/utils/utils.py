
def get_position_with_padding(position, clip_size, padding_percent, bg_width, bg_height):
    clip_width, clip_height = clip_size
    padding_x = clip_width * padding_percent / 100
    padding_y = clip_height * padding_percent / 100

    pos_x, pos_y = position
    if pos_x == "center":
        pos_x = (clip_width - bg_width) / 2
    elif pos_x == "left":
        pos_x = padding_x
    elif pos_x == "right":
        pos_x = clip_width - bg_width - padding_x

    if pos_y == "center":
        pos_y = (clip_height - bg_height) / 2
    elif pos_y == "top":
        pos_y = padding_y
    elif pos_y == "bottom":
        pos_y = clip_height - bg_height - padding_y

    return (pos_x, pos_y)
