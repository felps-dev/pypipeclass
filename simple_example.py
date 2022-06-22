import asyncio
from pypipeclass.classes import SyncedProcess


class SimpleExample(SyncedProcess):
    # This is commands that remote will receive.
    remote_commands = {'ping': 'pong'}
    # This is commands that local will receive
    local_commands = {'pong': 'ping'}


# Instantiate the simple_example
simple_example = SimpleExample(debug=True)


async def do_something_paralel():
    while True:
        # In parallel, we send a message to remote, called answer_hi
        simple_example.send_remote('ping')
        # We need to sleep for waking up eventloop (I don't know why asyncio do this)
        await asyncio.sleep(0.00001)


async def local_main():
    # The .start() will block if don't run on async proccess
    # so we need to run both functions at same time.
    await asyncio.gather(do_something_paralel(), simple_example.start())

if __name__ == '__main__':
    # As an asyncio, we need to run on async function.
    asyncio.run(local_main())
