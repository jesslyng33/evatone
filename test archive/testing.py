import asyncio
from hume import AsyncHumeClient
from hume.expression_measurement.stream import Config
from hume.expression_measurement.stream.socket_client import StreamConnectOptions
from hume.expression_measurement.stream.types import StreamLanguage

samples = [
    "Mary had a little lamb,",
    "Its fleece was white as snow."
    "Everywhere the child went,"
    "The little lamb was sure to go."
]

async def main():
    client = AsyncHumeClient(api_key="4pI4JMESdAFcX7YWA28TP4Fk7GFr6Oiw2zVmh7AizVV8lhP5")

    model_config = Config(language=StreamLanguage())

    stream_options = StreamConnectOptions(config=model_config)

    async with client.expression_measurement.stream.connect(options=stream_options) as socket:
        for sample in samples:
            result = await socket.send_text(sample)
            print(result.language.predictions[0].emotions)

if __name__ == "__main__":
    asyncio.run(main())