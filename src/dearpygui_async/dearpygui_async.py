import asyncio
import inspect
import threading

import dearpygui.dearpygui as dpg


class DearPyGuiAsync:

    __run_thread = True

    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.__start_thread, daemon=True)
        self.thread.start()

    def __start_thread(self):
        '''Starts the async event loop on a separate thread to prevent blocking dpg.
        Coroutines should be added to the async thread via this classes loop or one of the helper functions.
        `DearPyGuiAsync.create_task()` for async tasks or `DearPyGuiAsync.create_task_sync()` for sync tasks.
        '''
        asyncio.set_event_loop(self.loop) 
        self.loop.run_forever()

    def __is_coro(self, function):
        return inspect.iscoroutinefunction(function) or inspect.isawaitable(function) 

    async def setup(self):
        '''Special method that runs when starting
        This is helpful for running code that has special setup behavior that may be asynchronous
        '''
        pass

    async def teardown(self):
        '''Special method that runs when shutting down.
        This is helpful for running code that has special shutdown behavior that may be asynchronous
        '''
        pass

    def run_callbacks(self, jobs):
        '''Run the callbacks in the queue or pass to the async thread'''

        if jobs is None:
            pass
        else:
            for job in jobs:
                if job[0] is None:
                    pass
                else:
                    sig = dpg.inspect.signature(job[0])
                    args = [job[arg + 1] for arg in range(len(sig.parameters))]
                    
                    if self.__is_coro(job[0]):
                        try:
                            self.create_task(job[0](*args))
                        except Exception as e:
                            print(e)
                    else:
                        job[0](*args)


    def callback_loop(self):
        '''Event loop for for UI updates and running callbacks.
        This will configure the app to manually manage the callbacks so overwrite this if you want to do something else
        '''
        dpg.configure_app(manual_callback_management=True)
        while self.__run_thread and dpg.is_dearpygui_running():
            self.run_callbacks(dpg.get_callback_queue())
            dpg.render_dearpygui_frame()
        if self.__run_thread:
            self.stop()
        
    def create_task(self, coro):
        '''Run a coroutine on the separate async thread'''

        asyncio.run_coroutine_threadsafe(coro, loop=self.loop)

    def create_task_sync(self, func, *args):
        '''Run a function on the separate async thread'''

        self.loop.call_soon_threadsafe(func, *args)

    def stop(self):
        '''Manually cancel the callback processing task'''

        self.__run_thread = False
        async def stop():
            await self.teardown()
            [task.cancel() for task in asyncio.all_tasks()]
            await asyncio.sleep(0)
            self.loop.stop()
            self.loop.close()

        self.create_task(stop())

    def run(self):
        ''' Run DearPyGui with async compatibility
        Use this in place of `dpg.start_gui()`
        '''
        self.create_task(self.setup())
        self.callback_loop()