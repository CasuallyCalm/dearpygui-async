import asyncio
import time

import dearpygui.dearpygui as dpg


async def _sleep(seconds:float):
    '''An asyncio sleep.

    On Windows this achieves a better granularity than asyncio.sleep

    Args:
        seconds (float): Seconds to sleep for.
    
    '''
    await asyncio.get_running_loop().run_in_executor(None, time.sleep, seconds)

class DearPyGuiAsync:

    __callback_task:asyncio.Task

    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()

    async def setup(self):
        '''
        Special method that runs when starting
        This is helpful for running code that has special setup behavior that may be asynchronous
        '''
        pass

    async def teardown(self):
        '''
        Special method that runs when shutting down.
        This is helpful for running code that has special shutdown behavior that may be asynchronous
        '''
        pass

    async def run_callbacks(self, jobs):
        '''
        Run the callbacks that were added
        '''
        if jobs is None:
            pass
        else:
            for job in jobs:
                if job[0] is None:
                    pass
                else:
                    sig = dpg.inspect.signature(job[0])
                    args = []
                    for arg in range(len(sig.parameters)):
                        args.append(job[arg + 1])
                    if asyncio.iscoroutinefunction(
                        job[0]
                    ) or asyncio.iscoroutinefunction(job[0].__call__):
                        try:
                            await job[0](*args)
                        except Exception as e:
                            print(e)
                    else:
                        job[0](*args)


    async def callback_loop(self):
        '''
        |coro|
        Processes the the callbacks asynchronously
        This will configure the app to manually manage the callbacks so overwrite this if you want to do something else
        '''
        dpg.configure_app(manual_callback_management=True)
        while dpg.is_dearpygui_running():
            asyncio.create_task(self.run_callbacks(dpg.get_callback_queue()))
            dpg.render_dearpygui_frame()
            await _sleep(0.0095)
        await self.teardown() 

    async def start(self):
        '''
        |coro|
        For starting the gui in an async context
        Usually to add a gui to another async process
        '''
        await self.setup()
        self._callback_task = asyncio.create_task(self.callback_loop()) 
    
    async def __start(self):
        await self.setup()
        await self.callback_loop()

    async def stop(self):
        '''
        |coro|
        Manually cancel the callback processing task
        '''
        self._callback_task.cancel()
        await self.teardown()

    def run(self):
        '''
        |blocking|
        Run DearPyGui with async compatibility
        Use this in place of `dpg.start_gui()`
        
        '''
        self.loop.run_until_complete(self.__start())
