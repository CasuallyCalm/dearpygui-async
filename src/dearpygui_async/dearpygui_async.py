import asyncio

import dearpygui.dearpygui as dpg


class DearPyGuiAsync:
    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()

    async def setup(self):
        pass

    async def teardown(self):
        pass

    async def run_callbacks(self, jobs):
        """New in 1.2. Runs callbacks from the callback queue and checks arguments."""

        ran_awaitable_function = False

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
                            ran_awaitable_function = True
                        except Exception as e:
                            print(e)
                    else:
                        job[0](*args)

        if not ran_awaitable_function:
            await asyncio.sleep(0)

    async def start(self):
        await self.setup()
        dpg.configure_app(manual_callback_management=True)
        while dpg.is_dearpygui_running():
            await self.run_callbacks(dpg.get_callback_queue())
            dpg.render_dearpygui_frame()
        await self.stop()

    async def stop(self):
        await self.teardown()
        dpg.destroy_context()

    def run(self):
        self.loop.run_until_complete(self.start())
