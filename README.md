# pypipeclass

An async multiprocessing Python class with easy communication using pipes

![Imagem exemplo](https://i.imgur.com/7iqWbTe.png)

### RoadMap

- [x] Create base class
- [ ] Create decorators **@command** and **@job** for class functions
- [ ] Add more ideas of implementation

### Explanation

With this class we can have a lot of proccess communication with the main without needing of writing pipes or queues, that solve a lot of problems with async processes.

<p align="center">
    <img src="https://i.imgur.com/iyhjfES.png" />
</p>

In our `example.py` we have a class named **SomeClass**, when we apply to a variable `test = SomeClass()` we have one instance of `test` on the **Main Process**. After we call `test.start()`, another process named `SomeClass-1` is created, and has another instance of `test` on it, wich comunicates with `test` on **Main Process** using **pipes**.

### Usage

This simple ping-pong example above shows how the **MainProcess** communicate with **SimpleExample-1** wich is created when we call `simple_example.start()` method. As `start()` a asynchronous infinite looping method, we need to run in paralel with something else for avoiding blocking the **MainProcess**.

```python
import asyncio
from pypipeclass.classes import SyncedProcess

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
```

### Extras

Both remote and local commands can be functions and you can also have jobs running on both sides, see **complex_example.py** for more info.
