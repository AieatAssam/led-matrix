import io
import logging
import asyncio
import aiomisc
import os
import json
import base64

import aio_pika
from dotenv import load_dotenv

import animation

class QueueCommandConsumer(aiomisc.Service):
    def __init__(self, queue, exchange, routing_key, **kwargs):
        load_dotenv()
        self._connection_string = os.getenv('RABBITMQ_URL')
        self._queue = queue
        self._exchange = exchange
        self._routing_key = routing_key
        super().__init__(**kwargs)

    async def process_message(self,
        message: aio_pika.abc.AbstractIncomingMessage,
    ) -> None:
        async with message.process():
            try:
                print(message.body)
                message_payload = json.load(io.BytesIO(message.body))
                if message_payload['frames'] and message_payload['speed']:
                    # valid payload
                    animation.set_frames(
                        # each frame is base64 encoded, so decode to bytes
                        animation.convert_frames([base64.b64decode(f) for f in message_payload['frames']]),
                        message_payload['speed'],
                        (16, 16)
                    )
            finally:
                pass



    async def start(self) -> None:
        logging.basicConfig(level=logging.DEBUG)
        connection = await aio_pika.connect_robust(
            self._connection_string
        )

        async with connection:
            # Creating channel
            channel = await connection.channel()

            # Will take no more than 10 messages in advance
            await channel.set_qos(prefetch_count=10)

            # Declaring queue
            queue = await channel.declare_queue(self._queue, auto_delete=True)
            exchange = await channel.declare_exchange(self._exchange)
            await queue.bind(exchange, self._routing_key)
            await queue.consume(self.process_message)

            try:
                # Wait until terminate
                await asyncio.Future()
            finally:
                await connection.close()


if __name__ == '__main__':
    with (aiomisc.entrypoint(
            QueueCommandConsumer(
                'led_command_queue',
                'led_commands',
                ''),
            log_level="info",
            log_format="color")
    as loop):
        pass