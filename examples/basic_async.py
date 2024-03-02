import asyncio

import dearpygui.dearpygui as dpg
from dearpygui_async import DearPyGuiAsync

HEIGHT = 400
WIDTH = 600


def save_callback():
    print("Save Clicked")


def dpg_start():

    dpg.create_context()
    dpg.create_viewport(width=WIDTH, height=HEIGHT)
    dpg.setup_dearpygui()

    with dpg.window(label="Example Window", tag="Window", width=WIDTH, height=HEIGHT):
        dpg.add_text("Hello world")
        dpg.add_button(label="Save", callback=save_callback)
        dpg.add_input_text(label="string", tag="input")
        dpg.add_slider_float(label="float")

    dpg.show_viewport()


def dpg_stop():
    dpg.destroy_context()


dpg_async = DearPyGuiAsync()


async def coro():
    while True:
        print("background task")
        await asyncio.sleep(3)


async def hook():
    asyncio.create_task(coro())


dpg_async.setup = hook

if __name__ == "__main__":
    dpg_start()
    dpg_async.run()
    dpg_stop()
