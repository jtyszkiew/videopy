# Table of contents
- [Frames](#frames)
  - [plugins.core.frames.image](#pluginscoreframesimage)
  - [plugins.core.frames.video](#pluginscoreframesvideo)
- [Frame Effects](#frame-effects)
  - [plugins.core.effects.frames.fadein](#pluginscoreeffectsframesfadein)
  - [plugins.core.effects.frames.fadeout](#pluginscoreeffectsframesfadeout)
  - [plugins.core.effects.frames.audio](#pluginscoreeffectsframesaudio)
  - [plugins.core.effects.frames.resize](#pluginscoreeffectsframesresize)
  - [plugins.core.effects.frames.bouncein](#pluginscoreeffectsframesbouncein)
- [Blocks](#blocks)
  - [plugins.core.blocks.text](#pluginscoreblockstext)
  - [plugins.core.blocks.audio](#pluginscoreblocksaudio)
- [Block Effects](#block-effects)
  - [plugins.core.effects.blocks.text.write](#pluginscoreeffectsblockstextwrite)
  - [plugins.core.effects.blocks.text.typewrite](#pluginscoreeffectsblockstexttypewrite)
  - [plugins.core.effects.blocks.text.background](#pluginscoreeffectsblockstextbackground)
  - [plugins.core.effects.blocks.text.fadein](#pluginscoreeffectsblockstextfadein)
  - [plugins.core.effects.blocks.text.fadeout](#pluginscoreeffectsblockstextfadeout)
  - [plugins.core.effects.blocks.text.slidein](#pluginscoreeffectsblockstextslidein)
  - [plugins.core.effects.blocks.text.slideout](#pluginscoreeffectsblockstextslideout)
  - [plugins.core.effects.blocks.audio.play](#pluginscoreeffectsblocksaudioplay)
# Frames 
## plugins.core.frames.image
Image frame will use image passed in `configuration.file_path` as background. You can build blocks on top of it.
### Example: Showing Image as Frame
![plugins.core.frames.image - Image frame will use image passed in `configuration.file_path` as background. You can build blocks on top of it. - Example 0](outputs/examples/plugins.core.frames.image_example_0.gif)
>Example is showing how to set image as a frame, as the image size don't match the scenario size (640x240), it will additionally use the [plugins.core.effects.frames.resize](#pluginscoreeffectsframesresize) effect to center crop it.

> Example have a duration of 0.1 seconds for test purposes and generation speed. In real life you probably want a longer duration.


<details><summary>Example code</summary>

```yaml
frames:
- type: plugins.core.frames.image
  time:
    duration: 0.1
  configuration:
    file_path: example/assets/image/1.jpg
  effects:
  - type: plugins.core.effects.frames.resize
    configuration:
      mode: center_crop
    vars:
      frame: &id001
        scenario: {}
  vars: *id001
width: 640
height: 240
fps: 24
output_path: outputs/examples/plugins.core.frames.image_example_0.gif

```

</details>

<details><summary>Configuration</summary>

| Configuration | Description | Type | Required | Default Value |
| --- | --- | --- | --- | --- |
| file_path | The path to the image. | str | Yes | None |


</details>


---
## plugins.core.frames.video
This frame will display an video.
### Example: Showing Video as Frame
![plugins.core.frames.video - This frame will display an video. - Example 0](outputs/examples/plugins.core.frames.video_example_0.gif)
>Example is showing how to set video as a frame, as the video size don't match the scenario size (640x240), it will additionally use the [plugins.core.effects.frames.resize](#pluginscoreeffectsframesresize) effect to center crop it.

> Example have a duration of 1 seconds for test purposes and generation speed. In real life you probably want a longer duration.


<details><summary>Example code</summary>

```yaml
frames:
- type: plugins.core.frames.video
  time:
    duration: 1
  configuration:
    file_path: example/assets/video/BigBuckBunny_640x240.mp4
  effects:
  - type: plugins.core.effects.frames.resize
    configuration:
      mode: center_crop
    vars:
      frame: &id001
        scenario: {}
  vars: *id001
width: 640
height: 240
fps: 24
output_path: outputs/examples/plugins.core.frames.video_example_0.gif

```

</details>

<details><summary>Configuration</summary>

| Configuration | Description | Type | Required | Default Value |
| --- | --- | --- | --- | --- |
| file_path | The path to the video. | str | Yes | None |
| mute | Mute the source video (for example if you want to compose the sound differently). | bool | No | False |
| subclip_start | Setting the subclip will start the video from the given time. | float | No | 0 |
| cut_to_frame_duration | If video is longer than frame duration, cut it to frame duration. | bool | No | True |


</details>


---
# Frame Effects 
## plugins.core.effects.frames.fadein
Fade in the frame.
### Example: Fade In effect on frame
![plugins.core.effects.frames.fadein - Fade in the frame. - Example 0](outputs/examples/plugins.core.effects.frames.fadein_example_0.gif)
>Effect will slowly fade in the frame content.

> This effect ignores the `time.start` parameter, as it always starts from the beginning of the frame.


<details><summary>Example code</summary>

```yaml
frames:
- type: plugins.core.frames.image
  time:
    duration: 1
  configuration:
    file_path: example/assets/image/1.jpg
  effects:
  - type: plugins.core.effects.frames.resize
    configuration:
      mode: center_crop
    vars:
      frame: &id001
        scenario: {}
  - type: plugins.core.effects.frames.fadein
    time:
      duration: 0.5
    vars:
      frame: *id001
    configuration: {}
  vars: *id001
width: 640
height: 240
fps: 24
output_path: outputs/examples/plugins.core.effects.frames.fadein_example_0.gif

```

</details>


---
## plugins.core.effects.frames.fadeout
Fade out the frame.
### Example: Fade Out effect on frame
![plugins.core.effects.frames.fadeout - Fade out the frame. - Example 0](outputs/examples/plugins.core.effects.frames.fadeout_example_0.gif)
>Effect will slowly fade out the frame content.

> This effect ignores the `time.start` parameter, as it always starts from the (`frame.time.duration` - `effect.time.duration`) (right side) of the frame.


<details><summary>Example code</summary>

```yaml
frames:
- type: plugins.core.frames.image
  time:
    duration: 1
  configuration:
    file_path: example/assets/image/1.jpg
  effects:
  - type: plugins.core.effects.frames.resize
    configuration:
      mode: center_crop
    vars:
      frame: &id001
        scenario: {}
  - type: plugins.core.effects.frames.fadeout
    time:
      duration: 0.5
    vars:
      frame: *id001
    configuration: {}
  vars: *id001
width: 640
height: 240
fps: 24
output_path: outputs/examples/plugins.core.effects.frames.fadeout_example_0.gif

```

</details>


---
## plugins.core.effects.frames.audio
Adds audio effect on frame.
<details><summary>Configuration</summary>

| Configuration | Description | Type | Required | Default Value |
| --- | --- | --- | --- | --- |
| file_path | Path to the audio file. | str | Yes | None |
| subclip_start | Setting the subclip will start the audio from the given time. | float | No | 0 |


</details>


---
## plugins.core.effects.frames.resize
Resize the frame with given mode.
### Example: Resize Effect - Fit
![plugins.core.effects.frames.resize - Resize the frame with given mode. - Example 0](outputs/examples/plugins.core.effects.frames.resize_example_0.gif)
>This example shows how to add 'fit' resize effect on frame.


<details><summary>Example code</summary>

```yaml
frames:
- type: plugins.core.frames.image
  time:
    duration: 0.1
  configuration:
    file_path: example/assets/image/1.jpg
  effects:
  - type: plugins.core.effects.frames.resize
    configuration:
      mode: fit
    vars:
      frame: &id001
        scenario: {}
  vars: *id001
width: 640
height: 240
fps: 24
output_path: outputs/examples/plugins.core.effects.frames.resize_example_0.gif

```

</details>

### Example: Resize Effect - Center crop
![plugins.core.effects.frames.resize - Resize the frame with given mode. - Example 1](outputs/examples/plugins.core.effects.frames.resize_example_1.gif)
>This example shows how to add 'center_crop' resize effect on frame.


<details><summary>Example code</summary>

```yaml
frames:
- type: plugins.core.frames.image
  time:
    duration: 0.1
  configuration:
    file_path: example/assets/image/1.jpg
  effects:
  - type: plugins.core.effects.frames.resize
    configuration:
      mode: center_crop
    vars:
      frame: &id001
        scenario: {}
  vars: *id001
width: 640
height: 240
fps: 24
output_path: outputs/examples/plugins.core.effects.frames.resize_example_1.gif

```

</details>

<details><summary>Configuration</summary>

| Configuration | Description | Type | Required | Default Value |
| --- | --- | --- | --- | --- |
| mode | Mode of the resize effect. | str | No | default |


</details>


---
## plugins.core.effects.frames.bouncein
Bounce in the frame.
<details><summary>Configuration</summary>

| Configuration | Description | Type | Required | Default Value |
| --- | --- | --- | --- | --- |
| bounces | How many times frame will bounce (change the sizes down and up). | float | No | 4 |
| shrink_factor | Maximum shrink percentage. 0.2 means 20% of the original size. | float | No | 0.02 |
| randomize_shrink_factor | Randomize the shrink factor for each bounce. (the maximum shrink factor will be the shrink_factor value) | bool | No | True |


</details>


---
# Blocks 
## plugins.core.blocks.text
This block will display text.
### Example: Showing Text
![plugins.core.blocks.text - This block will display text. - Example 0](outputs/examples/plugins.core.blocks.text_example_0.gif)
>This example shows how to display text as a block.

> This block doesn't show anything by default.

> Don't forget to use some display effect on text block to make it visible. ([plugins.core.effects.block.text.write](pluginscoreeffectsblocktextwrite), [plugins.core.effects.block.text.typewrite](pluginscoreeffectsblocktexttypewrite)).


<details><summary>Example code</summary>

```yaml
frames:
- type: plugins.core.frames.image
  time: &id001
    duration: 0.1
  configuration:
    file_path: example/assets/image/1.jpg
  effects:
  - type: plugins.core.effects.frames.resize
    configuration:
      mode: center_crop
    vars:
      frame: &id002
        scenario: {}
  blocks:
  - type: plugins.core.blocks.text
    time: *id001
    position:
    - center
    - center
    configuration:
      content: Hello, World!
      color: white
      font: Roboto-Bold
      size: 50
      margin: 30
      padding: 20
    effects:
    - type: plugins.core.effects.blocks.text.write
      time:
        duration: 0.1
      vars:
        block: &id003
          frame: *id002
      configuration: {}
    vars: *id003
  vars: *id002
width: 640
height: 240
fps: 24
output_path: outputs/examples/plugins.core.blocks.text_example_0.gif

```

</details>

<details><summary>Configuration</summary>

| Configuration | Description | Type | Required | Default Value |
| --- | --- | --- | --- | --- |
| content | The text content. | str | Yes | None |
| font | The font of the text. | str | No | Roboto-Bold |
| size | The size of the text. | int | No | 50 |
| color | The color of the text. | str | No | black |
| margin | The margin of the text. | float | No | 30 |
| padding | The padding of the text. | float | No | 20 |


</details>


---
## plugins.core.blocks.audio
This is base block to manage audio on frame
<details><summary>Configuration</summary>

| Configuration | Description | Type | Required | Default Value |
| --- | --- | --- | --- | --- |
| file_path | The path to the audio file. | str | Yes | None |


</details>


---
# Blocks Effects 
## plugins.core.effects.blocks.text.write
Write text on a block. This is a base effect if you want to display text.
### Example: Write Effect On Text Block
![plugins.core.effects.blocks.text.write - Write text on a block. This is a base effect if you want to display text. - Example 0](outputs/examples/plugins.core.effects.blocks.text.write_example_0.gif)
>This is basic effect to display any text. It will write the text on the block.

> No configuration is accepted, as this effect inherits the configuration from [plugins.core.blocks.text](#pluginscoreblockstext).


<details><summary>Example code</summary>

```yaml
frames:
- type: plugins.core.frames.image
  time: &id001
    duration: 0.1
  configuration:
    file_path: example/assets/image/1.jpg
  effects:
  - type: plugins.core.effects.frames.resize
    configuration:
      mode: center_crop
    vars:
      frame: &id002
        scenario: {}
  blocks:
  - type: plugins.core.blocks.text
    time: *id001
    position:
    - center
    - center
    configuration:
      content: Hello, World!
      color: white
      font: Roboto-Bold
      size: 50
      margin: 30
      padding: 20
    effects:
    - type: plugins.core.effects.blocks.text.write
      time:
        duration: 0.1
      vars:
        block: &id003
          frame: *id002
      configuration: {}
    vars: *id003
  vars: *id002
width: 640
height: 240
fps: 24
output_path: outputs/examples/plugins.core.effects.blocks.text.write_example_0.gif

```

</details>


---
## plugins.core.effects.blocks.text.typewrite
This effect will type the text one the block.
### Example: Typewrite Effect On Text Block
![plugins.core.effects.blocks.text.typewrite - This effect will type the text one the block. - Example 0](outputs/examples/plugins.core.effects.blocks.text.typewrite_example_0.gif)
>This example shows how to add typewrite effect on text block.


<details><summary>Example code</summary>

```yaml
frames:
- type: plugins.core.frames.image
  time:
    duration: 1
  configuration:
    file_path: example/assets/image/1.jpg
  effects:
  - type: plugins.core.effects.frames.resize
    configuration:
      mode: center_crop
    vars:
      frame: &id001
        scenario: {}
  blocks:
  - type: plugins.core.blocks.text
    time:
      duration: 1
    position:
    - center
    - center
    configuration:
      content: Hello, World!
      color: white
      font: Roboto-Bold
      size: 50
      margin: 30
      padding: 20
    effects:
    - type: plugins.core.effects.blocks.text.typewrite
      time:
        duration: 1
      vars:
        block: &id002
          frame: *id001
      configuration:
        duration_per_char: 0
    vars: *id002
  vars: *id001
width: 640
height: 240
fps: 24
output_path: outputs/examples/plugins.core.effects.blocks.text.typewrite_example_0.gif

```

</details>

<details><summary>Configuration</summary>

| Configuration | Description | Type | Required | Default Value |
| --- | --- | --- | --- | --- |
| duration_per_char | The duration each character takes to appear. If not set it will be calculated based on the duration of the effect. (duration / len(text)) | float | No | 0 |


</details>


---
## plugins.core.effects.blocks.text.background
Adds background to the block.
### Example: Background Effect On Text Block
![plugins.core.effects.blocks.text.background - Adds background to the block. - Example 0](outputs/examples/plugins.core.effects.blocks.text.background_example_0.gif)
>This example shows how to add background effect on text block.


<details><summary>Example code</summary>

```yaml
frames:
- type: plugins.core.frames.image
  time: &id001
    duration: 0.1
  configuration:
    file_path: example/assets/image/1.jpg
  effects:
  - type: plugins.core.effects.frames.resize
    configuration:
      mode: center_crop
    vars:
      frame: &id002
        scenario: {}
  blocks:
  - type: plugins.core.blocks.text
    time: *id001
    position:
    - center
    - center
    configuration:
      content: Hello, World!
      color: white
      font: Roboto-Bold
      size: 50
      margin: 30
      padding: 20
    effects:
    - type: plugins.core.effects.blocks.text.write
      time:
        duration: 0.1
      vars:
        block: &id003
          frame: *id002
      configuration: {}
    - type: plugins.core.effects.blocks.text.background
      time:
        duration: 0.1
      configuration:
        color:
        - 0
        - 0
        - 0
        border_radius: 10
        opacity: 1
      vars:
        block: *id003
    vars: *id003
  vars: *id002
width: 640
height: 240
fps: 24
output_path: outputs/examples/plugins.core.effects.blocks.text.background_example_0.gif

```

</details>

<details><summary>Configuration</summary>

| Configuration | Description | Type | Required | Default Value |
| --- | --- | --- | --- | --- |
| color | The color of the background. | str | No | black |
| opacity | The opacity of the background. | float | No | 1 |
| border_radius | The border radius of the background. | float | No | 10 |


</details>


---
## plugins.core.effects.blocks.text.fadein
Fade in the text block.
### Example: Fade In Effect On Text Block
![plugins.core.effects.blocks.text.fadein - Fade in the text block. - Example 0](outputs/examples/plugins.core.effects.blocks.text.fadein_example_0.gif)
>This example shows how to add fade in effect on text block.


<details><summary>Example code</summary>

```yaml
frames:
- type: plugins.core.frames.image
  time:
    duration: 1
  configuration:
    file_path: example/assets/image/1.jpg
  effects:
  - type: plugins.core.effects.frames.resize
    configuration:
      mode: center_crop
    vars:
      frame: &id001
        scenario: {}
  blocks:
  - type: plugins.core.blocks.text
    time:
      duration: 1
    position:
    - center
    - center
    configuration:
      content: Hello, World!
      color: white
      font: Roboto-Bold
      size: 50
      margin: 30
      padding: 20
    effects:
    - type: plugins.core.effects.blocks.text.write
      time:
        duration: 1
      vars:
        block: &id002
          frame: *id001
      configuration: {}
    - type: plugins.core.effects.blocks.text.background
      time:
        duration: 1
      configuration:
        color:
        - 0
        - 0
        - 0
        border_radius: 10
        opacity: 1
      vars:
        block: *id002
    - type: plugins.core.effects.blocks.text.fadein
      time:
        duration: 1
      vars:
        block: *id002
      configuration: {}
    vars: *id002
  vars: *id001
width: 640
height: 240
fps: 24
output_path: outputs/examples/plugins.core.effects.blocks.text.fadein_example_0.gif

```

</details>


---
## plugins.core.effects.blocks.text.fadeout
Fade out the text block.
### Example: Fade Out Effect On Text Block
![plugins.core.effects.blocks.text.fadeout - Fade out the text block. - Example 0](outputs/examples/plugins.core.effects.blocks.text.fadeout_example_0.gif)
>This example shows how to add fade out effect on text block.


<details><summary>Example code</summary>

```yaml
frames:
- type: plugins.core.frames.image
  time:
    duration: 1
  configuration:
    file_path: example/assets/image/1.jpg
  effects:
  - type: plugins.core.effects.frames.resize
    configuration:
      mode: center_crop
    vars:
      frame: &id001
        scenario: {}
  blocks:
  - type: plugins.core.blocks.text
    time:
      duration: 1
    position:
    - center
    - center
    configuration:
      content: Hello, World!
      color: white
      font: Roboto-Bold
      size: 50
      margin: 30
      padding: 20
    effects:
    - type: plugins.core.effects.blocks.text.write
      time:
        duration: 1
      vars:
        block: &id002
          frame: *id001
      configuration: {}
    - type: plugins.core.effects.blocks.text.background
      time:
        duration: 1
      configuration:
        color:
        - 0
        - 0
        - 0
        border_radius: 10
        opacity: 1
      vars:
        block: *id002
    - type: plugins.core.effects.blocks.text.fadeout
      time:
        duration: 1
      vars:
        block: *id002
      configuration: {}
    vars: *id002
  vars: *id001
width: 640
height: 240
fps: 24
output_path: outputs/examples/plugins.core.effects.blocks.text.fadeout_example_0.gif

```

</details>


---
## plugins.core.effects.blocks.text.slidein
Slide in the text block from given direction into target position.
### Example: Text Block Slide In Effect
![plugins.core.effects.blocks.text.slidein - Slide in the text block from given direction into target position. - Example 0](outputs/examples/plugins.core.effects.blocks.text.slidein_example_0.gif)
>This example shows how to add slide in effect on text block.


<details><summary>Example code</summary>

```yaml
frames:
- type: plugins.core.frames.image
  time:
    duration: 1
  configuration:
    file_path: example/assets/image/1.jpg
  effects:
  - type: plugins.core.effects.frames.resize
    configuration:
      mode: center_crop
    vars:
      frame: &id001
        scenario: {}
  blocks:
  - type: plugins.core.blocks.text
    time:
      duration: 1
    position:
    - center
    - center
    configuration:
      content: Hello, World!
      color: white
      font: Roboto-Bold
      size: 50
      margin: 30
      padding: 20
    effects:
    - type: plugins.core.effects.blocks.text.write
      time:
        duration: 1
      vars:
        block: &id002
          frame: *id001
      configuration: {}
    - type: plugins.core.effects.blocks.text.background
      time:
        duration: 1
      configuration:
        color:
        - 0
        - 0
        - 0
        border_radius: 10
        opacity: 1
      vars:
        block: *id002
    - type: plugins.core.effects.blocks.text.slidein
      configuration:
        slide_from: top
      time:
        duration: 0.5
      vars:
        block: *id002
    vars: *id002
  vars: *id001
width: 640
height: 240
fps: 24
output_path: outputs/examples/plugins.core.effects.blocks.text.slidein_example_0.gif

```

</details>

<details><summary>Configuration</summary>

| Configuration | Description | Type | Required | Default Value |
| --- | --- | --- | --- | --- |
| slide_from | The direction of the slide in. | str | No | left |


</details>


---
## plugins.core.effects.blocks.text.slideout
Slide out the text block to given direction (until it's not visible).
### Example: Text Block Slide Out Effect
![plugins.core.effects.blocks.text.slideout - Slide out the text block to given direction (until it's not visible). - Example 0](outputs/examples/plugins.core.effects.blocks.text.slideout_example_0.gif)
>This example shows how to add slide out effect on text block.


<details><summary>Example code</summary>

```yaml
frames:
- type: plugins.core.frames.image
  time:
    duration: 1
  configuration:
    file_path: example/assets/image/1.jpg
  effects:
  - type: plugins.core.effects.frames.resize
    configuration:
      mode: center_crop
    vars:
      frame: &id001
        scenario: {}
  blocks:
  - type: plugins.core.blocks.text
    time:
      duration: 1
    position:
    - center
    - center
    configuration:
      content: Hello, World!
      color: white
      font: Roboto-Bold
      size: 50
      margin: 30
      padding: 20
    effects:
    - type: plugins.core.effects.blocks.text.write
      time:
        duration: 1
      vars:
        block: &id002
          frame: *id001
      configuration: {}
    - type: plugins.core.effects.blocks.text.background
      time:
        duration: 1
      configuration:
        color:
        - 0
        - 0
        - 0
        border_radius: 10
        opacity: 1
      vars:
        block: *id002
    - type: plugins.core.effects.blocks.text.slideout
      configuration:
        slide_to: bottom
      time:
        duration: 0.5
      vars:
        block: *id002
    vars: *id002
  vars: *id001
width: 640
height: 240
fps: 24
output_path: outputs/examples/plugins.core.effects.blocks.text.slideout_example_0.gif

```

</details>

<details><summary>Configuration</summary>

| Configuration | Description | Type | Required | Default Value |
| --- | --- | --- | --- | --- |
| slide_to | The direction of the slide out. | str | No | left |


</details>


---
## plugins.core.effects.blocks.audio.play
Play audio on block.
<details><summary>Configuration</summary>

| Configuration | Description | Type | Required | Default Value |
| --- | --- | --- | --- | --- |
| subclip_start | Setting the subclip will start the audio from the given time. | float | No | 0 |
| cut_to_block_duration | If audio is longer than block duration, cut it to block duration. | bool | No | True |


</details>


---
