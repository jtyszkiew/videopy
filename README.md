videopy is a small script built on to of moviepy that allows to define videos as "scenarios" which are a sequence of frames containing blocks & effects.

I've created it to start automating the creation of small videos for youtube and others. It's still in a very early stage but I'm already using it to create some videos.

Example scenario can be found in the `example/scenario.yml` file.

It is also possible to create some scripts that will generate the scenario file for you. For example, I've created a script that will ask for some data and than generate video from image files found in the asked directory.

Installation: `pip install -r requirements.txt`

You can check available commands by running `python video.py --help`.

To run example scenario, you can run `python video.py run --scenario-file=example/scenario.yml`.

Example output video is saved in the `example/output` directory

btw. It's my first project written in Python - any suggestions are welcome!

btw2. I will try to make this README better experience in the future. 
