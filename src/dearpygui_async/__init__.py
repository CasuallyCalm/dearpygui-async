import asyncio

import dearpygui.dearpygui as dpg


class DearPyGuiAsync:
    __slots__ = ["loop"]

    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()

    async def setup(self):
        pass

    async def teardown(self):
        pass

    async def start(self):
        dpg.configure_app(manual_callback_management=True)
        while dpg.is_dearpygui_running():
            await asyncio.sleep(0)
            dpg.render_dearpygui_frame()
        await self.teardown()

    async def close(self):
        pass

    def run(self):
        self.loop.run_until_complete(self.start())
        self.loop.close()
