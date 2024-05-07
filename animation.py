import io
import typing
from PIL import Image


frames: typing.List[Image.Image] = []
speed = 0.1

def convert_frames(frames: typing.List[bytes]) -> typing.List[Image.Image]:
     return [Image.open(io.BytesIO(f)) for f in frames]

def set_frames(new_frames: typing.List[Image], new_speed: float, size: typing.Tuple[int, int]) -> None:
    global frames
    global speed
    frame: Image
    frames = []
    for frame in new_frames:
        # ensure they frames are all 16x16 pixels and if not resize
        image = Image.new("RGBA", size)
        image.alpha_composite(frame.resize(size))
        image.convert('RGB')
        frames.append(image)
    speed = new_speed

