import asyncio

import dearpygui.dearpygui as dpg
from dearpygui_async import DearPyGuiAsync

dpg_async = DearPyGuiAsync()


def save_callback():
    print("Save Clicked")


async def coro():
    while True:
        print("background task")
        await asyncio.sleep(3)


dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

with dpg.window(label="Example Window"):
    dpg.add_text("Hello world")
    dpg.add_button(label="Save", callback=save_callback)
    dpg.add_input_text(label="string")
    dpg.add_slider_float(label="float")

dpg_async.loop.create_task(coro())

dpg.show_viewport()
dpg_async.run()
dpg.destroy_context()
