'''Basic example with a background task and a button that starts another process without blocking the gui'''

import asyncio

import dearpygui.dearpygui as dpg
from dearpygui_async import DearPyGuiAsync

HEIGHT = 300
WIDTH = 400


async def save_callback():
    _input = dpg.get_value('input')
    print(f"Saved input: {_input}")
    await asyncio.sleep(3)
    _new_input = dpg.get_value('input')
    if _input != _new_input:
        print(f"Your input changed to: {_new_input}")



def dpg_start():

    dpg.create_context()
    dpg.create_viewport(width=WIDTH, height=HEIGHT)
    dpg.setup_dearpygui()

    with dpg.window(label="Async Example Window", tag="Window", width=WIDTH, height=HEIGHT):
        dpg.add_text("Controls")
        dpg.add_button(label="Save", callback=save_callback)
        dpg.add_input_text(label="string", tag="input")
        dpg.add_slider_float(label="float", tag="slider")

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
