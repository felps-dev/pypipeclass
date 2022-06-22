

from abc import abstractmethod
import asyncio
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection


class SyncedProcess(Process):
    pipe_rcv = Connection
    pipe_snd = Connection
    remote_commands = {}
    local_commands = {}
    debug = False

    def __init__(self, debug=False):
        Process.__init__(self)
        pv, ps = Pipe()
        self.pipe_rcv = pv
        self.pipe_snd = ps
        self.debug = debug

    def send_cmd(self, pipe, cmd, data):
        '''
            Create command object and send to relative pipe
        '''
        pipe.send({
            'cmd': cmd,
            'data': data
        })

    def send_remote(self, cmd, data=None):
        '''
            Send command to remote process
        '''
        self.send_cmd(self.pipe_snd, cmd, data)

    def send_local(self, cmd, data=None):
        '''
            Send command to local process
        '''
        self.send_cmd(self.pipe_rcv, cmd, data)

    def proccess_comand(self, data, cmd_list, dir='remote'):
        '''
            Generic processing command function, can be
            overrited
        '''
        if(data['cmd'] in cmd_list):
            ret = cmd_list[data['cmd']]
            if(self.debug):
                print('Received ' + dir + ' command: ' + data['cmd'])
            if(callable(ret)):
                ret(self, data['data'], self.send_local if dir ==
                    'remote' else self.send_remote)
            elif(isinstance(ret, str)):
                if(dir == 'remote'):
                    self.send_local(ret, None)
                elif(dir == 'local'):
                    self.send_remote(ret, None)
        else:
            if(self.debug):
                print('Command not found: ', data['cmd'])

    async def remote_listen(self):
        '''
            Remote pooling and listen for reacting to commands
        '''
        while True:
            if(self.pipe_rcv.poll(timeout=0)):
                data = self.pipe_rcv.recv()
                self.proccess_comand(data, self.remote_commands, 'remote')
            await asyncio.sleep(0.0001)

    @abstractmethod
    async def remote_job(self):
        '''
            Generic remote job, must be overrited.
        '''
        pass

    async def remote_proccess(self):
        '''
            Processing of remote jobs, we can have a lot of jobs later.
        '''
        while True:
            await self.remote_job()
            await asyncio.sleep(0.0001)

    async def remote_main(self):
        '''
            Main remote wrapper for executing functions
        '''
        await asyncio.gather(self.remote_listen(), self.remote_proccess())

    async def local_listen(self):
        '''
            Local pooling and listen for reacting to commands
        '''
        while True:
            if(self.pipe_snd.poll(timeout=0)):
                data = self.pipe_snd.recv()
                self.proccess_comand(data, self.local_commands, 'local')
            await asyncio.sleep(0.0001)

    @abstractmethod
    async def local_job(self):
        '''
            Generic local job, must be overrited.
        '''
        pass

    async def local_proccess(self):
        '''
            Processing of local jobs, we can have a lot of jobs later.
        '''
        while True:
            await self.local_job()
            await asyncio.sleep(0.0001)

    async def local_main(self):
        '''
            Main local wrapper for executing functions
        '''
        await asyncio.gather(self.local_listen(), self.local_proccess())

    async def start(self):
        '''
            Start function, executed on local side.
        '''
        super().start()
        # wait for commands on local side
        await self.local_main()

    def run(self):
        '''
            Run function, executed on remote side.
        '''
        asyncio.run(self.remote_main())
