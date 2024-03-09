import asyncio
import threading

import dearpygui.dearpygui as dpg


def _is_coro(function):
    return asyncio.iscoroutinefunction(function) or dpg.inspect.isawaitable(function) #asyncio.iscoroutinefunction(function.__call__) 

class DearPyGuiAsync:

    __callback_task:asyncio.Task
    __run_thread = True

    def __init__(self):
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.__start_thread, daemon=True).start()

    def __start_thread(self):
        '''
        Starts the async event loop on a separate thread to prevent blocking dpg.
        Coroutines must be added using either self.loop.
        '''
        asyncio.set_event_loop(self.loop) 
        self.loop.run_forever()


    async def setup(self):
        '''
        Special method that runs when starting
        This is helpful for running code that has special setup behavior that may be asynchronous
        '''
        print('setup')
        pass

    async def teardown(self):
        '''
        Special method that runs when shutting down.
        This is helpful for running code that has special shutdown behavior that may be asynchronous
        '''
        print('teardown')
        pass

    def run_callbacks(self, jobs):
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
                    if _is_coro(job[0]):
                        try:
                            self.create_task(job[0](*args))
                        except Exception as e:
                            print(e)
                    else:
                        job[0](*args)


    def callback_loop(self):
        '''
        Processes the the callbacks asynchronously
        This will configure the app to manually manage the callbacks so overwrite this if you want to do something else
        '''
        dpg.configure_app(manual_callback_management=True)
        while self.__run_thread and dpg.is_dearpygui_running():
            self.run_callbacks(dpg.get_callback_queue())
            dpg.render_dearpygui_frame()
        if self.__run_thread:
            self.stop()
        
    # def __start(self):
    #     '''
    #     |blocking|
    #     Run DearPyGui with async compatibility
    #     Use this in place of `dpg.start_gui()`
        
    #     '''
    #     self.create_task(self.setup())
    #     self.callback_loop()

    def create_task(self, coro):
        '''
        Run a coroutine on the separate async thread
        '''
        if _is_coro(coro):
            asyncio.run_coroutine_threadsafe(coro, loop=self.loop)

    def create_task_sync(self, func, *args):
        '''
        Run a function on the separate async thread
        '''
        self.loop.call_soon_threadsafe(func, *args)

    def stop(self):
        '''
        Manually cancel the callback processing task
        '''
        self.__run_thread = False
        async def stop():
            await self.teardown()
            await asyncio.sleep(0)
            self.loop.stop
        self.create_task(stop())

    def run(self):
        '''
        |blocking|
        Run DearPyGui with async compatibility
        Use this in place of `dpg.start_gui()`
        
        '''
        # self.__start()
        self.create_task(self.setup())
        self.callback_loop()