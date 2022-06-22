import asyncio
from multiprocessing import current_process
from pypipeclass.classes import SyncedProcess


def say_hi(th, data, res):
    print(current_process().name,
          'Hi! This function is running on another process, as you can see, the some_prop is different from the local process', th.some_prop)
    # Send command back to local process
    res('listen_hi', 'Example data')


def got_hi(th, data, res):
    print(current_process().name,
          'And here im receiving this data from remote process: ', data, 'And this is the local prop value', th.some_prop)


class MyTest(SyncedProcess):
    # This prop may have 2 values, one on remote and other on local.
    some_prop = None

    # This is commands that remote will receive.
    remote_commands = {'answer_hi': say_hi}

    # This is commands that local will receive
    local_commands = {'listen_hi': got_hi}

    # Remote function that will run on remote process
    async def remote_job(self):
        self.some_prop = 2

    # Local function that will run on local process
    async def local_job(self):
        self.some_prop = 4


async def do_something_paralel(ins: MyTest):
    while True:
        # In parallel, we send a message to remote, called answer_hi
        ins.send_remote('answer_hi')
        # We need to sleep for waking up eventloop (I don't know why asyncio do this)
        await asyncio.sleep(0.00001)


async def local_main():
    ins = MyTest()
    # The .start() will block if don't run on async proccess
    # so we need to run both functions at same time.
    await asyncio.gather(do_something_paralel(ins), ins.start())

if __name__ == '__main__':
    # As an asyncio, we need to run on async function.
    asyncio.run(local_main())
