from typing import Any

import aiomisc
import asyncio
import board
import neopixel
from adafruit_blinka.microcontroller.generic_micropython import Pin
from adafruit_pixel_framebuf import PixelFramebuffer
from animation import frames as animation_frames, speed as animation_speed

class LedDisplay(aiomisc.Service):
    def __init__(self, led_pin: Pin, pixel_width: int, pixel_height: int, **kwargs: Any):
        super().__init__(**kwargs)
        self._leds_width = pixel_width
        self._leds_height = pixel_height
        self._pixels = neopixel.NeoPixel(
            led_pin,
            pixel_width * pixel_height,
            brightness=0.3,
            auto_write=False)
        # noinspection PyTypeChecker
        self._pixel_buf = PixelFramebuffer(
            self._pixels,
            pixel_width,
            pixel_height,
            reverse_x=True)
        # clear display
        self._pixel_buf.fill_rect(0, 0, pixel_width, pixel_height, 0x000000)
        self._pixel_buf.display()

    async def start(self):
        while True:
            for frame in animation_frames:
                self._pixel_buf.image(frame)
                self._pixel_buf.display()
                await asyncio.sleep(animation_speed)
            if not animation_frames:
                await asyncio.sleep(animation_speed)