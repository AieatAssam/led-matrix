#!/home/aieat/led-matrix/venv/bin/python

import asyncio

import aiomisc
import board
import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.rainbowchase import RainbowChase

from led_display import LedDisplay
from rabbitmq_link import QueueCommandConsumer

pixel_pin = board.D18
pixel_width = 16
pixel_height = 16

with (aiomisc.entrypoint(
        QueueCommandConsumer(
            'led_command_queue',
            'led_commands',
            ''),
        LedDisplay(pixel_pin, pixel_width, pixel_height),
        log_level="info",
        log_format="color")
as loop):
    pass
