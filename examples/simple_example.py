'''simple example shown in the readme, slight modification from the example shown on dearpygui github'''

import asyncio

import dearpygui.dearpygui as dpg
from dearpygui_async import DearPyGuiAsync

dpg_async = DearPyGuiAsync()

async def save_callback():
    print("Save Clicked")
    await asyncio.sleep(3)
    print("Save Clicked after 3 more seconds")


dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

with dpg.window(label="Example Window"):
    dpg.add_text("Hello world")
    dpg.add_button(label="Save", callback=save_callback)
    dpg.add_input_text(label="string")
    dpg.add_slider_float(label="float")

dpg.show_viewport()
dpg_async.run()
dpg.destroy_context()
