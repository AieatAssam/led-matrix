import logging
import sys
from typing import Any

import aiomisc
import asyncio
import neopixel
from adafruit_blinka.microcontroller.generic_micropython import Pin
from adafruit_pixel_framebuf import PixelFramebuffer
from animation import animation

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

class LedDisplay(aiomisc.Service):
    def __init__(self, led_pin: Pin, pixel_width: int, pixel_height: int, **kwargs: Any):
        super().__init__(**kwargs)
        self._leds_width = pixel_width
        self._leds_height = pixel_height
        self._pixels = neopixel.NeoPixel(
            led_pin,
            pixel_width * pixel_height,
            brightness=0.1,
            auto_write=False)
        # noinspection PyTypeChecker
        self._pixel_buf = PixelFramebuffer(
            self._pixels,
            pixel_width,
            pixel_height,
            reverse_x=True)
        # clear display
        logger.info('Clearing display')
        self._pixel_buf.fill_rect(0, 0, pixel_width, pixel_height, 0x000000)
        self._pixel_buf.display()

    async def start(self):
        logger.info(f'Starting LedDisplay')
        while True:
            if animation.frames:
                logger.debug(f'Animation frames: {animation.frames}')
                for frame in animation.frames:
                    logger.debug('Animating frame')
                    self._pixel_buf.image(frame)
                    self._pixel_buf.display()
                    await asyncio.sleep(animation.speed)
            else:
                logger.debug('Waiting for frames')
                await asyncio.sleep(animation.speed)