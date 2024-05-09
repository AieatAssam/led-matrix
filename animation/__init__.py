import io
import typing
from PIL import Image

__all__ = ['animation']

class Animation:
    def __init__(self):
        self._frames: typing.List[Image.Image] = []
        self._speed = 0.1

    @property
    def speed(self):
        return self._speed

    @property
    def frames(self):
        return self._frames

    def convert_frames(self, frames: typing.List[bytes]) -> typing.List[Image.Image]:
         return [Image.open(io.BytesIO(f)) for f in frames]

    def set_frames(self, new_frames: typing.List[Image], new_speed: float, size: typing.Tuple[int, int]) -> None:
        frame: Image
        self._frames.clear()
        for frame in new_frames:
            # ensure they frames are all 16x16 pixels and if not resize
            image = Image.new("RGBA", size)
            image.alpha_composite(frame.resize(size))
            self._frames.append(image.convert('RGB'))
        self._speed = new_speed if new_speed > 0 else 0.1

animation = Animation()